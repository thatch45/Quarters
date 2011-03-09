import tornado.ioloop
import tornado.web
import json

import glob

class GlobalStatusHandler(tornado.web.RequestHandler):
    def initialize( self, job_states ):
        self.job_states = job_states
    def get( self ):
        self.write( json.dumps( dict(self.job_states) ) )

class ListOfPackagesHandler(tornado.web.RequestHandler):
    def get( self, ujid ):
        results = glob.glob( '/var/tmp/quarters/' + str( ujid ) + '/*.pkg.tar.xz' )
        results = list( map( lambda x: x.split('/')[-1], results ) )
        self.write( json.dumps( list(results) ) )

class JobHandler(tornado.web.RequestHandler):
    def get( self, ujid, pkg ):
        self.set_header('Content-Type', 'application/octet-stream')
        pkgul = '/var/tmp/quarters/' + str( ujid ) + '/' + str( pkg )
        with open( pkgul, 'rb' ) as fp:
            self.write( fp.read() )

class Spout:
    ''' webserver for the builder '''

    def __init__( self, job_states, port=8888 ):
        self.job_states = job_states
        self.port = port

    def start( self ):
        application = tornado.web.Application( [
            ( r"/global_status", GlobalStatusHandler, dict( job_states=self.job_states ) ),
            ( r"/([0-9]+)/list_of_packages", ListOfPackagesHandler ),
            ( r"/([0-9]+)/(.*.pkg.tar.xz)", PackageHandler ),
        ] )

        application.listen( self.port )
        tornado.ioloop.IOLoop.instance().start()
