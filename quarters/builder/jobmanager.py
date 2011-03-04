import threading
from quarters.state import State
import urllib.request
import os
import tarfile
from multiprocessing import Process, Queue, Lock
import subprocess

class JobOverlord( threading.Thread ):
    ''' controls all the poor joblings running on the server '''

    def __init__( self, max_jobs ):
        threading.Thread.__init__( self )
        self.max_jobs = max_jobs
        self.processlist = []
        self.pending_jobs = Queue()
        self.job_states = {}
        mutex = Lock() # used for the job_states

    def run( self ):
        for i in range( self.max_jobs ):
            p = Process( target=worker, args=( self.pending_jobs, i, self.mutex ) )
            p.start()
            self.processlist.append( p )

        for p in self.processlist:
            p.join()

    def add_job( self, job_description ):
        self.pending_jobs.put( job_description )
        self.mutex.acquire()
        job_states[ job_description.ujid ] = 'notdone'
        self.mutex.release()

def worker( job_queue, worker_id, job_states_lock ):
    ''' worker where the grunt work takes place '''
    while 1:
        current_job = job_queue.get()

        # update state here (running)
        job_states_lock.acquire()
        job_states[ current_job.ujid ] = 'inprogress'
        job_states_lock.release()

        # need to send unique chroot path per worker
        current_job.job( worker_id )

        # update state here (done)
        job_states_lock.acquire()
        job_states[ current_job.ujid ] = 'done'
        job_states_lock.release()

class JobDescription:
    ''' a structure to store a job description '''

    # ujid - unique job id, given out by master
    def __init__( self, ujid, package_name, package_source ):
        self.ujid = ujid
        self.package_name = package_name
        self.package_source = package_source

    def job( self, worker_id ):
        job_path = os.path.join( '/var/tmp/quarters/', self.ujid )
        pkgsrc_path = os.path.join( job_path, self.package_name + '.tar.gz' )
        pkg_path = os.path.join( job_path, self.package_name )
        chroot_path = '/var/tmp/quarters/chroots' + str( worker_id )

        os.makedirs( job_path, exist_ok=True )

        # need to make sure that urlretrieve overwrites if existing file with same name is found
        # "If the URL points to a local file, or a valid cached copy of the object exists, the object is not copied."
        # http://docs.python.org/py3k/library/urllib.request.html#urllib.request.urlretrieve
        urllib.request.urlretrieve( self.package_source, pkgsrc_path )

        temp_tar = tarfile.open( pkgsrc_path )
        temp_tar.extractall( job_path )

        chroot_cmd = [ '/usr/bin/extra-x86_64-build', '-r', chroot_path ]
        return_code = subprocess.call( chroot_cmd, cwd=pkg_path )
