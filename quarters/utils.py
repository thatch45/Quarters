'''
General utilities
'''
import os
import sys
import subprocess
import urllib.request
from hashlib import sha256
import json

def parse_pkgbuild(path):
    '''
    Parse a pkgbuild and reurn the information about it, like this:
    {'_split_': {'base': '<basename>',...},
     '<package_name>': {'pkgver': '<pkgver>',...}
     }
    '''
    workingdir = os.path.dirname(path)
    process = subprocess.Popen(['parsepkgbuild',filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=workingdir)
    data = process.communicate()
    if process.returncode > 0:
        return None
    comps = []
    if '\0' in data[0]:
        comps.extend(data[0].split('\0'))
    else:
        compa.apend(data[0])
    pkgs = []
    for comp in comps:
        pkgs.append(parse_pkg_data(data[0]))
    pkgd = {}
    for pkg in pkgs:
        if pkg.has_key('base'):
            pkgd['_split_'] = pkg
        else:
            pkgd[pkg['name']] = pkg
    return pkgd

def parse_pkg_data(data):
    '''
    Parses the output from parsepkgbuid and returns a dict like this:
    {'pkgver': ['0.1.2'],
     'depends': ['foo', 'bar', 'baz'], ...}
    '''
    pkgd = {}
    val = None
    for line in data.split('\n'):
        if line.startswith('%'):
            val = line.strip('%').lower()
            pkgd[val] = []
        if line.strip() != '':
            pkgd[val].append(line.strip())
    return pkgd

def get_url( url ):
    ''' returns the contents at the url '''
    return urllib.request.urlopen( url ).read()

def sha256sum_file( filename ):
    ''' compute the sha256sum of filename '''
    s = sha256()
    with open( filename, 'rb' ) as f:
        bufsize = 8192
        data = f.read( bufsize )
        while data:
            s.update( data )
            data = f.read( bufsize )
    return s.hexdigest()

def fetch_states( list_of_ips, port ):
    ret = {}
    for ip in list_of_ips:
        url = 'http://' + ip + ':' + str( port ) + '/global_status'

        try:
            json_data = get_url( url )
        except:
           continue

        status = json.loads( json_data.decode('utf-8' ) )

        ret.update( { ip : status } )

    return ret
