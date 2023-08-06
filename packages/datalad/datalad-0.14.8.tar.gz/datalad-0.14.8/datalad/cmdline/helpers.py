# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""
"""

__docformat__ = 'restructuredtext'

import argparse
import os
import re
import sys
import gzip
from tempfile import NamedTemporaryFile
from textwrap import wrap

from ..cmd import WitlessRunner as Runner
from ..interface.common_opts import eval_defaults
from ..log import is_interactive
from ..utils import (
    ensure_unicode,
    getpwd,
    unlink,
)
from ..version import __version__
from ..dochelpers import exc_str

from logging import getLogger
lgr = getLogger('datalad.cmdline')


class HelpAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # Lets use the manpage on mature systems but only for subcommands --
        # --help should behave similar to how git does it:
        # regular --help for "git" but man pages for specific commands.
        # It is important since we do discover all subcommands from entry
        # points at run time and thus any static manpage would like be out of
        # date
        interactive = is_interactive()
        if interactive \
                and option_string == '--help' \
                and ' ' in parser.prog:  # subcommand
            try:
                import subprocess
                # get the datalad manpage to use
                manfile = os.environ.get('MANPATH', '/usr/share/man') \
                    + '/man1/{0}.1.gz'.format(parser.prog.replace(' ', '-'))
                # extract version field from the manpage
                if not os.path.exists(manfile):
                    raise IOError("manfile is not found")
                with gzip.open(manfile) as f:
                    man_th = [line for line in f if line.startswith(b".TH")][0]
                man_version = man_th.split(b' ')[-1].strip(b" '\"\t\n").decode('utf-8')

                # don't show manpage if man_version not equal to current datalad_version
                if __version__ != man_version:
                    raise ValueError
                subprocess.check_call(
                    'man %s 2> /dev/null' % manfile,
                    shell=True)
                sys.exit(0)
            except (subprocess.CalledProcessError, IOError, OSError, IndexError, ValueError) as e:
                lgr.debug("Did not use manpage since %s", exc_str(e))
        if option_string == '-h':
            usage = parser.format_usage()
            ucomps = re.match(
                r'(?P<pre>.*){(?P<cmds>.*)}(?P<post>....*)',
                usage,
                re.DOTALL)
            if ucomps:
                ucomps = ucomps.groupdict()
                indent_level = len(ucomps['post']) - len(ucomps['post'].lstrip())
                usage = '{pre}{{{cmds}}}{post}'.format(
                    pre=ucomps['pre'],
                    cmds='\n'.join(wrap(
                        ', '.join(sorted(c.strip() for c in ucomps['cmds'].split(','))),
                        break_on_hyphens=False,
                        subsequent_indent=' ' * indent_level)),
                    post=ucomps['post'],
                )
            helpstr = "%s\n%s" % (
                usage,
                "Use '--help' to get more comprehensive information.")
        else:
            helpstr = parser.format_help()
        # better for help2man
        # for main command -- should be different sections. And since we are in
        # heavy output massaging mode...
        if "commands for dataset operations" in helpstr.lower():
            opt_args_str = '*Global options*'
            pos_args_str = '*Commands*'
            # tune up usage -- default one is way too heavy
            helpstr = re.sub(r'^[uU]sage: .*?\n\s*\n',
                             'Usage: datalad [global-opts] command [command-opts]\n\n',
                             helpstr,
                             flags=re.MULTILINE | re.DOTALL)
            # and altogether remove sections with long list of commands
            helpstr = re.sub(r'positional arguments:\s*\n\s*{.*}\n', '', helpstr)
        else:
            opt_args_str = "*Options*"
            pos_args_str = "*Arguments*"
        helpstr = re.sub(r'optional arguments:', opt_args_str, helpstr)
        helpstr = re.sub(r'positional arguments:', pos_args_str, helpstr)
        # usage is on the same line
        helpstr = re.sub(r'^usage:', 'Usage:', helpstr)

        if interactive and option_string == '--help':
            import pydoc
            pydoc.pager(helpstr)
        else:
            print(helpstr)
        sys.exit(0)


class LogLevelAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        from ..log import LoggerHelper
        LoggerHelper().set_level(level=values)


# MIH: Disabled. Non-functional, untested.
#class PBSAction(argparse.Action):
#    """Action to schedule actual command execution via PBS (e.g. Condor)"""
#    def __call__(self, parser, namespace, values, option_string=None):
#        pbs = values[0]
#        import pdb; pdb.set_trace()
#        i = 1


def parser_add_common_opt(parser, opt, names=None, **kwargs):
    from . import common_args
    opt_tmpl = getattr(common_args, opt)
    opt_kwargs = opt_tmpl[2].copy()
    opt_kwargs.update(kwargs)
    if names is None:
        parser.add_argument(*opt_tmpl[1], **opt_kwargs)
    else:
        parser.add_argument(*names, **opt_kwargs)


def parser_add_common_options(parser, version):
    parser_add_common_opt(parser, 'log_level')
    parser_add_common_opt(parser, 'pbs_runner')
    parser_add_common_opt(parser, 'change_path')
    parser_add_common_opt(
        parser,
        'version',
        version=f'datalad {version}\n')
    if __debug__:
        parser.add_argument(
            '--dbg', action='store_true', dest='common_debug',
            help="enter Python debugger when uncaught exception happens")
        parser.add_argument(
            '--idbg', action='store_true', dest='common_idebug',
            help="enter IPython debugger when uncaught exception happens")
    parser.add_argument(
        '-c', action='append', dest='cfg_overrides', metavar='KEY=VALUE',
        help="""configuration variable setting. Overrides any configuration
        read from a file, but is potentially overridden itself by configuration
        variables in the process environment.""")
    # CLI analog of eval_params.result_renderer but with `<template>` handling
    # and a different default: in Python API we have None as default and do not render
    # the results but return them.  In CLI we default to "default" renderer
    parser.add_argument(
        '-f', '--output-format', dest='common_output_format',
        default='default',
        type=ensure_unicode,
        metavar="{default,json,json_pp,tailored,'<template>'}",
        help="""select format for returned command results. 'default' give one line
        per result reporting action, status, path and an optional message;
        'json' renders a JSON object with all properties for each result (one per
        line); 'json_pp' pretty-prints JSON spanning multiple lines; 'tailored'
        enables a command-specific rendering style that is typically
        tailored to human consumption (no result output otherwise),
        '<template>' reports any value(s) of any result properties in any format
        indicated by the template (e.g. '{path}'; compare with JSON
        output for all key-value choices). The template syntax follows the Python
        "format() language". It is possible to report individual
        dictionary values, e.g. '{metadata[name]}'. If a 2nd-level key contains
        a colon, e.g. 'music:Genre', ':' must be substituted by '#' in the template,
        like so: '{metadata[music#Genre]}'. [Default: '%(default)s']""")
    parser.add_argument(
        '--report-status', dest='common_report_status',
        choices=['success', 'failure', 'ok', 'notneeded', 'impossible', 'error'],
        help="""constrain command result report to records matching the given
        status. 'success' is a synonym for 'ok' OR 'notneeded', 'failure' stands
        for 'impossible' OR 'error'.""")
    parser.add_argument(
        '--report-type', dest='common_report_type',
        choices=['dataset', 'file'],
        action='append',
        help="""constrain command result report to records matching the given
        type. Can be given more than once to match multiple types.""")
    # CLI analog of eval_params.on_failure. TODO: dedup
    parser.add_argument(
        '--on-failure', dest='common_on_failure',
        default=eval_defaults['on_failure'],
        choices=['ignore', 'continue', 'stop'],
        help="""when an operation fails: 'ignore' and continue with remaining
        operations, the error is logged but does not lead to a non-zero exit code
        of the command; 'continue' works like 'ignore', but an error causes a
        non-zero exit code; 'stop' halts on first failure and yields non-zero exit
        code. A failure is any result with status 'impossible' or 'error'.
        [Default: '%(default)s']""")
    parser.add_argument(
        '--cmd', dest='_', action='store_true',
        help="""syntactical helper that can be used to end the list of global
        command line options before the subcommand label. Options taking
        an arbitrary number of arguments may require to be followed by a single
        --cmd in order to enable identification of the subcommand.""")


def strip_arg_from_argv(args, value, opt_names):
    """Strip an originally listed option (with its value) from the list cmdline args
    """
    # Yarik doesn't know better
    if args is None:
        args = sys.argv
    # remove present pbs-runner option
    args_clean = []
    skip = 0
    for i, arg in enumerate(args):
        if skip:
            # we skip only one as instructed
            skip -= 1
            continue
        if not (arg in opt_names and i < len(args) - 1 and args[i + 1] == value):
            args_clean.append(arg)
        else:
            # we need to skip this one and next one
            skip = 1
    return args_clean


def run_via_pbs(args, pbs):
    assert(pbs in ('condor',))  # for now

    # TODO: RF to support multiple backends, parameters, etc, for now -- just condor, no options
    f = NamedTemporaryFile('w', prefix='datalad-%s-' % pbs, suffix='.submit', delete=False)
    try:
        pwd = getpwd()
        logs = f.name.replace('.submit', '.log')
        exe = args[0]
        # TODO: we might need better way to join them, escaping spaces etc.  There must be a stock helper
        #exe_args = ' '.join(map(repr, args[1:])) if len(args) > 1 else ''
        exe_args = ' '.join(args[1:]) if len(args) > 1 else ''
        f.write("""\
