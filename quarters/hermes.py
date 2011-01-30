import threading
import urllib.request
#import utils

class Hermes( threading.Thread ):
    '''

    used to fetch state information from https servers

    '''

    # FIXME: how to implement this? should it work like the joboverlord?
    def __init__( self, state_url ):
        threading.Thread.__init__( self )
        self.state_url = state_url

    def run( self ):
#        utils.download( state_url )
        state  = urllib.request.urlopen( state_url )
