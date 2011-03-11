import tornado.web

from quarters.common_spout_interface import Spout, GlobalStatusHandler, ListOfPackagesHandler, PackageHandler, BuildLogHandler

class JobHandler(tornado.web.RequestHandler):
    ''' handles /job '''

    def initialize( self, pending_jobs ):
        self.pending_jobs = pending_jobs

    def get( self ):
        try:
            jd = self.pending_jobs.get_nowait()
            self.write( jd.dump_json() )
        except:
            self.write( 'NOJOBS' )

def start_master_web( job_states, pending_jobs, port ):
    application = tornado.web.Application( [
     ( r"/global_status", GlobalStatusHandler, dict( job_states=job_states ) ),
     ( r"/job", JobHandler, dict( pending_jobs=pending_jobs ) ),
     ( r"/([0-9]+)/list_of_packages", ListOfPackagesHandler ),
     ( r"/([0-9]+)/(.*.pkg.tar.xz)", PackageHandler ),
     ( r"/([0-9]+)/build_log", BuildLogHandler ),
    ] )

    ws = Spout( port, application )
    ws.start()
