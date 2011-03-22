''' file resereved for the communications of master and builder '''

import bz2

def quarters_compress( f ):
    ''' decorator to compress argument '''
    return lambda x: f( bz2.compress( x ) )

def quarters_decompress( f ):
    ''' decorator to decompress argument '''
    return lambda x: f( bz2.decompress( x ) )

def master_url():
    '''
    Retrive the master url from the configuration
    '''
    pass

def master_state():
    '''
    Download the master state file and translate the data to a structure
    '''
    pass

def build_pkgs():
    '''
    Download the build_pkgs from the master
    '''
    pass

def builder_states(builders):
    '''
    Retrieve the state of the builders
    '''
    for builder in builders:
        url = 'http://' + builder['url'] + '/builder_state.qjz'
        try:
            fn_ = urllib.request.urlretrieve(url)[0]
        except:
            pass
