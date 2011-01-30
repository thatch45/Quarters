import urllib.request

class State:
    '''

    base class for states

    '''

    def __init__( self, url, state={} ):
        self.url = url
        self.state = state

    def fetch_state( self ):
        # download & return json state file here
        # FIXME: urlopen doesn't do https verification
        json_state = urllib.request.urlopen( url ).read()
        return json_state

    def update( self ):
        json_state = fetch_state()

        # do hardcore processing here
