'''
The core quarters module is used to create the daemon functional objects,
these objects are all it takes to fire up the entire builders and masters.
'''
import optparse
import sys
import os

def daemonize():
    '''
    Daemonize a process
    '''
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError as e:
        print("fork #1 failed: %d (%s)" % (e.errno, e.strerror), file=sys.stderr)
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/") 
    os.setsid() 
    os.umask(0o22)

    # do second fork
    try: 
        pid = os.fork() 
        if pid > 0:
            # print "Daemon PID %d" % pid 
            sys.exit(0) 
    except OSError as e:
        print("fork #2 failed: %d (%s)" % (e.errno, e.strerror), file=sys.stderr)
        sys.exit(1) 

    dev_null = file('/dev/null','rw') 
    os.dup2(dev_null.fileno(), sys.stdin.fileno()) 
    os.dup2(dev_null.fileno(), sys.stdout.fileno()) 
    os.dup2(dev_null.fileno(), sys.stderr.fileno()) 

class Master:
    '''
    The master quarters server
    '''
    def __init__(self):
        cli_opts = self.__cli_parser()
        self.opts = quarters.config.read(cli_opts['config'])
        if not cli_opts['foreground']:
            daemonize()

    def __cli_parser(self):
        '''
        Parses the command line arguments.
        '''
        parser = optparse.OptionParser()
        parser.add_option('-c',
                '--config', 
                dest='config',
                default='/etc/quarters/master.conf',
                help='The location of the master configuration file;'\
                    + ' default=/etc/quarters/master.conf')

        parser.add_option('--foreground',
                dest='foreground',
                default=False,
                action='store_true',
                help='Set this flag to run the quarters master in the'\
                    + ' foreground, this is helpful when debugging problems'\
                    + ' with the server')

        options, args = parser.parse_args()

        opts = {'config': options.config,
                'foreground': option.foreground}

        return opts

    def start_quarters_master(self):
        '''
        This method executes the quarters master server.
        '''
        if not self.opts['disable_https']:
            quarters.https.partner_https(
                    self.opts['listen_addr'],
                    self.opts['port'],
                    self.opts['https_root'],
                    self.opts['pemfile'])


class Builder:
    '''
    The quarters builder
    '''
    def __init__(self):
        cli_opts = self.__cli_parser()
        self.opts = quarters.config.read(cli_opts['config'])
        if not cli_opts['foreground']:
            daemonize()

    def __cli_parser(self):
        '''
        Parses the command line arguments.
        '''
        parser = optparse.OptionParser()
        parser.add_option('-c',
                '--config', 
                dest='config',
                default='/etc/quarters/builder.conf',
                help='The location of the builder configuration file;'\
                    + ' default=/etc/quarters/builder.conf')
        parser.add_option('--foreground',
                dest='foreground',
                default=False,
                action='store_true',
                help='Set this flag to run the quarters builder in the'\
                    + ' foreground, this is helpful when debugging problems'\
                    + ' with the server')

        options, args = parser.parse_args()

        opts = {'config': options.config,
                'foreground': option.foreground}

        return opts

    def start_quarters_builder(self):
        '''
        This method executes the quarters master server.
        '''
        if not self.opts['disable_https']:
            quarters.https.partner_https(
                    self.opts['listen_addr'],
                    self.opts['port'],
                    self.opts['https_root'],
                    self.opts['pemfile'])
