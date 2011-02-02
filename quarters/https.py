'''
The quarters.https module provides two main things, the https server that is
used to post communication information with the builder, and the communication
calls to retrive the json from the master and builders.
'''
# Import python modules
import os
import sys
import socket
import socketserver
import http.server
import urllib.request
import zlib
import json
import random
import ssl
import multiprocessing
import subprocess

class SecureHTTP(socketserver.ThreadingMixIn, http.server.HTTPServer):
    def __init__(self, pem, server_addr, HandlerClass):
        socketserver.BaseServer.__init__(self, server_addr, HandlerClass)
        if not os.path.isfile(pem):
            ssl_cmd = 'openssl req -new -x509 -keyout ' + pem + ' -out '\
                    + pem + ' -days 365 -nodes -config /etc/quarters/openssl.cnf'
            print(ssl_cmd)
            subprocess.call(ssl_cmd, shell=True)
        self.socket = ssl.wrap_socket(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                keyfile=pem,
                certfile=pem)

        self.server_bind()
        self.server_activate()


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

def serve_https(addr, port, basedir='.', pem='server.pem'):
    '''
    Starts up an https server in the designated directory
    '''
    server_address = (addr, port)
    httpd = SecureHTTP(pem,
            server_address,
            http.server.SimpleHTTPRequestHandler)
    sa = httpd.socket.getsockname()
    httpd.serve_forever()

def partner_https(addr, port, basedir, pem):
    '''
    Starts up an https server in a python multiprocess so that it run
    allongside the other opperations
    '''
    multiprocessing.Process(target=serve_https(addr, port, basedir, pem)).start()

if __name__ == '__main__':
    serve_https(sys.argv[1], sys.argv[2])
