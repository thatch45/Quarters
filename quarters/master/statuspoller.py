import threading
import quarters.utils
from quarters.protocol import builder_states, get_packages, get_build_log
import time
import os

class StatusPoller( threading.Thread ):
    def __init__( self, local_state, config ):
        threading.Thread.__init__( self )
        self.local_state = local_state
        self.config = config

    def run( self ):
        while 1:
            # { ip : State, ... }
            b_states = builder_states( self.config )

            print( 'builder states:', b_states )
            print( 'local (master) state:', self.job_states )

            local_ujids = self.local_state.get_ujids()
            for ( ip, remote_state ) in b_states.items():
                remote_ujids = set( remote_state.get_ujids() )
                for ujid in remote_ujids.intersection( local_ujids ):
                    remote_status = remote_state.get_status( ujid )
                    local_status = self.local_state.get_status( ujid )
                    if remote_status == 'done' and local_status != 'done':
                        self.local_state.set_status( ujid, 'downloading' )
                        get_packages( ip, ujid, self.config )
                        get_build_log( ip, ujid, self.config )
                        self.local_state.set_status( ujid, 'done' )

                    if remote_status == 'failed' and local_status != 'failed':
                        self.local_state.set_status( ujid, 'downloading' )
                        get_build_log( ip, ujid, self.config )
                        self.local_state.set_status( ujid, 'failed' )

            time.sleep( 2 )
