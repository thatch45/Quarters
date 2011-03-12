import threading
import quarters.utils
from quarters.utils import fetch_states
from quarters.utils import get_url
import time
import json
import os
import urllib.request

class StatusPoller( threading.Thread ):
    def __init__( self, job_states, config ):
        threading.Thread.__init__( self )
        self.job_states = job_states
        self.list_of_ips = config[ 'builders' ]
        self.port = int( config[ 'builder_port' ] )
        self.master_root = config[ 'master_root' ]

    def run( self ):
        while 1:
            cur = fetch_states( self.list_of_ips, self.port )

            print( 'remote status:', cur )
            print( 'local status:', self.job_states )
            
            for ( ujid, v ) in self.job_states.items():
                # skip values that are going to be final
                if v in ( 'done', 'failed' ):
                    pass

                if ujid in cur:
                    if cur[ ujid ] == 'done' and v != 'done':
                        self.job_states[ ujid ] = 'downloading'

                        # TODO: download packages and build_log
                        root_ujid_path = os.path.join( self.master_root , str(ujid) )
                        os.makedirs( root_ujid_path, exist_ok=True )

                        baseurl = 'http://' + self.list_of_ips[0] + ':' + str(self.port) + '/' + ujid 
                        url = baseurl + '/list_of_packages'
                        pkg_list = json.loads( get_url( url ).decode( 'utf-8' ) )

                        # TODO: implement when we start using https
                        # need to make sure that urlretrieve overwrites
                        #  if existing file with same name is found
                        # "If the URL points to a local file, or a valid
                        #  cached copy of the object exists, the object is not copied."
                        # http://docs.python.org/py3k/library/urllib.request.html#urllib.request.urlretrieve
                        for pkg in pkg_list:
                            url_to_dl = baseurl + '/' + pkg[ 'pkgname' ]
                            pkg_path = os.path.join( root_ujid_path, pkg[ 'pkgname' ] )
                            urllib.request.urlretrieve( url_to_dl, pkg_path )
                        build_log_url = baseurl + '/build_log'
                        build_log_path = os.path.join( root_ujid_path, 'build_log' )
                        urllib.request.urlretrieve( build_log_url, build_log_path )

                        self.job_states[ ujid ] = 'done'

                    if cur[ ujid ] == 'failed' and v != 'failed':
                        self.job_states[ ujid ] = 'downloading'
                        # TODO: download packages and build_log
                        self.job_states[ ujid ] = 'failed'

                    if cur[ ujid ] == 'inprogress':
                        # we don't give a
                        pass

                    if cur[ ujid ] == 'notdone':
                        # we don't give a
                        pass

            time.sleep( 2 )
