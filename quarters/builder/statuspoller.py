import threading
from quarters.utils import fetch_states
import time
import shutil
import os

class StatusPoller( threading.Thread ):
    def __init__( self, job_states, config ):
        threading.Thread.__init__( self )
        self.job_states = job_states
        self.list_of_ips = [ config[ 'master' ] ]
        self.port = config[ 'master_port' ]
        self.builder_root = config[ 'builder_root' ]

    def run( self ):
        while 1:
            # cur is the status on master
            cur = fetch_states( self.list_of_ips, self.port )
            # there is only 1 ip (master) on the builder status poller
            cur = cur[ self.list_of_ips[0] ]

            print( 'master status:', cur )
            print( 'local status:', self.job_states )
            
            for ( ujid, v ) in self.job_states.items():
                if ujid in cur:
                    if cur[ ujid ] == 'stop':
                        # TODO: implement stop
                        self.job_states[ ujid ] = 'stop'
                        pass

                    if cur[ ujid ] == 'done' and v == 'done':
                        # remove from builder since master already synced this job
                        rm_path = os.path.join( self.builder_root, ujid )
                        # TODO: find out why this is getting deleted early
                        #shutil.rmtree( rm_path )
                        # remove the key from the builder status since it is done
                        del self.job_states[ ujid ]

                    if cur[ ujid ] == 'failed' and v == 'failed':
                        # remove from builder since master already synced this job
                        rm_path = os.path.join( self.builder_root, ujid )
                        # TODO: find out why this is getting deleted early
                        #shutil.rmtree( rm_path )
                        # remove the key from the builder status since it is done
                        del self.job_states[ ujid ]

            time.sleep( 2 )
