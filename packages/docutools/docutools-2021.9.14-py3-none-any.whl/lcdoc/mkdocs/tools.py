import datetime
import sys
import time
from functools import partial

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import log as mkdlog

from lcdoc.const import PageStats, Stats, now_ms, t0
from lcdoc.tools import (
    app,
    dirname,
    exists,
    now,
    os,
    project,
    read_file,
    require,
    write_file,
)


def add_post_page_func(kw, f):
    p = kw['LP'].page
    h = getattr(p, 'lp_on_post_page', [])
    h.append(partial(f, page=p, config=kw['LP'].config))
    p.lp_on_post_page = h


# -------------------------------------------------------- replacements


def srclink(fn, config, line=None, match=None, title=''):
    # TODO: allow others:
    u = config['repo_url'] + 'blob/master'
    r = project.root(config)
    if fn[0] == '/':
        fnr = fn.split(r, 1)[1]
    else:
        fnr = '/' + fn
    lnk = u + fnr
    if match:
        s = read_file(r + fnr, dflt='')
        m = s.split(match, 1)
        if len(m) > 1:
            line = len(m[0].splitlines())
    if line:
        lnk += '#L%s' % line
    # return T
    title = (title + ' ') if title else ''
    return {
        'link': '[%s:fontawesome-brands-git-alt:](%s)' % (title, lnk),
        'url': lnk,
    }  # {align=right}'


# used in mdreplace
def srcref(**kw):
    """Often used as replacement function
    In mdreplace.py:
    'srcref': inline_srclink,
    """
    line = kw['line']
    fn = line.split(':srcref:', 1)[1].split(' ', 1)[0]
    if fn[-1] in {',', ')', ']', '}'}:
        fn = fn[:-1]
    repl = ':srcref:' + fn
    if not ',' in fn:
        if '=' in fn:
            l = fn.split('=')
            spec = {'fn': l[0], 'm': l[1]}
        else:
            spec = {'fn': fn}
    else:
        try:
            spec = dict([kv.split('=', 1) for kv in fn.split(',')])
        except Exception as ex:
            app.error('inline_srclink failed', line=line, page=kw['page'])
            return {'line': line}
    spec['t'] = spec.get('t', '`%s`' % spec['fn'])  # title default: file path
    if spec['t'] == 'm':
        spec['t'] = spec['m']
    # if 'changelog' in line: breakpoint()  # FIXME BREAKPOINT
    l = srclink(spec['fn'], kw['config'], match=spec.get('m'), title=spec['t'])
    return {'line': line.replace(repl, l['link'])}


def find_md_files(match, config):
    require('fd --version')
    dd = config['docs_dir']
    cmd = "cd '%s' && fd -I --type=file -e md | grep '%s'" % (dd, match)
    r = os.popen(cmd).read().strip().splitlines()
    # split off docs dir:
    return r


def theme_dir(config):
    """strangly we don't see custom_dir in config.theme - it only inserts it, when given, into config.theme.dirs
    """
    cd = config['theme'].dirs[0]
    if cd.endswith('/' + config['theme'].name):
        app.debug('Theme dir is docs dir')
        return config['docs_dir']
    app.info('Theme dir is custom', dir=cd)
    return cd


def link_assets(plugin, fn_plugin, config):
    """Linking assets folder content into D/lcd/<pluginname>, where D is either docs dir or custom_dir
    Setting plugin.d_assets to that folder.
    """
    # extra css and js has be in docs dir, even with custom dir:
    d = dirname(fn_plugin) + '/assets'
    if not exists(d):
        app.die('Cannot link: No assets found', dir=d)
    n = fn_plugin.rsplit('/', 2)[-2]
    to = config['docs_dir'] + '/lcd'
    t = to + '/' + n
    plugin.d_assets = t
    if exists(t):
        return app.debug('Exists already', linkdest=t)
    app.warning('Linking', frm=d, to=t)
    os.makedirs(dirname(t), exist_ok=True)
    cmd = 'ln -s "%s" "%s"' % (d, t)
    if os.system(cmd):
        app.die('Could not link assets')


