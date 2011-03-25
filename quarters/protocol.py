''' file resereved for the communications of master and builder '''

import bz2
import json
import urllib.request
import os
import glob

# TODO start using this decorator
def quarters_compress( f ):
    ''' decorator to compress argument '''
    return lambda x: bz2.compress( f( x ) )

# TODO start using this decorator
def quarters_decompress( f ):
    ''' decorator to decompress argument '''
    return lambda x: bz2.decompress( f( x ) )

def foreign_url( ip, port ):
    '''
    Retrive the master url from the configuration
    '''
    return 'http://' + ip + ':' + str( port )

def master_state( config ):
    '''
    Download the master state file and translate the data to a structure
    '''
    ret = {}
    url = foreign_url( config[ 'master' ], config[ 'master_port' ] ) + '/global_status'
    try:
        json_data = get_url( url )
        status = json.loads( json_data.decode('utf-8' ) )
        ret.update( status )
    except:
        print( 'failed to retrieve master state' )
    return ret

def builder_states( config ):
    '''
    Retrieve the state of the builders
    '''
    ret = {}
    for ip in config[ 'builders' ]:
        url = foreign_url( ip, config[ 'builder_port' ] ) + '/global_status'
        try:
            json_data = get_url( url )
        except:
           continue
        status = json.loads( json_data.decode('utf-8' ) )
        ret.update( { ip : status } )
    return ret

def get_url( url ):
    '''
    returns the contents at the url
    '''
    return urllib.request.urlopen( url ).read()

def get_package_list( ip, ujid, config ):
    '''
    gets a dictionary representing the object at http://ip:port/ujid/list_of_packages
    '''
    port = int( config[ 'builder_port' ] )
    url = foreign_url( ip, port ) + '/' + ujid + '/list_of_packages'
    return json.loads( get_url( url ).decode( 'utf-8' ) )

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

def response_global_status( job_states ):
    # we need to wrap in a dict because job_states is a dict proxy
    return json.dumps( dict( job_states ) )

def response_list_of_packages( root, ujid ):
    ujid_path = os.path.join( root, str( ujid ) )
    results = glob.glob( ujid_path + '/*.pkg.tar.xz' )
    results = list( map( lambda x: x.split('/')[-1], results ) )
    temp = [{ 'pkgname' : i, 'sha256sum' : sha256sum_file( ujid_path + '/' + i ) } for i in results]
    return json.dumps( temp )

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

def response_job( pending_jobs ):
    ret = ''
    try:
        jd = pending_jobs.get_nowait()
        ret = jd.dump_json()
    except:
        ret = 'NOJOBS'
    return ret

def response_pkgsrc( root, ujid, pkgname ):
    content = ''
    ujid_path = os.path.join( root, str( ujid ) )
    pkgsrc_path = os.path.join( ujid_path, pkgname )

    with open( pkgsrc_path, 'rb' ) as fp:
        content = fp.read()
    return content
