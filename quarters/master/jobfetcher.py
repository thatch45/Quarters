import threading
import time
#from quarters.scm.aurrss import AURRSS
#from quarters.scm.archsvn import ArchSVN
from quarters.scm.web import Web

class JobFetcher( threading.Thread ):
    ''' manages the status of jobs '''

    def __init__( self, local_state, config ):
        threading.Thread.__init__( self )
        self.local_state = local_state
        self.config = config

    def run( self ):
        ''' iterator over all scms to fetch new jobs '''
        #ar = AURRSS( self.config )
        #svn = ArchSVN( self.config )
        web = Web( self.config )

        while 1:
            # keep 2 jobs in the buffer
            if self.local_state.size_pending_job() < 2:
                
                for jd in web.get_jobs():
                    if jd.ujid not in self.local_state.get_ujids():
                        self.local_state.put_pending_job( jd )

            time.sleep( 100 )
