'''
The quarters.https module provides two main things, the https server that is
used to post communication information with the builder, and the communication
calls to retrive the json from the master and builders.
'''
# Import python modules
import os
import socket
import socketserver
import http.server
import urllib.request
import zlib
import json
import random
import multiprocessing
import subprocess
# Import third party modules
import OpenSSL
# Import quarters modules
#import quarters.config

class SecureHTTP(socketserver.ThreadingMixIn, http.server.HTTPServer):
    def __init__(self, pem, server_addr, HandlerClass):
        socketserver.BaseServer.__init__(self, server_addr, HandlerClass)
        ctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
        if not os.path.isfile(pem):
            ssl_cmd = 'openssl req -new -x509 -keyout ' + pem + ' -out '\
                    + pem + ' -days 365 -nodes'
            print(ssl_cmd)
            subprocess.call(ssl_cmd, shell=True)
        ctx.use_privatekey_file(pem)
        ctx.use_certificate_file(pem)
        self.socket = OpenSSL.SSL.COnnection(ctx,
            socket.socket(self.address_family, self.socket_type))

        self.server_bind()
        self.server_activate()


class SecureHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)


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

def serve_http():
    server_address = ('', 443)
    httpd = SecureHTTP('server.pem', server_address, SecureHTTPRequestHandler)
    sa = httpd.socket.getsockname()
    httpd.serve_forever()


if __name__ == '__main__':
    serve_http()
