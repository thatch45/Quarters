''' file resereved for the communications of master and builder '''

import bz2
from quarters.utils import fetch_states

# TODO start using this decorator
def quarters_compress( f ):
    ''' decorator to compress argument '''
    return lambda x: f( bz2.compress( x ) )

# TODO start using this decorator
def quarters_decompress( f ):
    ''' decorator to decompress argument '''
    return lambda x: f( bz2.decompress( x ) )

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
    ''' returns the contents at the url '''
    return urllib.request.urlopen( url ).read()
