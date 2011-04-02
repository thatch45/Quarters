import threading
import time
import shutil
import os
from quarters.protocol import master_state

class StatusPoller( threading.Thread ):
    def __init__( self, local_state, config ):
        threading.Thread.__init__( self )
        self.local_state = local_state
        self.config = config
        self.builder_root = config[ 'builder_root' ]

    def run( self ):
        while 1:
            remote_state = master_state( self.config )

            print( 'master status:', remote_state.get_state_dict() )
            print( 'local status:', self.local_state.get_state_dict() )
            
            remote_ujids = set( remote_state.get_ujids() ) # master
            local_ujids = set( self.local_state.get_ujids() ) # builder
            for ujid in remote_ujids.intersection( local_ujids ):
                local_status = self.local_state.get_status( ujid )
                remote_status = remote_state.get_status( ujid )
                if local_status in ( 'done', 'failed' ) and remote_status == local_status:
                    # remove from builder since master already synced this job
                    rm_path = os.path.join( self.builder_root, ujid )
                    shutil.rmtree( rm_path )
                    # remove the key from the builder status since it is done
                    self.local_state.remove_ujid( ujid )

            time.sleep( 2 )