Executable = %(exe)s
Initialdir = %(pwd)s
Output = %(logs)s
Error = %(logs)s
getenv = True

arguments = %(exe_args)s
queue
""" % locals())
        f.close()
        Runner().run(['condor_submit', f.name])
        lgr.info("Scheduled execution via %s.  Logs will be stored under %s", pbs, logs)
    finally:
        unlink(f.name)


# TODO: useful also outside of cmdline, move to support/
from os import curdir


def get_repo_instance(path=curdir, class_=None):
    """Returns an instance of appropriate datalad repository for path.
    Check whether a certain path is inside a known type of repository and
    returns an instance representing it. May also check for a certain type
    instead of detecting the type of repository.

    Parameters
    ----------
    path: str
      path to check; default: current working directory
    class_: class
      if given, check whether path is inside a repository, that can be
      represented as an instance of the passed class.

    Raises
    ------
    RuntimeError, in case cwd is not inside a known repository.
    """

    from os.path import ismount, exists, normpath, isabs
    from datalad.support.exceptions import InvalidGitRepositoryError
    from ..utils import expandpath
    from ..support.gitrepo import GitRepo
    from ..support.annexrepo import AnnexRepo

    dir_ = expandpath(path)
    abspath_ = path if isabs(path) else dir_
    if class_ is not None:
        if class_ == AnnexRepo:
            type_ = "annex"
        elif class_ == GitRepo:
            type_ = "git"
        else:
            raise RuntimeError("Unknown class %s." % str(class_))

    while not ismount(dir_):  # TODO: always correct termination?
        if exists(opj(dir_, '.git')):
            # found git dir
            if class_ is None:
                # detect repo type:
                try:
                    return AnnexRepo(dir_, create=False)
                except RuntimeError as e:
                    pass
                try:
                    return GitRepo(dir_, create=False)
                except InvalidGitRepositoryError as e:
                    raise RuntimeError("No datalad repository found in %s" %
                                       abspath_)
            else:
                try:
                    return class_(dir_, create=False)
                except (RuntimeError, InvalidGitRepositoryError) as e:
                    raise RuntimeError("No %s repository found in %s." %
                                       (type_, abspath_))
        else:
            dir_ = normpath(opj(dir_, ".."))

    if class_ is not None:
        raise RuntimeError("No %s repository found in %s" % (type_, abspath_))
    else:
        raise RuntimeError("No datalad repository found in %s" % abspath_)


from appdirs import AppDirs
from os.path import join as opj

dirs = AppDirs("datalad", "datalad.org")
