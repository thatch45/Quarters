import tornado.web
import os

from quarters.common_spout_interface import Spout, GlobalStatusHandler, ListOfPackagesHandler, PackageHandler, BuildLogHandler

class JobHandler(tornado.web.RequestHandler):
    ''' handles /job '''

    def initialize( self, pending_jobs ):
        self.pending_jobs = pending_jobs

    def get( self ):
        print( 'in job handler' )
        try:
            jd = self.pending_jobs.get_nowait()
            self.write( jd.dump_json() )
        except:
            self.write( 'NOJOBS' )

class PkgSrcHandler( tornado.web.RequestHandler ):
    def initialize( self, root ):
        self.root = root

    def get( self, ujid, pkgname ):
        print( 'in pkgsrc_handler' )
        self.set_header('Content-Type', 'application/octet-stream')

        ujid_path = os.path.join( self.root, str( ujid ) )
        pkgsrc_path = os.path.join( ujid_path, pkgname )

        with open( pkgsrc_path, 'rb' ) as fp:
            self.write( fp.read() )

def start_master_web( job_states, pending_jobs, config ):
    application = tornado.web.Application( [
     ( r"/global_status", GlobalStatusHandler, dict( job_states=job_states ) ),
     ( r"/job", JobHandler, dict( pending_jobs=pending_jobs ) ),
     ( r"/([0-9a-f-]+)/list_of_packages", ListOfPackagesHandler, dict( root=config[ 'master_root' ] ) ),
     ( r"/([0-9a-f-]+)/(.*.pkg.tar.xz)", PackageHandler, dict( root=config[ 'master_root' ] ) ),
     ( r"/([0-9a-f-]+)/build_log", BuildLogHandler, dict( root=config[ 'master_root' ] ) ),
     ( r"/([0-9a-f-]+)/(.*.tar.gz)", PkgSrcHandler, dict( root=config[ 'master_root' ] ) ),
    ] )

    ws = Spout( config[ 'master_port' ], application )
    ws.start()
