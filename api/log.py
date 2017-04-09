# -*- coding: utf-8 -*-
import logging
import logging.handlers
import traceback

__author__ = "y.nawachi"
__status__ = "development"
__version__ = "0.1.1"
__date__ = "2016-04-01"


def logging_args(logger, args):
    for arg in vars(args):
        val = getattr(args, arg)

        if type(val) == list and len(val) > 0:
            if type(val[0]) == unicode:
                val = ', '.join(val).encode('utf-8')
            else:
                val = ', '.join(val)

        logger.info('arguments %s = %s' % (arg, val))


def logging_exception(logger, exception):
    logger.error('Catch exception: {}: {}\n{}'.format(type(exception), exception, traceback.format_exc()))


def get_logger(name, level_stream='info', logfile=None, level_file=None, rotate_when='D', rotate_count=7):
    log_level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    if not level_stream or not log_level[level_stream]:
        level_stream = 'info'

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s - %(levelname)s - %(message)s')

    sh = logging.StreamHandler()
    sh.setLevel(log_level[level_stream])
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    if logfile:
        if not level_file or not log_level[level_file]:
            level_file = level_stream

        fh = logging.FileHandler(logfile)
        fh.setLevel(log_level[level_file])
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
