import threading
from quarters.state import State
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

    def run( self ):
        # add packages (FAKE it for now since we don't have a working server to test it on)
        i = 0
        while 1:
            # keep 1 job in the buffer
            if self.pending_jobs.qsize() < 2:
                pkgname = 'libuser'
                pkgurl = 'https://aur.archlinux.org/packages/' + pkgname + '/' + pkgname + '.tar.gz'

                # job description: ujid, pkgname, pkgsrc
                jd = JobDescription( str(i), pkgname, pkgurl )
                self.add_job( jd )

                time.sleep( 10 )
                i += 1
            # do check ups here on package status on builders

    def add_job( self, job_description ):
        self.pending_jobs.put( job_description )
        self.job_states[ job_description.ujid ] = 'notdone'
