import tornado.ioloop
import tornado.web
import json
import glob
from quarters.utils import sha256sum_file
import os

class GlobalStatusHandler(tornado.web.RequestHandler):
    ''' handles /global_status '''

    def initialize( self, job_states ):
        self.job_states = job_states

    def get( self ):
        self.write( json.dumps( dict(self.job_states) ) )

class ListOfPackagesHandler(tornado.web.RequestHandler):
    def initialize( self, root ):
        self.root = root

    def get( self, ujid ):
        ujid_path = os.path.join( self.root, str( ujid ) )
        results = glob.glob( ujid_path + '/*.pkg.tar.xz' )
        results = list( map( lambda x: x.split('/')[-1], results ) )
        temp = [{ 'pkgname' : i, 'sha256sum' : sha256sum_file( ujid_path + '/' + i ) } for i in results]
        self.write( json.dumps( temp ) )

class PackageHandler(tornado.web.RequestHandler):
    def initialize( self, root ):
        self.root = root

    def get( self, ujid, pkg ):
        ujid_path = os.path.join( self.root, str( ujid ) )
        self.set_header('Content-Type', 'application/octet-stream')
        pkgul = ujid_path + '/' + str( pkg )
        with open( pkgul, 'rb' ) as fp:
            self.write( fp.read() )

class BuildLogHandler(tornado.web.RequestHandler):
    def initialize( self, root ):
        self.root = root

    def get( self, ujid ):
        ujid_path = os.path.join( self.root, str( ujid ) )
        self.set_header('Content-Type', 'text/plain')
        build_log_path = ujid_path + '/build_log'
        with open( build_log_path, 'rb' ) as fp:
            self.write( fp.read() )

class Spout:
    ''' webserver '''

    def __init__( self, port, application ):
        ''' application is of type tornado.web.Application '''
        self.port = port
        self.application = application

    def start( self ):
        self.application.listen( int( self.port ) )
        tornado.ioloop.IOLoop.instance().start()
