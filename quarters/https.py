'''
The quarters.https module provides two main things, the https server that is
used to post communication information with the builder, and the communication
calls to retrive the json from the master and builders.
'''
# Import python modules
import urllib.request
import zlib
import json
import random
# Import quarters modules
import quarters.config

def master_url():
    '''
    Retrive the master url from the configuration
    '''

def master_state():
    '''
    Download the master state file and translate the data to a structure
    '''

def build_pkgs():
    '''
    Download the build_pkgs from the master
    '''

def builder_states():
    '''
    Retrieve the state of the builders
    '''
    for builder in <builders>:
        url = 'http://' + builder['url'] + '/builder_state.qjz'
        try:
            fn_ = urllib.request.urlretrieve(url)[0]
        except:
            pass
