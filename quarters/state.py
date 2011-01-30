import urllib.request
import threading
import json

class State:
    '''

    base class for states

    implementation: one reader or one writer at a time,
                    could make it multiple readers or one writer
                    at a time in future, might be unnecessary

    '''

    def __init__( self, url, state={} ):
        self.url = url
        self._state = state
        self._statelock = threading.Lock()

    def get( self ):
        self._statelock.acquire()
        temp_state  = self._state
        self._statelock.releaes()

        return temp_state

    def set( self, state ):
        self._statelock.acquire()
        self._state = state
        self._statelock.releaes()

    def update( self ):
        # FIXME: urlopen doesn't do https verification
        json_state = urllib.request.urlopen( url )

        state = json.load( json_state )

        set_state( self, json_state )
