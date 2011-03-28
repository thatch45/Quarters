import tornado.ioloop
import tornado.web
from quarters.protocol import response_global_status, response_list_of_packages, response_package, response_build_log, response_job, response_pkgsrc

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

def start_builder_web( job_states, config ):
    application = tornado.web.Application( [
        ( r"/global_status", GlobalStatusHandler, dict( job_states=job_states ) ),
        ( r"/([0-9a-f-]+)/list_of_packages", ListOfPackagesHandler, dict( root=config[ 'builder_root' ] ) ),
        ( r"/([0-9a-f-]+)/(.*.pkg.tar.xz)", PackageHandler, dict( root=config[ 'builder_root' ] ) ),
        ( r"/([0-9a-f-]+)/build_log", BuildLogHandler, dict( root=config[ 'builder_root' ] ) ),
    ] )

    ws = Spout( int (config[ 'builder_port' ] ), application )
    ws.start()

class JobHandler(tornado.web.RequestHandler):
    ''' handles /job '''
    def initialize( self, pending_jobs ):
        self.pending_jobs = pending_jobs

    def get( self ):
        self.write( response_job( self.pending_jobs ) )

class PkgSrcHandler( tornado.web.RequestHandler ):
    ''' handles /ujid/ujid.src.tar.gz '''
    def initialize( self, root ):
        self.root = root

    ''' TODO pkgname parameter should be the same as ujid so we could remove it in the future '''
    def get( self, ujid, pkgname ):
        self.set_header( 'Content-Type', 'application/octet-stream' )
        self.write( response_pkgsrc( self.root, ujid, pkgname ) )

def start_master_web( job_states, pending_jobs, config ):
    application = tornado.web.Application( [
     ( r"/global_status", GlobalStatusHandler, dict( job_states=job_states ) ),
     ( r"/job", JobHandler, dict( pending_jobs=pending_jobs ) ),
     ( r"/([0-9a-f-]+)/list_of_packages", ListOfPackagesHandler, dict( root=config[ 'master_root' ] ) ),
     ( r"/([0-9a-f-]+)/(.*.pkg.tar.xz)", PackageHandler, dict( root=config[ 'master_root' ] ) ),
     ( r"/([0-9a-f-]+)/build_log", BuildLogHandler, dict( root=config[ 'master_root' ] ) ),
     ( r"/([0-9a-f-]+)/(.*.src.tar.gz)", PkgSrcHandler, dict( root=config[ 'master_root' ] ) ),
    ] )

    ws = Spout( config[ 'master_port' ], application )
    ws.start()
