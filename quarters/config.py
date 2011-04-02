import yaml
import os
import sys

def read_config( filename ):
    '''
    robust config reader
    '''
    builder = {
               'master': '',
               'master_port': '',
               'builders': [],
               'builder_port': '',
               'chroots': 1,
               'builder_root': '/var/tmp/quarters/builder',
               'chroot_root': '/var/tmp/quarters/chroots',
               'master_root': '/var/tmp/quarters/master',
               'svn_root': '/var/cache/quarters/svn',
              }
    
    with open( filename ) as file:
        conf = yaml.load( file )

    if conf:
        builder.update(conf)

    return builder
