from quarters.jobdescription import JobDescription
import uuid
import os
import subprocess
from quarters.utils import sha256sum_file
import glob
import shutil
from quarters.protocol import get_url
import json

class Web:
    def __init__( self, config ):
        self.config = config
        self.master_root = config[ 'master_root' ]

    def get_jobs( self ):
        ''' returns a list of new jobdescriptions '''

        ret = []

        # make sure we can exit safely if the web ui is down
        try:
            json_data = get_url( 'http://localhost:8080/stat' )
        except:
            return ret

        temp_json = bytes.decode( json_data )
        print( 'temp_json is:', temp_json )
        print( 'json_data is:', json_data )
        remote_pkgs = json.loads( temp_json )

        makepkg_cmd = [ 'makepkg', '--source', '--skipinteg' ]
        for rpkg in remote_pkgs:
            # copy over the sources to a temp directory
            orig_dir = os.path.join( '/var/abs/core', rpkg[ 'pkgname' ] )
            dest_dir = os.path.join( '/tmp', rpkg[ 'uuid' ] )
            # check if we already did this
            if os.path.exists( dest_dir ):
                continue
            shutil.copytree( orig_dir, dest_dir )

            # build the .src.tar.gz file
            proc = subprocess.Popen( makepkg_cmd, cwd=dest_dir )
            proc.wait()

            # find the resulting .src.tar.gz file
            getsrc = glob.glob( os.path.join( dest_dir, '*.src.tar.gz' ) )
            print( 'glob returned' + str( getsrc ) )
            if len( getsrc ) != 1:
                print( 'error, not enough, or too many srcpkgs detected in Web' )
                # TODO change status instead of just ignoring the package
                # also need to create a build log with a message from the scm telling what happened
                continue

            # get the sha256sum of the file
            sha256sum = sha256sum_file( getsrc[0] )

            # move the srcpkg to the final resting place
            srcpkg_path = os.path.join( self.master_root, rpkg[ 'uuid' ] )
            os.makedirs( srcpkg_path, exist_ok=True )
            srcpkg_path = os.path.join( srcpkg_path, rpkg[ 'uuid' ] + '.src.tar.gz' )
            shutil.move( getsrc[0], srcpkg_path )

            # add the final jobdescription to the list
            jd = JobDescription( rpkg[ 'uuid' ], rpkg[ 'pkgname' ], sha256sum, 'x86_64' )
            ret.append( jd )

        return ret
