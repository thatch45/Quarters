import threading
import urllib.request
import os
import tarfile
import subprocess
import time
from quarters.jobdescription import JobDescription
import urllib.request

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
        prev_pkgname = ''
        while 1:
            time.sleep( 10 )

            # keep 2 jobs in the buffer
            if self.pending_jobs.qsize() < 2:
                
                temp = urllib.request.urlopen( 'http://aur.archlinux.org/rss.php' ).read().decode( 'ascii' ).split('\n')[16].split('>')[1].split('<')[0]

                if prev_pkgname == temp:
                    continue
                prev_pkgname = temp
                pkgname = temp
                pkgurl = 'http://' + self.master + ':' + str( self.master_port ) + '/' + str( new_ujid ) + '/' + pkgname + '.tar.gz'

                job_path = os.path.join( self.master_root, str( new_ujid ) )
                pkgsrc_path = os.path.join( job_path, pkgname + '.tar.gz' )
                remote_url = 'https://aur.archlinux.org/packages/' + pkgname + '/' + pkgname + '.tar.gz'
                os.makedirs( job_path, exist_ok=True )
                urllib.request.urlretrieve( remote_url, pkgsrc_path )

                # job description: ujid, pkgname, pkgsrc, sha256sum of srcpkg, architecture to build (x86_64,i686,any)
                jd = JobDescription( str( new_ujid ), pkgname, pkgurl, 'sha256sumgoeshere', 'x86_64' )
                self.add_job( jd )

                new_ujid += 1

    def add_job( self, job_description ):
        self.pending_jobs.put( job_description )
        self.job_states[ job_description.ujid ] = 'notdone'
