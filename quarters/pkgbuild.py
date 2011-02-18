'''
This module acts as a minimal pkgbuild parser, we only need a few bits of
information from the PKGBUILD, namely the version, the rel, the top level
name (pkgbase trumps pkgname) and all of the deps.
'''

import os

def parse(PKGBUILD):
    '''
    Parse a PKGBUILD, returns a dict:
    {'pkgname': '<package name>',
     'fullver': '<pkgver+pkgrel>',
     'deps': ['<deps and makedeps>']
    '''
    ret = {}
    ver = ''
    rel = ''
    if not os.path.isfile(PKGBUILD):
        return ret
    for line in open(PKGBUILD, 'r').readlines(): # change this to be index based - a while loop
        # Check for pkgbase
        if line.startswith('pkgbase='):
            ret['pkgname'] = line.split('=')[1].strip("'").strip('(').strip(')')
        if line.find
        if not ret.has_key('pkgname'):
            # Check for all other cases where the the pkgname might pop up
            if line.startswith('pkgname='):
                ret['pkgname'] = line.split('=')[1].strip('(').strip(')').strip("'").strip('"')
        # Look for the version
        if line.startswith('pkgver='):
            ver = line.split('=')[1].strip('(').strip(')'),strip("'").strip('"')
        if line.startswith('pkgrel='):
            rel = line.split('=')[1].strip('(').strip(')'),strip("'").strip('"')
        # Look for deps
