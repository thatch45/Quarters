import tornado.ioloop
import tornado.web
from quarters.common_spout_interface import Spout, GlobalStatusHandler, ListOfPackagesHandler, PackageHandler, BuildLogHandler

def start_builder_web( job_states, port ):
    application = tornado.web.Application( [
        ( r"/global_status", GlobalStatusHandler, dict( job_states=job_states ) ),
        ( r"/([0-9]+)/list_of_packages", ListOfPackagesHandler ),
        ( r"/([0-9]+)/(.*.pkg.tar.xz)", PackageHandler ),
        ( r"/([0-9]+)/build_log", BuildLogHandler ),
    ] )

    ws = Spout( port, application )
    ws.start()
