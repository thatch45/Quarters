import threading
import quarters.utils
from quarters.protocol import builder_states, get_package_list, get_packages, get_build_log
import time
import os
import urllib.request

class StatusPoller( threading.Thread ):
    def __init__( self, job_states, config ):
        threading.Thread.__init__( self )
        self.job_states = job_states
        self.config = config

    def run( self ):
        while 1:
            # { ip : { ujid : status, ... }, ... }
            b_states = builder_states( self.config )

            print( 'builder states:', b_states )
            print( 'local (master) state:', self.job_states )

            for ( ip, cur ) in b_states.items():
                for ( ujid, v ) in self.job_states.items():
                    # skip values that are finalized
                    if v in ( 'done', 'failed' ):
                        pass

                    if ujid in cur:
                        if cur[ ujid ] == 'done' and v != 'done':
                            self.job_states[ ujid ] = 'downloading'
                            get_packages( ip, ujid, pkg_list, self.config )
                            get_build_log( ip, ujid, self.config )
                            self.job_states[ ujid ] = 'done'

                        if cur[ ujid ] == 'failed' and v != 'failed':
                            self.job_states[ ujid ] = 'downloading'
                            get_build_log( ip, ujid, self.config )
                            self.job_states[ ujid ] = 'failed'

                        if cur[ ujid ] == 'inprogress':
                            # we don't give a
                            pass

                        if cur[ ujid ] == 'notdone':
                            # we don't give a
                            pass

            time.sleep( 2 )
