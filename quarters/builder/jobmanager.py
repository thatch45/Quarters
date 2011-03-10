import threading
import urllib.request
import os
import tarfile
from multiprocessing import Process, Queue
import subprocess
import time
from quarters.jobdescription import JobDescription
from quarters.utils import get_url

class JobOverlord( threading.Thread ):
    ''' controls all the poor joblings running on the server '''

    def __init__( self, job_states, config ):
        threading.Thread.__init__( self )
        self.max_jobs = int( config['chroots'] )
        self.processlist = []
        self.pending_jobs = Queue()
        self.job_states = job_states
        self.chroot_base = config['chroot_base']
        self.master = config['master']
        self.master_port = config['master_port']

    def run( self ):
        # start all the workers
        for worker_id in range( self.max_jobs ):
            p = Process( target=worker, args=( self.pending_jobs, worker_id, self.job_states, self.chroot_base ) )
            p.start()
            self.processlist.append( p )

        # add packages (FAKE it for now since we don't have a working server to test it on)
        i = 0
        while 1:
            # keep 1 job in the buffer
            if self.pending_jobs.qsize() < 1:
                ret = get_url( 'http://0.0.0.0:' + str( self.master_port ) + '/job' ).decode( 'utf-8' )
                print( ret )
                if ret != 'NOJOBS':
                    jd = JobDescription( 0, 0, 0 )
                    jd.load_json( ret )
                    self.add_job( jd )

                time.sleep( 2 )

    def add_job( self, job_description ):
        self.pending_jobs.put( job_description )
        self.job_states[ job_description.ujid ] = 'notdone'

def worker( job_queue, worker_id, job_states, chroot_base ):
    ''' worker where the grunt work takes place '''
    while 1:
        current_job = job_queue.get()

        # update job state here (running)
        job_states[ current_job.ujid ] = 'inprogress'

        job_path = os.path.join( '/var/tmp/quarters/', str(current_job.ujid) )
        pkgsrc_path = os.path.join( job_path, current_job.package_name + '.tar.gz' )
        pkg_path = os.path.join( job_path, current_job.package_name )
        chroot_path = os.path.join( chroot_base, str( worker_id ) )

        os.makedirs( job_path, exist_ok=True )

        # TODO: implement when we start using https
        # need to make sure that urlretrieve overwrites if existing file with same name is found
        # "If the URL points to a local file, or a valid cached copy of the object exists, the object is not copied."
        # http://docs.python.org/py3k/library/urllib.request.html#urllib.request.urlretrieve
        urllib.request.urlretrieve( current_job.package_source, pkgsrc_path )

        # extract
        temp_tar = tarfile.open( pkgsrc_path )
        temp_tar.extractall( job_path )

        # chroot
        chroot_cmd = [ '/usr/bin/extra-x86_64-build', '-r', chroot_path ]
        with subprocess.Popen( chroot_cmd, cwd=pkg_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
            log_path = os.path.join( job_path, 'build_log' )
            with open( log_path, 'wb' ) as f:
                f.write( proc.communicate()[0] )
            return_code = proc.returncode

        # move to final destination
        # TODO: find a pythonic way of doing this
        mvcmd = '/bin/mv -f ' + pkg_path + '/*.pkg.tar.xz ' + job_path
        mv_return_code = subprocess.call( mvcmd , shell=True )
        ###### end building

        # update job state (failed or done)
        if return_code != 0:
            job_states[ current_job.ujid ] = 'failed'
        else:
            job_states[ current_job.ujid ] = 'done'
