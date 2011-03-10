import tornado.ioloop
import tornado.web
import json

import glob

class GlobalStatusHandler(tornado.web.RequestHandler):
    def initialize( self, job_states ):
        self.job_states = job_states
    def get( self ):
        self.write( json.dumps( dict(self.job_states) ) )

class JobHandler(tornado.web.RequestHandler):
    ''' return new job, or return nothing to be done '''
    def initialize( self, pending_jobs ):
        self.pending_jobs = pending_jobs
    def get( self ):
        try:
            jd = self.pending_jobs.get_nowait()
            self.write( jd.dump_json() )
        except:
            self.write( 'NOJOBS' )

class Spout:
    ''' webserver for the builder '''

    def __init__( self, job_states, pending_jobs, config ):
        self.job_states = job_states
        self.pending_jobs = pending_jobs
        self.port = config['master_port']

    def start( self ):
        application = tornado.web.Application( [
            ( r"/global_status", GlobalStatusHandler, dict( job_states=self.job_states ) ),
            ( r"/job", JobHandler, dict( pending_jobs=self.pending_jobs ) ),
        ] )

        application.listen( self.port )
        tornado.ioloop.IOLoop.instance().start()
