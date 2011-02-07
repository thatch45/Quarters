#!/usr/bin/python

from distutils.core import setup

setup(name='quarters',
      version='0.0.1',
      description='Arch Linux package build system',
      author='Thomas S Hatch',
      author_email='thatch45@gmail.com',
      url='https://github.com/thatch45/Quarters',
      packages=['quarters'],
      scripts=['scripts/quartermaster',
               'scripts/quarterbuilder'],
      data_files=[('/etc/quarters',
                    ['conf/builder.conf',
                     'conf/master.conf',
                     'conf/openssl.cnf',
                     ]),
                 ],
     )

