#!/usr/bin/env python
# coding: UTF-8

'''This scirpt package seahub-extra to a tarball
'''

import sys
import os
import subprocess

####################
### Requires Python 3.6+
####################
if sys.version_info[0] == 2:
    print('Python 2 not supported yet. Quit now.')
    sys.exit(1)
if sys.version_info[1] < 6:
    print('Python 3.6 or above is required. Quit now.')
    sys.exit(1)

outputdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(outputdir)

def highlight(content, is_error=False):
    '''Add ANSI color to content to get it highlighted on terminal'''
    if is_error:
        return '\x1b[1;31m%s\x1b[m' % content
    else:
        return '\x1b[1;32m%s\x1b[m' % content

def error(msg=None, usage=None):
    if msg:
        print(highlight('[ERROR] ') + msg)
    if usage:
        print(usage)
    sys.exit(1)

def run(cmdline, cwd=None, env=None, suppress_stdout=False, suppress_stderr=False):
    '''Like run_argv but specify a command line string instead of argv'''
    with open(os.devnull, 'w') as devnull:
        if suppress_stdout:
            stdout = devnull
        else:
            stdout = sys.stdout

        if suppress_stderr:
            stderr = devnull
        else:
            stderr = sys.stderr

        proc = subprocess.Popen(cmdline,
                                cwd=cwd,
                                stdout=stdout,
                                stderr=stderr,
                                env=env,
                                shell=True)
        return proc.wait()

def create_tarball(tarball_name):
    '''call tar command to generate a tarball'''

    seahub_extra_dir = 'seahub_extra'

    ignored_patterns = [
        # common ignored files
        '*.pyc',
        '*~',
        '*#',

        # seahub-extra
        '*.md',
        '*.markdown',
        '*.gz',
        '*.git*',
        '*/thirdparts*',
        '*/scripts*',
        os.path.join(seahub_extra_dir, 'pay*'),
        os.path.join(seahub_extra_dir, 'plan*'),
        os.path.join(seahub_extra_dir, 'tagging*'),
        os.path.join(seahub_extra_dir, 'trialaccount*'),
    ]

    excludes_list = [ '--exclude=%s' % pattern for pattern in ignored_patterns ]
    excludes_list.append('--exclude-vcs')
    excludes = ' '.join(excludes_list)

    tar_cmd = 'tar czvf %(tarball_name)s seahub-extra %(excludes)s' \
              % dict(tarball_name=tarball_name,
                     seahub_extra_dir=seahub_extra_dir,
                     excludes=excludes)

    d = os.path.dirname
    seahub_extra_parent_dir = d(d(d(os.path.abspath(__file__))))
    if run(tar_cmd, cwd=seahub_extra_parent_dir) < 0:
        error('failed to generate the tarball')

    print('---------------------------------------------')
    print('output is %s' % tarball_name)
    print('---------------------------------------------')

def compile_po():
    d = os.path.dirname
    topdir = d(d(os.path.abspath(__file__)))
    for dirpath, dirnames, filenames in os.walk(os.path.join(topdir, 'seahub_extra')):
        for name in filenames:
            if not name.endswith('.po'):
                continue

            src = os.path.join(dirpath, name)
            dst = os.path.join(dirpath, name.replace('.po', '.mo'))
            cmd = 'msgfmt -o %s %s' % (dst, src)
            print('running ', cmd)
            if os.system(cmd) != 0:
                raise RuntimeError('failed to run ' + cmd)

def main():
    compile_po()
    create_tarball(os.path.join(outputdir, 'seahub-extra.tar.gz'))

if __name__ == '__main__':
    main()
