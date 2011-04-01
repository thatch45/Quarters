import tornado.ioloop
import tornado.web
from quarters.protocol import response_global_status, response_package, response_build_log, response_job, response_pkgsrc

class GlobalStatusHandler(tornado.web.RequestHandler):
    ''' handles /global_status '''
    def initialize( self, local_state ):
        self.local_state = local_state

    def get( self ):
        self.write( response_global_status( self.local_state ) )

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

def start_builder_web( local_state, config ):
    application = tornado.web.Application( [
        ( r"/global_status", GlobalStatusHandler, dict( local_state=local_state ) ),
        ( r"/([0-9a-f-]+)/(.*.pkg.tar.xz)", PackageHandler, dict( root=config[ 'builder_root' ] ) ),
        ( r"/([0-9a-f-]+)/build_log", BuildLogHandler, dict( root=config[ 'builder_root' ] ) ),
    ] )

    ws = Spout( int (config[ 'builder_port' ] ), application )
    ws.start()

class JobHandler(tornado.web.RequestHandler):
    ''' handles /job '''
    def initialize( self, local_state ):
        self.local_state = local_state

    def get( self ):
        self.write( response_job( self.local_state ) )

class PkgSrcHandler( tornado.web.RequestHandler ):
    ''' handles /ujid/ujid.src.tar.gz '''
    def initialize( self, root ):
        self.root = root

    def get( self, ujid ):
        self.set_header( 'Content-Type', 'application/octet-stream' )
        self.write( response_pkgsrc( self.root, ujid ) )

def start_master_web( local_state, config ):
    application = tornado.web.Application( [
     ( r"/global_status", GlobalStatusHandler, dict( local_state=local_state ) ),
     ( r"/job", JobHandler, dict( local_state=local_state ) ),
     ( r"/([0-9a-f-]+)/(.*.pkg.tar.xz)", PackageHandler, dict( root=config[ 'master_root' ] ) ),
     ( r"/([0-9a-f-]+)/build_log", BuildLogHandler, dict( root=config[ 'master_root' ] ) ),
     ( r"/([0-9a-f-]+)/.*.src.tar.gz", PkgSrcHandler, dict( root=config[ 'master_root' ] ) ),
    ] )

    ws = Spout( config[ 'master_port' ], application )
    ws.start()
