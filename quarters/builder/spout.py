import tornado.ioloop
import tornado.web
from quarters.common_spout_interface import Spout, GlobalStatusHandler, ListOfPackagesHandler, PackageHandler, BuildLogHandler

def start_builder_web( job_states, config ):
    application = tornado.web.Application( [
        ( r"/global_status", GlobalStatusHandler, dict( job_states=job_states ) ),
        ( r"/([0-9]+)/list_of_packages", ListOfPackagesHandler, dict( root=config[ 'builder_root' ] ) ),
        ( r"/([0-9]+)/(.*.pkg.tar.xz)", PackageHandler, dict( root=config[ 'builder_root' ] ) ),
        ( r"/([0-9]+)/build_log", BuildLogHandler, dict( root=config[ 'builder_root' ] ) ),
    ] )

    ws = Spout( int (config[ 'builder_port' ] ), application )
    ws.start()
