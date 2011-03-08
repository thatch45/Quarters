import tornado.ioloop
import tornado.web

class GlobalStatusHandler(tornado.web.RequestHandler):
    def initialize( self, job_states ):
        self.job_states = job_states
    def get( self ):
        self.write( str( self.job_states ) )

class Spout:
    ''' webserver for the builder '''

    def __init__( self, job_states, port=8888 ):
        self.job_states = job_states

    def start( self ):
        application = tornado.web.Application( [
            ( r"/global_status", GlobalStatusHandler, dict( job_states=self.job_states ) ),
        ] )

        application.listen( 8888 )
        tornado.ioloop.IOLoop.instance().start()
