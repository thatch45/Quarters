import tornado.ioloop
import tornado.web
import json
import glob
from quarters.utils import sha256sum_file

class GlobalStatusHandler(tornado.web.RequestHandler):
    ''' handles /global_status '''

    def initialize( self, job_states ):
        self.job_states = job_states

    def get( self ):
        self.write( json.dumps( dict(self.job_states) ) )

class ListOfPackagesHandler(tornado.web.RequestHandler):
    def get( self, ujid ):
        results = glob.glob( '/var/tmp/quarters/' + str( ujid ) + '/*.pkg.tar.xz' )
        results = list( map( lambda x: x.split('/')[-1], results ) )
        temp = [{ 'pkgname' : i, 'sha256sum' : sha256sum_file( '/var/tmp/quarters/' + str( ujid ) + '/' + i ) } for i in results]
        self.write( json.dumps( temp ) )

class PackageHandler(tornado.web.RequestHandler):
    def get( self, ujid, pkg ):
        self.set_header('Content-Type', 'application/octet-stream')
        pkgul = '/var/tmp/quarters/' + str( ujid ) + '/' + str( pkg )
        with open( pkgul, 'rb' ) as fp:
            self.write( fp.read() )

class BuildLogHandler(tornado.web.RequestHandler):
    def get( self, ujid ):
        self.set_header('Content-Type', 'text/plain')
        build_log_path = '/var/tmp/quarters/' + str( ujid ) + '/build_log'
        with open( build_log_path, 'rb' ) as fp:
            self.write( fp.read() )

class Spout:
    ''' webserver '''

    def __init__( self, port, application ):
        ''' application is of type tornado.web.Application '''
        self.port = port
        self.application = application

    def start( self ):
        self.application.listen( self.port )
        tornado.ioloop.IOLoop.instance().start()
