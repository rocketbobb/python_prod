#!/usr/bin/python3
# ######################################################################
#
# Program:  logging.py
#
# Purpose:  logging setups and initializes pythons logging subsystem
#           supports console and logfile recording
#           formats logfile message records according to group standard
#           datetime is ISO8601 enhanced
#           uses runid to uniquely track each job, includes runid in log msg
#
# ######################################################################

"""
Example:
    >>> import lib.logger import LoggerPlus
    >>> import logging
    >>> loggerpp = LoggerPlus(logdir='logs')
    >>> logging.info('Test message')
"""

# Import Core libraries
import os
import sys
import logging
import datetime

# Import Internal libraries
from lib import utils

try:
    import colorlog
    HAVE_COLORLOG = True
except ImportError:
    HAVE_COLORLOG = False

class LoggerPlus:

    # Loglevels range from 0 to 50 with 0-NOTSET to 50-Critical
    DEFAULT_LOGLEVEL = 'logging.INFO'
    DEFAULT_LOGDIR = 'logs'

    def __init__(self, logdir=LoggerPlus.DEFAULT_LOGDIR, loglevel=LoggerPlus.DEFAULT_LOGLEVEL, runid=None):
        """ Set up logging (console and logfile).

        When the logger class is initialized, it creates a logfile name, runid and the target logs direction, 
        if missing. The logfile name encodes creation date, time, and runid. For example "20181115-153559.txt". 
        All messages with a log level of at least "warn" are also forwarded to the console.

        Args:
            logdir (str): path of the directory where to store the log files. Both a relative or an absolute path may be 
            specified. If a relative path is specified, it is interpreted relative to the working directory.
            If no directory is given, the logs are written to a folder called "logs" in the working directory. 
        """
        if runid is None:
            self.runid = int(11)
        else:
            self.runid = runid
        logging.debug(self.runid)

        if self.loglevel <= 10:
            pass
            #print('Running ' + utils.get_function_name() + '(' + str(utils.get_function_parameters_and_values()) +')')
 
        # TODO colored logs
        #coloredlogs.install(level='DEBUG')

        #
        # create logger  ( logger.propagate = False )
        # also add nullhandler to prevent exception on addhandler test
        #
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        self.logger = logging.getLogger()       # setting instance logger
        self.logger.setLevel(self.loglevel)     # setting logger loglevel

        # Now call setLogger method
        self.setLogger(logdir=logdir,loglevel=loglevel)

        ##logging.debug(self.logfile)
        ##self.logger = logging.getLogger()   # getting root logger
        ##self.logger.setLevel(self.loglevel)

    def logDir(self, logdir=None):
        logging.debug('Running ' + utils.get_function_name() + '(' + str(utils.get_function_parameters_and_values()) +')')
        if logdir is not None:
            self.logdir = logdir

        if utils.isNotBlank(self.logdir):
        # TODO rnb ( except can't write) create dir for logfiles
        # TODO rnb make sure logdir is a directory
            if self.logdir == '.':
                self.logdir = ''
            else:
                self.logdir = logdir.strip().rstrip('\\/')
                if not os.path.exists(logdir):
                    try:
                        os.mkdir(logdir)
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise OSError("Can't create destinataion directory ($s)!" % (logdir))
                        pass
        return logdir
    
    def setLogger(self, pgmname='-blank-', logdir=None, loglevel=None):
        # testing to see if setter called with logdir or loglevel changes
        if loglevel is not None:
            self.loglevel = self.level_str_to_int(loglevel)
        if logdir is not None:
            self.logdir = logdir
            self.logfile = self.logDir(self.logdir) + '/' + pgmname + '_' + self.runid + '.log'

        # logging code outside of logger system, if debug, print to console
        if self.loglevel <= 10:
            pass
            #print('Running ' + utils.get_function_name() + '(' + str(utils.get_function_parameters_and_values()) +')')
        
        # creating console handler and set level
        #
        ch = logging.StreamHandler(sys.stderr)  # sys.stderr
        ch.setLevel(self.loglevel)
