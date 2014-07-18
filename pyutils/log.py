######################################################################################
# Python's logging libraries are overly complicated for daily use.
# 
# This library simplifies things by assuming that your application:
#
# * Wants to write all log messages to a single log file or to stdout.
# * Only wants to toggle between INFO and DEBUG level logging.
# 
# Sample usage:
#
# import pyUtils.log
# import signal
# pyUtils.log.setup_logging( "/var/log/myapp.log" )
# # reopen logfile if we catch a sighup (e.g. from logrotate)
# signal.signal( signal.SIGHUP, pyUtils.log.reopen_logfile )
# logging.info( "myapp started" )
#
######################################################################################

import logging
import time
import sys
import os

__log_setup_complete = False
__logfile_handler = None
__logfile_name    = None
__log_format      = "%(asctime)s %(levelname)-5s [%(process)d/%(threadName)-10s]: %(message)s" 
__sigusr_handler  = None


class log_prepend(logging.Filter):
    """
    This is a log filter which prepends contextual information into the log.

    Original use case is for MAC Addresses so greping is easier.
    
    To change value use:
      logging.log(99, 'value')
    To reset value use:
      logging.log(99, None)
    """
    def __init__(self, default='00-00-00', length=8, loglevel=99):
        self.default_value = default
        self.log_level = loglevel
        self.length = -length

        self.log_prepend_value = default
    
    def filter(self, record):
        if record.levelno == self.log_level:
          if record.msg == None:
            self.log_prepend_value = self.default_value         
          else:
            self.log_prepend_value = record.msg[self.length:]
          return False

        try:
          new_msg = self.log_prepend_value + " | " + record.msg.__str__()
        except:
          new_msg = self.log_prepend_value + " | " + record.msg.__repr__()
        new_msg = new_msg.replace("\n", "\n" + self.log_prepend_value + " | ")
        record.msg = new_msg
        return True


class sigusr_log_handler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        self.sigusr_timeout  = 0
        logging.Handler.__init__(self, level)

    def handle(self, record):
        '''This function is called every time a log record is encountered'''
        if ( (self.sigusr_timeout != 0) and (self.sigusr_timeout <= time.time()) ):
          self.sigusr_timeout = 0
          logging.debug( "Stopping DEBUG Logging - SIGUSR1 Expired" )
          loglevel = logging.INFO
          rootLogger = logging.getLogger( '' )
          rootLogger.setLevel( loglevel )
          rootLogger.removeHandler( self )


def setup_logging( logfile=None, verbose=False, debug=False, enable_sigusr=False, prepend_mac=False ): 
    '''Initialize the python logging classes with some reasonable defaults.
        logfile: the file where log messages will be written
        verbose: if true, log messages will also be sent to stdout
        debug: if true, log at priority DEBUG (default is INFO).

        After calling this function your application can write log messages via:

        logging.<loglevel>( "foo" )

        assuming you've done "import logging" somewhere along the way.
'''

    global __logfile_handler, __logfile_name, __log_setup_complete
    loglevel = logging.INFO
    if debug:
        loglevel = logging.DEBUG

    rootLogger = logging.getLogger('')
    rootLogger.setLevel( loglevel )

    if logfile:
        __logfile_name = logfile
        __logfile_handler = logging.FileHandler( logfile )
        __logfile_handler.setFormatter( logging.Formatter(__log_format) )
        rootLogger.addHandler( __logfile_handler )

        if verbose:
            # also log to stdout
            console = logging.StreamHandler( sys.stdout )
            console.setFormatter( logging.Formatter(__log_format))
            logging.getLogger('').addHandler( console )

        if prepend_mac:
           rootLogger.addFilter(log_prepend( default='00-00-00', length=8, loglevel=99 ))

    else:
        logging.basicConfig(level=loglevel, format=__log_format)

    if enable_sigusr:
        import signal
        signal.signal(signal.SIGUSR1, __SIGUSR_Handler)

    __log_setup_complete = True
    logging.debug( "debug logging enabled" )


def reopen_logfile(signum=None,frame=None):
    '''Call me after rotating logs to reopen your logfile. Suitable
    for using as a signal handler (e.g. after logrotation).'''
    global __logfile_handler, __logfile_name

    if not logging_is_setup():
        abort( "must call setup_logging() before reopen_logfile()" )

    rootLogger = logging.getLogger('')
    rootLogger.removeHandler(__logfile_handler)
    __logfile_handler = logging.FileHandler( __logfile_name )
    __logfile_handler.setFormatter( logging.Formatter(__log_format) )
    rootLogger.addHandler( __logfile_handler )
    logging.info( "started new logfile" )


def logging_is_setup():
    '''Returns True if setup_logging() has been called; false otherwise.'''
    return __log_setup_complete


def __SIGUSR_Handler(signum, frame):
    import signal
    if signum == signal.SIGUSR1:
        global __sigusr_handler
        
        # If we haven't already created one, create it
        if __sigusr_handler == None:
            __sigusr_handler = sigusr_log_handler()

        # set the timeout
        __sigusr_handler.sigusr_timeout = time.time() + (30*60) # add 30 minutes

        loglevel = logging.DEBUG
        rootLogger = logging.getLogger('')
        rootLogger.setLevel( loglevel )
        rootLogger.addHandler( __sigusr_handler )

        logging.debug( "SIGUSR1 Encountered - Begin DEBUG Logging" )


def abort( message ):
    '''Log a fatal() message and exit the current process.

    If you have cleanup to do, do it before calling me!  Calling this
    function also won't clean up pidfiles or anything else, under the
    assumption that we'd like someone to be able to manually clean up
    or inspect the state of the app later on.'''
    logging.fatal( message )
    os._exit(1)

