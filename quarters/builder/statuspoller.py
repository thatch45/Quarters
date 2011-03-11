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
                if k in cur:
                    if cur[ k ] == 'stop':
                        # stop job k
                        pass

                    if cur[ k ] == 'done' and v != 'done':
                        pass

                    if cur[ k ] == 'failed' and v != 'failed':
                        pass

            time.sleep( 2 )
