from quarters.jobdescription import JobDescription
import uuid
import os
import urllib.request
import subprocess
from quarters.protocol import foreign_url
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

        json_data = get_url( 'http://localhost:8080/stat' )
        temp_json = bytes.decode( json_data )
        print( 'temp_json is:', temp_json )
        print( 'json_data is:', json_data )
        remote_pkgs = json.loads( json_data )

        makepkg_cmd = [ 'makepkg', '--source', '--skipinteg' ]
        for rpkg in remote_pkgs:
            # copy over the sources to a temp directory
            orig_dir = os.path.join( '/var/abs/core', rpkg[ 'pkgname' ] )
            dest_dir = os.path.join( '/tmp', rpkg[ 'uuid' ] )
            os.makedirs( dest_dir, exist_ok=True )
            shutil.copytree( orig_dir, dest_dir )

            # build the .src.tar.gz file
            proc = subprocess.Popen( makepkg_cmd, cwd=dest_dir )
            proc.wait()

            # find the resulting .src.tar.gz file
            getsrc = glob.glob( os.path.join( dest_dir, '*.src.tar.gz' ) )
            print( 'glob returned' + str( getsrc ) )
            if len( getsrc ) != 1:
                print( 'error, not enough, or too many srcpkgs detected in Web' )
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
