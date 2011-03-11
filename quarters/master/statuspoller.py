import threading
from quarters.utils import get_url
import json
import time

class StatusPoller( threading.Thread ):
    def __init__( self, job_states, list_of_ips, port ):
        threading.Thread.__init__( self )
        self.job_states = job_states
        self.list_of_ips = list_of_ips
        self.port = port

    def fetch_states( self ):
        ret = {}
        for ip in self.list_of_ips:
            url = 'http://' + ip + ':' + str( self.port ) + '/global_status'

            try:
                json_data = get_url( url )
            except:
                continue

            status = json.loads( json_data.decode('utf-8' ) )

            ret.update( status )

        return ret

    def run( self ):
        while 1:
            cur = self.fetch_states()

            print( 'remote status:', cur )
            print( 'local status:', self.job_states )
            
            if len( cur ):
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
