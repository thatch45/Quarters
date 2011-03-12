import threading
import urllib.request
import os
import tarfile
import subprocess
import time
from quarters.jobdescription import JobDescription

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
        # add packages (FAKE it for now since we don't have a working server to test it on)
        new_ujid = 0
        while 1:
            # keep 1 job in the buffer
            if self.pending_jobs.qsize() < 2:
                
                pkgname = 'libuser'
                pkgurl = 'https://' + self.master + ':' + str( self.master_port ) + '/' + str( new_ujid ) + '/' + pkgname + '.tar.gz'

                # TODO make package sources available only through master
                job_path = os.path.join( self.master_root, str( new_ujid ) )

                # job description: ujid, pkgname, pkgsrc
                jd = JobDescription( str( new_ujid ), pkgname, pkgurl )
                self.add_job( jd )

                time.sleep( 10 )
                new_ujid += 1
            # do check ups here on package status on builders

    def add_job( self, job_description ):
        self.pending_jobs.put( job_description )
        self.job_states[ job_description.ujid ] = 'notdone'
