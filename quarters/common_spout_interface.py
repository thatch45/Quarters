import tornado.ioloop
import tornado.web
from quarters.protocol import response_global_status, response_list_of_packages, response_package, response_build_log

class GlobalStatusHandler(tornado.web.RequestHandler):
    ''' handles /global_status '''

    def initialize( self, job_states ):
        self.job_states = job_states

    def get( self ):
        self.write( response_global_status( self.job_states ) )

class ListOfPackagesHandler(tornado.web.RequestHandler):
    ''' handles /ujid/list_of_packages '''
    def initialize( self, root ):
        self.root = root

    def get( self, ujid ):
        self.write( response_list_of_packages( self.root, ujid ) )

class PackageHandler(tornado.web.RequestHandler):
    ''' handles /ujid/*.pkg.tar.xz '''
    def initialize( self, root ):
        self.root = root

    def get( self, ujid, pkg ):
        self.set_header('Content-Type', 'application/octet-stream')
        self.write( response_package( self.root, ujid, pkg ) )

class BuildLogHandler(tornado.web.RequestHandler):
    ''' handles /ujid/build_log '''
    def initialize( self, root ):
        self.root = root

    def get( self, ujid ):
        self.set_header('Content-Type', 'text/plain')
        self.write( response_build_log( self.root, ujid ) )

class Spout:
    ''' webserver '''

    def __init__( self, port, application ):
        ''' application is of type tornado.web.Application '''
        self.port = port
        self.application = application

    def start( self ):
        self.application.listen( int( self.port ) )
        tornado.ioloop.IOLoop.instance().start()
