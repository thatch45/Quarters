import threading
import urllib.request
import os
import tarfile
from multiprocessing import Process
import subprocess
import time
from quarters.jobdescription import JobDescription
from quarters.protocol import get_url
import glob
import shutil
from quarters.utils import sha256sum_file

class JobOverlord( threading.Thread ):
    ''' controls all the poor joblings running on the server '''

    def __init__( self, local_state, config ):
        threading.Thread.__init__( self )
        self.max_jobs = int( config['chroots'] )
        self.processlist = []
        self.local_state = local_state
        self.builder_root = config['builder_root']
        self.master = config['master']
        self.master_port = config['master_port']
        self.config = config

    def run( self ):
        # start all the workers
        for worker_id in range( self.max_jobs ):
            p = Process( target=worker, args=( worker_id, self.local_state, self.config ) )
            p.start()
            self.processlist.append( p )

        while 1:
            # keep 1 job in the buffer
            time.sleep( 2 )

            if self.local_state.size_pending_job() < 1:
                new_job_url = 'http://' + self.master + ':' + str( self.master_port ) + '/job'
                
                try:
                    ret = get_url( new_job_url ).decode( 'utf-8' )
                except:
                    print( 'could not contact master' )
                    continue

                if ret != 'NOJOBS':
                    jd = JobDescription.load_json( ret )
                    self.local_state.put_pending_job( jd )
                    print( 'added', ret )
                else:
                    print( 'NOJOBS' )

def worker( worker_id, local_state, config ):
    ''' worker where the grunt work takes place '''
    builder_root = config['builder_root']
    while 1:
        current_job = local_state.get_pending_job()

        # update job state here (running)
        local_state.set_status( current_job.ujid, 'inprogress' )

        job_path = os.path.join( builder_root, str(current_job.ujid) )
        pkgsrc_path = os.path.join( job_path, current_job.package_name + '.tar.gz' )
        pkg_path = os.path.join( job_path, current_job.package_name )

        os.makedirs( job_path, exist_ok=True )

        # TODO: implement when we start using https
        # need to make sure that urlretrieve overwrites if existing file with same name is found
        # "If the URL points to a local file, or a valid cached copy of the object exists, the object is not copied."
        # http://docs.python.org/py3k/library/urllib.request.html#urllib.request.urlretrieve
        srcpkg_url = 'http://' + config[ 'master' ] + ':' + str( config[ 'master_port' ] ) + '/' + current_job.ujid + '/' + current_job.ujid + '.src.tar.gz'
        # TODO: wrap this in a protocol.py function
        urllib.request.urlretrieve( srcpkg_url, pkgsrc_path )

        # extract
        temp_tar = tarfile.open( pkgsrc_path )
        temp_tar.extractall( job_path )

        # chroot
        if current_job.architecture == 'i686':
            chroot_cmd = [ 'sudo', 'extra-i686-build', '-r', config[ 'chroot_root' ] ]
        else:
            chroot_cmd = [ 'sudo', 'extra-x86_64-build', '-r', config[ 'chroot_root' ] ]

        with subprocess.Popen( chroot_cmd, cwd=pkg_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT ) as proc:
            log_path = os.path.join( job_path, 'build_log' )
            with open( log_path, 'wb' ) as f:
                f.write( proc.communicate()[0] )
            return_code = proc.returncode

        # if failed, just ignore the rest of the code
        if return_code != 0:
            local_state.set_status( current_job.ujid, 'failed' )
            continue

        # move to final destination
        getsrc = glob.glob( os.path.join( pkg_path, '*.pkg.tar.[gx]z' ) )
        for pkg in getsrc:
            shutil.move( pkg, job_path )

        getsrc = glob.glob( os.path.join( job_path, '*.pkg.tar.[gx]z' ) )
        # update list of packages
        results = list( map( (lambda x: x.split('/')[-1]), getsrc ) )
        temp = [{ 'pkgname' : i, 'sha256sum' : sha256sum_file( job_path + '/' + i ) } for i in results]
        local_state.set_packages( current_job.ujid, temp )

        local_state.set_status( current_job.ujid, 'done' )
