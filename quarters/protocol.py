''' file resereved for the communications of master and builder '''

import bz2

def quarters_compress( f ):
    ''' decorator to compress argument '''
    def helper( x ):
        f( bz2.compress( x ) )
    return helper

def quarters_decompress( f ):
    ''' decorator to decompress argument '''
    def helper( x ):
        f( bz2.decompress( x ) )
    return helper
