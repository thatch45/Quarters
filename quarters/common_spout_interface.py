import tornado.ioloop
import tornado.web
import json

class GlobalStatusHandler(tornado.web.RequestHandler):
    ''' handles /global_status '''

    def initialize( self, job_states ):
        self.job_states = job_states

    def get( self ):
        self.write( json.dumps( dict(self.job_states) ) )

class Spout:
    ''' webserver '''

    def __init__( self, job_states, pending_jobs, port, application ):
        ''' application is of type tornado.web.Application '''
        self.job_states = job_states
        self.pending_jobs = pending_jobs
        self.port = port
        self.application = application

    def start( self ):
        self.application.listen( self.port )
        tornado.ioloop.IOLoop.instance().start()
