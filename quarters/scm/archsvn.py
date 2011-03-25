from quarters.jobdescription import JobDescription
import uuid
import os
import urllib.request
import subprocess
from quarters.protocol import foreign_url
from quarters.utils import sha256sum_file
import glob
import shutil

class ArchSVN:
    ''' an scm that fetches new jobs based on new entries from the aur rss feed '''
    def __init__( self, config ):
        self.prev_pkgname = ''
        self.config = config
        self.master = config[ 'master' ]
        self.master_port = config[ 'master_port' ]
        self.master_root = config[ 'master_root' ]
        self.svn_root = config[ 'svn_root' ]

    def get_jobs( self ):
        ''' returns a list of new jobdescriptions '''
        ret = []
        svnup_cmd = [ '/usr/bin/svn', 'up' ]
        pkgs = set()

        with subprocess.Popen( svnup_cmd, cwd=self.svn_root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT ) as proc:
            lines = proc.communicate()[0].splitlines()
            #return_code = proc.returncode

        # find unique pkgnames
        for line in lines[0:-1]:
            pkgname = bytes.decode(line).split('/')[0].split()[1]
            pkgs.add( pkgname )

        makepkg_cmd = [ '/usr/bin/makepkg', '--source', '--skipinteg' ]
        for pkg in pkgs:
            new_ujid = str( uuid.uuid4() )

            # create a srcpkg
            print( 'getting package from svn' )
            print( pkg )
            pkg_path = os.path.join( self.svn_root,  pkg + '/trunk' )
            proc = subprocess.Popen( makepkg_cmd, cwd=pkg_path ) #, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
            proc.wait()
            srcpkg_path = os.path.join( self.master_root, new_ujid )
            os.makedirs( srcpkg_path, exist_ok=True )
            srcpkg_path = os.path.join( srcpkg_path, new_ujid + '.src.tar.gz' )

            # TODO: find a pythonic way of doing this
            #mvcmd = '/bin/mv -f ' + os.path.join( pkg_path, pkg + '*.src.tar.gz' ) + ' ' + srcpkg_path
            getsrc = glob.glob( os.path.join( pkg_path, pkg + '*.src.tar.gz' ) )
            print( 'glob returned' + str( getsrc ) )

            if len( getsrc ) != 1:
                print( 'error moving srcpkgs, not enough, or too many detected' )
                continue

            shutil.move( getsrc[0], srcpkg_path )
            #mvcmd = [ '/bin/mv', os.path.join( pkg_path, pkg + '*.src.tar.gz' ), srcpkg_path ]
            #print( mvcmd )
            #mv_return_code = subprocess.call( mvcmd, shell=True )

            # TODO we could probably get rid of the job_url and have the url always point to the master
            job_url = foreign_url( self.master, self.master_port ) + '/' + new_ujid + '/' + new_ujid + '.src.tar.gz'
            sha256sum = sha256sum_file( srcpkg_path )

            # job description: ujid, cur_pkgname, pkgsrc, sha256sum of srcpkg, architecture to build (x86_64,i686,any)
            jd = JobDescription( new_ujid, pkgname, job_url, sha256sum, 'x86_64' )

            ret.append( jd )

        return ret
