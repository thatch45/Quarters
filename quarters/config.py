import yaml
import os
import sys

def read_master(filename):
    '''
    robust config reader
    '''
    if not os.path.isfile(filename):
        err = 'The configuration file ' + filename + ' does not exist.'
        sys.stderr.write(err + '\n')
        sys.exit(2)
    master = {
              'builders': [],
              'svn': [],
              'listen': '0.0.0.0',
              'port': 6777,
              'https_root': '/var/cache/quarters/https',
              'pemfile': '/etc/quarters/cert/quarters.pem',
              'disable_https': '',
             }
    
    conf = yaml.load(open(filename, 'r'))
    if conf:
        master.update(conf)
    return master

def read_builder(filename):
    '''
    robust config reader
    '''
    if not os.path.isfile(filename):
        err = 'The configuration file ' + filename + ' does not exist.'
        sys.stderr.write(err + '\n')
        sys.exit(2)
    builder = {
               'master': '',
               'chroots': 1,
               'listen': '0.0.0.0',
               'port': 6777,
               'https_root': '/var/cache/quarters/https',
               'pemfile': '/etc/quarters/cert/quarters.pem',
               'disable_https': '',
              }
    
    conf = yaml.load(open(filename, 'r'))
    if conf:
        master.update(conf)
    return master

