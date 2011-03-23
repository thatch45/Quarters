import threading
import time
from quarters.scm.aurrss import AURRSS

class JobFetcher( threading.Thread ):
    ''' manages the status of jobs '''

    def __init__( self, job_states, pending_jobs, config ):
        threading.Thread.__init__( self )
        self.pending_jobs = pending_jobs
        self.job_states = job_states
        self.master = config[ 'master' ]
        self.master_port = config[ 'master_port' ]
        self.master_root = config[ 'master_root' ]

    def run( self ):
        ''' iterator over all scms to fetch new jobs '''
        ar = AURRSS()

        while 1:
            # keep 2 jobs in the buffer
            if self.pending_jobs.qsize() < 2:
                
                for jd in ar.get_jobs():
                    self.add_job( jd )

            time.sleep( 10 )

    def add_job( self, job_description ):
        self.pending_jobs.put( job_description )
        self.job_states[ job_description.ujid ] = 'notdone'
