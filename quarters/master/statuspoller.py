import threading
from quarters.utils import get_url
import json
import time

class StatusPoller( threading.Thread ):
    def __init__( self, job_states, list_of_ips, port ):
        threading.Thread.__init__( self )
        self.job_states = job_states
        self.list_of_ips = list_of_ips

    def fetch_states( self ):
        ret = {}
        for ip in self.list_of_ips:
            try:
                status = json.loads( get_url( 'http://' + ip + ':' + str( port ) + '/global_status' ) )
                ret.update( status )
                # remove if dict.update works
                #for k, v in status:
                #    a[k] = v
            except:
                continue

    def run( self ):
        while 1:
            cur = fetch_states()

            for k, v in self.job_states:
                # skip values that are going to be final
                if v in ( 'done', 'failed' ):
                    continue

                if cur[ k ] in ( 'done', 'failed' ):
                    self.job_states[ k ] = 'downloading'
                    # TODO: download packages and build_log
                    self.job_states[ k ] = cur[ k ]

                if cur[ k ] == 'inprogress':
                    # we don't give a
                    pass

                if cur[ k ] == 'notdone':
                    # we don't give a
                    pass

            print( self.job_states )

            time.sleep( 2 )
