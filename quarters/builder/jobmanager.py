import threading
from quarters.state import State
import urllib.request
import os
import tarfile
from multiprocessing import Process, Queue
from subprocess import Popen

class JobOverlord( threading.Thread ):
    ''' controls all the poor joblings running on the server '''

    def __init__( self, max_jobs ):
        threading.Thread.__init__( self )
        self.max_jobs = max_jobs
        self.plist = []
        self.pending_jobs = Queue()

    def run( self ):
        for i in range( self.max_jobs ):
            p = Process( target=worker, args=( self.pending_jobs, i ) )
            p.start()
            self.plist.append( p )

        for p in self.plist:
            p.join()

    def add_job( self, job_description ):
        self.pending_jobs.put( job_description )

def worker( job_queue, worker_id ):
    ''' worker where the grunt work takes place '''
    while 1:
        current_job = job_queue.get()

        # update state here (running)

        # need to send unique chroot path per worker
        current_job.job( '/var/tmp/quarters/chroots' + str( worker_id ) )

        # update state here (done)

class JobDescription:
    ''' a structure to store a job description '''

    # ujid - unique job id, given out by master
    def __init__( self, ujid, package_name, package_source ):
        self.ujid = ujid
        self.package_name = package_name
        self.package_source = package_source

    def job( self, chroot_path ):
        print( 'thread %s sleeping for 2 seconds' % ( self.package_name ) )

        job_path = os.path.join( '/var/tmp/quarters/', self.ujid )
        pkgsrc_path = os.path.join( job_path, self.package_name + '.tar.gz' )

        try:
            os.makedirs( job_path )
        except os.error as e:
            print( 'warning: leaf directory already exists at ' + job_path )

        # need to make sure that urlretrieve overwrites if existing file with same name is found
        # "If the URL points to a local file, or a valid cached copy of the object exists, the object is not copied."
        # http://docs.python.org/py3k/library/urllib.request.html#urllib.request.urlretrieve
        urllib.request.urlretrieve( self.package_source, pkgsrc_path )

        temp_tar = tarfile.open( pkgsrc_path )
        temp_tar.extractall( job_path )

        Popen( ['/usr/bin/testing-x86_64-build', '-r', chroot_path ], cwd=os.path.join( job_path, self.package_name ) )
