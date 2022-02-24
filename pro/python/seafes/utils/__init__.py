#!coding: UTF_8

import os
import sys
import logging
import subprocess

from seafes.config import seafes_config

def _expand(v):
    return v[0] if isinstance(v, list) else v

def get_result_set_hits(result):
    hits = result.__getattr__('hits')
    if isinstance(hits, dict):
        hits = hits['hits']

    # In ES 1.4.0 the returned fields values are like {field1: [value1], field2: [value2], ...}
    for entry in hits:
        fields = entry.get('fields', {})
        for k, v in fields.copy().items():
            fields[k] = _expand(v)

    return hits


def run(argv, cwd=None, env=None, suppress_stdout=False, suppress_stderr=False):
    """Run a program and wait it to finish, and return its exit code. The
    standard output of this program is suppressed.
    """
    with open(os.devnull, 'w') as devnull:
        if suppress_stdout:
            stdout = devnull
        else:
            stdout = sys.stdout

        if suppress_stderr:
            stderr = devnull
        else:
            stderr = sys.stderr

        proc = subprocess.Popen(argv,
                                cwd=cwd,
                                stdout=stdout,
                                stderr=stderr,
                                env=env)

        return proc.wait()


def do_dict_config(level, stream):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'seafes': {
                'format': '[%(asctime)s] %(message)s',
            },
        },
        'handlers': {
            'seafes': {
                'level': level,
                'class': 'logging.StreamHandler',
                'stream': stream,
                'formatter': 'seafes',
            },
        },
        'loggers': {
            'seafes': {
                'handlers': ['seafes'],
                'level': level,
                'propagate': False
            },
        }
    }

    # Make sure that dictConfig is available
    # This was added in Python 2.7/3.2
    try:
        from logging.config import dictConfig
    except ImportError:
        from django.utils.dictconfig import dictConfig

    dictConfig(LOGGING)

def init_logging(args):
    level = args.loglevel

    if level == 'debug':
        level = logging.DEBUG
    elif level == 'info':
        level = logging.INFO
    elif level == 'warning':
        level = logging.WARNING
    else:
        if seafes_config.debug:
            level = logging.DEBUG
        else:
            level = logging.INFO

    try:
        # set boto log level
        import boto
        boto.log.setLevel(logging.WARNING)
    except:
        pass

    # do_dict_config(level, args.logfile)

    kw = {
       #'format': '[%(asctime)s] %(message)s',
        'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)s %(funcName)s: %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': level,
        'stream': args.logfile
    }

    logging.basicConfig(**kw)
    logging.getLogger('oss_util').setLevel(logging.WARNING)
    logging.getLogger('elasticsearch').setLevel(logging.ERROR)
    logging.getLogger('elasticsearch.trace').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    if seafes_config.debug:
        logging.debug('debug flag turned on')
