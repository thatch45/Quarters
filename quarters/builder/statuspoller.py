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
            # cur is the status on master
            cur = fetch_states( self.list_of_ips, self.port )

            print( 'master status:', cur )
            print( 'local status:', self.job_states )
            
            for ( k, v ) in self.job_states.items():
                if k in cur:
                    if cur[ k ] == 'stop':
                        # TODO: implement stop
                        # stop job k
                        self.job_states[ k ] = 'stop'
                        pass

                    if cur[ k ] == 'done' and v == 'done':
                        # remove from builder since master already synced this job
                        pass

                    if cur[ k ] == 'failed' and v == 'failed':
                        # remove from builder since master already synced this job
                        pass

            time.sleep( 2 )
