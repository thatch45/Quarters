''' file resereved for the communications of master and builder '''

import bz2
import json
import urllib.request
import os
import glob
import queue # for queue.Empty exception
from quarters.state import json_to_state, State

from quarters.utils import sha256sum_file

def http_url( ip, port ):
    '''
    return an http url from the given ip and port in the form http://ip:port with no trailing '/'

    >>> http_url( '127.0.0.1', '80' )
    'http://127.0.0.1:80'
    '''
    return 'http://' + ip + ':' + port

def get_state( ip, port ):
    ret = State()
    url = http_url( ip, port ) + '/global_status'
    try:
        json_data = get_url( url )
        remote_state = json.loads( json_data.decode('utf-8' ) )
        ret = json_to_state( remote_state )
    except:
        #print( 'failed to retrieve state' )
        ret = State()
    return ret

def master_state( config ):
    '''
    Download the master state file and translate the data to a structure
    '''
    ret = get_state( config[ 'master' ], config[ 'master_port' ] )
    return ret

def builder_states( config ):
    '''
    Retrieve the state of the builders
    '''
    ret = {}
    for ip in config[ 'builders' ]:
        try:
            remote_state = get_state( ip, config[ 'builder_port' ] )
        except:
            continue
        ret.update( { ip : remote_state } )
    return ret

def get_url( url ):
    '''
    returns the contents at the url
    '''
    return urllib.request.urlopen( url ).read()

def get_package_list( ip, ujid, config ):
    remote_state = get_state( ip, config[ 'builder_port' ] )
    return remote_state.get_packages( ujid )

def get_packages( ip, ujid, config ):
    # TODO: implement when we start using https
    # need to make sure that urlretrieve overwrites
    #  if existing file with same name is found
    # "If the URL points to a local file, or a valid
    #  cached copy of the object exists, the object is not copied."
    # http://docs.python.org/py3k/library/urllib.request.html#urllib.request.urlretrieve
    pkg_list = get_package_list( ip, ujid, config )
    port = int( config[ 'builder_port' ] )
    baseurl = 'http://' + ip + ':' + str(port) + '/' + ujid 
    root_ujid_path = os.path.join( config[ 'master_root' ], str(ujid) )
    os.makedirs( root_ujid_path, exist_ok=True )
    for pkg in pkg_list:
        url_to_dl = baseurl + '/' + pkg[ 'pkgname' ]
        pkg_path = os.path.join( root_ujid_path, pkg[ 'pkgname' ] )
        urllib.request.urlretrieve( url_to_dl, pkg_path )
    
def get_build_log( ip, ujid, config ):
    '''
    gets the build log from the ip and ujid
    '''
    port = int( config[ 'builder_port' ] )
    baseurl = 'http://' + ip + ':' + str(port) + '/' + ujid 
    root_ujid_path = os.path.join( config[ 'master_root' ], str(ujid) )
    os.makedirs( root_ujid_path, exist_ok=True )
    build_log_url = baseurl + '/build_log'
    build_log_path = os.path.join( root_ujid_path, 'build_log' )
    urllib.request.urlretrieve( build_log_url, build_log_path )

def response_global_status( local_state ):
    return json.dumps( local_state.get_state_dict() )

def response_package( root, ujid, pkg ):
    ujid_path = os.path.join( root, str( ujid ) )
    pkgul = ujid_path + '/' + str( pkg )
    content = 'blah'
    with open( pkgul, 'rb' ) as fp:
        content = fp.read()
    return content

def response_build_log( root, ujid ):
    ujid_path = os.path.join( root, str( ujid ) )
    build_log_path = ujid_path + '/build_log'
    content = 'blah'
    with open( build_log_path, 'rb' ) as fp:
        content = fp.read()
    return content

def response_job( local_state ):
    ret = ''
    try:
        jd = local_state.get_nowait_pending_job()
        ret = jd.dump_json()
    except queue.Empty:
        ret = 'NOJOBS'
    return ret

def response_pkgsrc( root, ujid ):
    content = ''
    pkgsrc_path = os.path.join( os.path.join( root, str( ujid ) ) )
    pkgsrc_path = os.path.join( pkgsrc_path, str( ujid ) + '.src.tar.gz' )

    with open( pkgsrc_path, 'rb' ) as fp:
        content = fp.read()
    return content

# TODO start using this decorator
def quarters_compress( f ):
    ''' decorator to compress argument '''
    return lambda x: bz2.compress( f( x ) )

# TODO start using this decorator
def quarters_decompress( f ):
    ''' decorator to decompress argument '''
    return lambda x: bz2.decompress( f( x ) )