def split_off_fenced_blocks(markdown, fc_crit=None, fc_process=None, fcb='```'):
    fc_crit = (lambda s: True) if fc_crit is None else fc_crit
    lines = markdown if isinstance(markdown, list) else markdown.splitlines()
    mds, fcs = [[]], []
    lnr = 0
    while lines:
        l = lines.pop(0)
        lnr += 1
        ls = l.lstrip()
        if not ls.startswith(fcb):
            mds[-1].append(l)
            continue
        beg = (' ' * (len(l) - len(l.lstrip()))) + fcb
        if not fc_crit(ls):
            # an fc but crit is not met (e.g. not lp) -> ignore all till closed:
            while lines:
                mds[-1].append(l)
                l = lines.pop(0)
                lnr += 1
                if l.startswith(beg) and l.strip() == fcb:
                    mds[-1].append(l)
                    lnr -= 1
                    break
            continue

        fc = []
        mds.append([])
        fc.append(l)
        fc_ln_start = lnr
        while lines:
            l = lines.pop(0)
            lnr += 1
            fc.append(l)
            if l.startswith(beg) and l.strip() == fcb:
                break
            elif not lines:
                msg = 'Closing fenced block. Your markdown will not be correctly rendered'
                app.warning(msg, block=fc)
                lines.append(beg)
        if fc_process:
            fc = fc_process(fc)
            fc['linenr'] = fc_ln_start
        fcs.append(fc)
    return mds, fcs


hooks = [
    'on_serve',
    'on_config',
    'on_pre_build',
    # 'on_files',
    # 'on_nav',
    # 'on_env',
    'on_post_build',
    # 'on_build_error',
    # 'on_pre_template',
    # 'on_template_context',
    # 'on_post_template',
    # 'on_pre_page',
    # 'on_page_read_source',
    'on_page_markdown',
    # 'on_page_content',
    # 'on_page_context',
    'on_post_page',
]

clsn = lambda o: o.__class__.__name__


def get_page(hookname, a, kw, c={}):
    pos = c.get(hookname)
    if pos is None:
        if 'page' in kw:
            pos = 'kw'
        else:
            h = None
            for i, arg in zip(range(len(a)), a):
                if getattr(arg, 'is_page', None):
                    h = i
                    break
            if h is None:
                c[hookname] = -1
                return
    if pos == 'kw':
        return kw['page']
    if pos < 0:
        return
    return a[pos]


def wrap_hook(plugin, hook, hookname):
    """Decorates the actual lcd- plugin hooks with stats and logging"""
    n = clsn(plugin)
    Stats[n][hookname] = {}
    PageStats[n][hookname] = {}

    def wrapped_hook(*a, plugin=plugin, hook=hook, name=n, hookname=hookname, **kw):
        plugin.stats = stats = Stats[n][hookname]
        page = get_page(hookname, a, kw)
        p = t = ''
        if page:
            stats = PageStats[n][hookname]
            stats[(page.url, page.title)] = stats = page.stats = {}
            f = page.file.src_path
            p = ':%s' % f.rsplit('/', 1)[-1]
            t = ': %s' % f
        on = app.name  # orig name
        app.name = n.replace('Plugin', '') + p  # e.g. LPPlugin
        app.debug('%s.%s%s' % (n, hookname, t))
        t0 = now()
        r = hook(*a, **kw)
        dt = now() - t0
        stats['dt'] = stats.get('dt', 0) + dt
        app.name = on
        return r

    setattr(plugin, hookname, wrapped_hook)


def reset_if_is_first_loaded_plugin_and_hash_changed(plugin, c={}):
    """mkdocs serve, we must detect if this is a new build"""
    cl = clsn(plugin)
    if c and not cl in c:
        return
    if not c:
        c[cl] = 0
    if c[cl] == hash(plugin):
        return
    c[cl] = hash(plugin)
    return reset()


def reset():
    import lcdoc.const as c

    t0[0] = now_ms()

    [k.clear() for k in [c.Stats, c.PageStats]]
    c.LogStats.update({k: 0 for k in c.LogStats})
    return True


class MDPlugin(BasePlugin):
    def __init__(self):
        # also on mkdocs serve, this is called at each rebuild:
        r = reset_if_is_first_loaded_plugin_and_hash_changed(self)
        app.setup_logging(mkdlog, name='lcd')
        if r:
            d = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
            app.info('Ran reset, cleared stats', reset=r, utc=d, unix=int(time.time()))
        Stats[clsn(self)] = {}
        PageStats[clsn(self)] = {}
        for h in hooks:
            f = getattr(self, h, None)
            if not f:
                continue
            wrap_hook(self, f, h)


"""
All Hooks with Params:
https://www.mkdocs.org/dev-guide/plugins/
"""
