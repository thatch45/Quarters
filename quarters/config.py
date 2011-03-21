import yaml
import os
import sys

def read_config( filename ):
    '''
    robust config reader
    '''
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
    
    with open( filename ) as file:
        conf = yaml.load( file )

    if conf:
        builder.update(conf)

    return builder
