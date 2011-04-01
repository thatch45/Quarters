from quarters.jobdescription import JobDescription
import uuid
import os
import subprocess
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

        # find unique pkgnames
        for line in lines[0:-1]:
            pkgname = bytes.decode(line).split('/')[0].split()[1]
            pkgs.add( pkgname )

        makepkg_cmd = [ 'makepkg', '--source', '--skipinteg' ]
        for pkg in pkgs:
            new_ujid = str( uuid.uuid4() )

            # create a srcpkg
            print( 'getting package from svn' )
            print( pkg )
            pkg_path = os.path.join( self.svn_root,  pkg + '/trunk' )
            proc = subprocess.Popen( makepkg_cmd, cwd=pkg_path ) #, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
            proc.wait()
            print( 'process returned ' + str( proc.returncode ) )
            srcpkg_path = os.path.join( self.master_root, new_ujid )
            os.makedirs( srcpkg_path, exist_ok=True )
            srcpkg_path = os.path.join( srcpkg_path, new_ujid + '.src.tar.gz' )

            getsrc = glob.glob( os.path.join( pkg_path, pkg + '*.src.tar.gz' ) )
            print( 'glob returned' + str( getsrc ) )

            if len( getsrc ) != 1:
                print( 'error moving srcpkgs, not enough, or too many detected' )
                continue

            shutil.move( getsrc[0], srcpkg_path )

            sha256sum = sha256sum_file( srcpkg_path )

            # job description: ujid, cur_pkgname, pkgsrc, sha256sum of srcpkg, architecture to build (x86_64,i686,any)
            jd = JobDescription( new_ujid, pkgname, sha256sum, 'x86_64' )

            ret.append( jd )

        return ret
