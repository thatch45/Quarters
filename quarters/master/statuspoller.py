import threading
from quarters.utils import fetch_states
import time

class StatusPoller( threading.Thread ):
    def __init__( self, job_states, list_of_ips, port ):
        threading.Thread.__init__( self )
        self.job_states = job_states
        self.list_of_ips = list_of_ips
        self.port = port

    def run( self ):
        while 1:
            cur = fetch_states( self.list_of_ips, self.port )

            print( 'remote status:', cur )
            print( 'local status:', self.job_states )
            
            for ( k, v ) in self.job_states.items():
                # skip values that are going to be final
                if v in ( 'done', 'failed' ):
                    pass

                if k in cur:
                    if cur[ k ] == 'done' and v != 'done':
                        self.job_states[ k ] = 'downloading'
                        # TODO: download packages and build_log
                        self.job_states[ k ] = 'done'

                    if cur[ k ] == 'failed' and v != 'failed':
                        self.job_states[ k ] = 'downloading'
                        # TODO: download packages and build_log
                        self.job_states[ k ] = 'failed'

                    if cur[ k ] == 'inprogress':
                        # we don't give a
                        pass

                    if cur[ k ] == 'notdone':
                        # we don't give a
                        pass

            time.sleep( 2 )