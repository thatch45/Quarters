import yaml
import os
import sys

def read_config( filename ):
    '''
    robust config reader
    '''
    if not os.path.isfile(filename):
        err = 'The configuration file ' + filename + ' does not exist.'
        sys.stderr.write(err + '\n')
        sys.exit(2)
    builder = {
              'builders': [],
               'master': '',
               'chroots': 1,
               'listen': '0.0.0.0',
               'port': 6777,
               'https_root': '/var/cache/quarters/https',
               'pemfile': '/etc/quarters/quarters.pem',
               'disable_https': '',
              'svn': [],
              'svn_root': '/var/cache/quarters/svn',
              'git_root': '/var/cache/quarters/git',
              'pacman_root': '/var/cache/quarters/pacman_root',
              }
    
    conf = yaml.load(open(filename, 'r'))
    if conf:
        builder.update(conf)
    return builder
