import threading
import time
import shutil
import os
from quarters.protocol import master_state

class StatusPoller( threading.Thread ):
    def __init__( self, job_states, config ):
        threading.Thread.__init__( self )
        self.job_states = job_states
        self.config = config
        self.builder_root = config[ 'builder_root' ]

    def run( self ):
        while 1:
            cur = master_state( self.config )

            print( 'master status:', cur )
            print( 'local status:', self.job_states )
            
            for ( ujid, v ) in self.job_states.items():
                if ujid in cur:
                    if cur[ ujid ] == 'stop':
                        # TODO: implement stop
                        self.job_states[ ujid ] = 'stop'
                        pass

                    if cur[ ujid ] in ( 'done', 'failed' ) and v in ( 'done', 'failed' ):
                        # remove from builder since master already synced this job
                        rm_path = os.path.join( self.builder_root, ujid )
                        shutil.rmtree( rm_path )
                        # remove the key from the builder status since it is done
                        del self.job_states[ ujid ]

            time.sleep( 2 )