#        ch_formatter = logging.Formatter('% (name) - 12s: % (levelname) - 8s % (message)s')
        ch_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

        ch.setFormatter(ch_formatter)
        #logging.getLogger().addHandler(ch)
        #logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().setLevel(self.loglevel)
        # creating file handler and set level if directory provided
        #
        fhtest=False
        chtest=False
        for handlers in self.logger.handlers:
            if isinstance(handlers,logging.FileHandler): 
                fhtest=True
                self.logger.removeHandler(handlers)
            if isinstance(handlers,logging.StreamHandler):
                chtest=True

        if self.logfile != None:
            fh = logging.FileHandler(self.logfile)
            fh_formatter = logging.Formatter('%(asctime)s %(levelname)s' + ' [' + 'pgmname' + '] '
                        + self.runid + ' %(module)s %(lineno)s [%(message)s]', datefmt='%Y-%m-%dT%H:%M:%S%z')
            fh_formatter.default_msec_format = '%s.%03d'
            fh.setFormatter(fh_formatter)
            self.logger.addHandler(fh)
            fh.setLevel(self.loglevel)
        if not chtest:
            print(''''ddddddddddddddd''')
            # creating console formatter (sys.stderr)
            # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch_formatter = logging.Formatter('% (name) - 12s: % (levelname) - 8s % (message)s')
            """ 
            # TODO, add color support for log message level
            format_str = '%(asctime)s - %(levelname)-8s - %(message)s'
            date_format = '%Y-%m-%d %H:%M:%S
            if HAVE_COLORLOG:
                cformat = '%(log_color)s' + format_str
                colors = {'DEBUG': 'reset',
                        'INFO': 'reset',
                        'WARNING': 'bold_yellow',
                        'ERROR': 'bold_red',
                        'CRITICAL': 'bold_red'}
                ch_formatter = ColoredFormatter(cformat, date_format,log_colors=colors)
            """
            # add formatter to ch
            ch.setFormatter(ch_formatter)
            # add ch to logger, not sure about multiple
            self.logger.addHandler(ch)
            ch.setLevel(self.loglevel)
        # debug info for the logging framework itself
        logging.debug(f'logging setup complete, loglevel:[{loglevel}]')
        logging.debug('logfilename [{}]'.format(self.logfile))
        return

    def level_str_to_int(self, arg):
        #logging.debug('Running ' + utils.get_function_name() + '(' + str(utils.get_function_parameters_and_values()) +')')
        """
        remapping logging.<level> into level as per logging package requirements
        TODO validate range, may be a simpler way
        """
        if isinstance(arg, str):
            switcher = {
                'NOTSET': 0,
                'DEBUG':  10,
                'INFO':   20,
                'WARNING': 30,
                'WARN': 30,
                'ERROR': 40,
                'CRITICAL': 50,
            }
            level = switcher.get(arg, 20)
        elif isinstance(arg, int):
            levels = [0, 10, 20, 30, 40, 50]
            if arg not in levels:
                logging.warning('Invalid loglevel ' + utils.get_function_name() + '(' + str(
                    utils.get_function_parameters_and_values()) + ')')
            level = arg
        return level        

    main_logger = LoggerPlus(glbs=main_env.getGlobals(), logdir=main_env.getGlobal('LOG_DIR'))
    
    # save logfile name
    main_env.setGlobal('logfile', main_logger.logfile)
    
    # setting loglevel to debug
    main_logger.setLogger(loglevel=logging.DEBUG)

    logging.debug('Logging subsystem initialized')
    logging.debug(f'env globals [{main_env.getGlobals()}]')

    # changing logdir to /tmp
    logging.debug('Changing log records to logs1 directory')
    main_logger.logDir(logdir='logs1')
    main_logger.setLogger(logdir='logs1')
    logging.debug('Now writing logfiles to logs1 directory')

    # end of main()

if __name__ == '__main__':
    pgmname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    print(f'\n**** Running main Program [{pgmname}]\n')

    sys.path.append('.')
    main_env = set_env.Inv_Env()

    main()
    logging.info('End of logging subsystem test')
    print(f'\n**** Main clean exit [{pgmname}]\n')
    # end of main