import threading
import time
#from quarters.scm.aurrss import AURRSS
from quarters.scm.archsvn import ArchSVN

class JobFetcher( threading.Thread ):
    ''' manages the status of jobs '''

    def __init__( self, job_states, pending_jobs, config ):
        threading.Thread.__init__( self )
        self.pending_jobs = pending_jobs
        self.job_states = job_states
        self.config = config

    def run( self ):
        ''' iterator over all scms to fetch new jobs '''
        #ar = AURRSS( self.config )
        svn = ArchSVN( self.config )

        while 1:
            # keep 2 jobs in the buffer
            if self.pending_jobs.qsize() < 2:
                
                for jd in svn.get_jobs():
                    self.add_job( jd )

            time.sleep( 100 )

    def add_job( self, job_description ):
        self.pending_jobs.put( job_description )
        self.job_states[ job_description.ujid ] = 'notdone'
