import yaml

def read( filename ):
    '''

    robust config reader

    '''

    defaultconfig = {
                      'master'   : '0.0.0.0',
                      'builders' : [
                                     '0.0.0.1',
                                     '0.0.0.2'
                                   ]
                    }

    # file handling
    try:
        with open( filename ) as stream:
            loadedconfig = yaml.load( stream )
        if loadedconfig is None:
            print( 'warning: empty config, using default config' )
            return defaultconfig
    except ( IOError, yaml.YAMLError ) as e:
        print( 'warning: %s, using default config' % e )
        return defaultconfig

    # check if there is something useful in the config
    if 'master' not in loadedconfig and 'builders' not in loadedconfig:
        print( 'warning: master or builders not defined in config, using default config' )
        return defaultconfig
    else:
        print( 'config loaded successfully')
        return loadedconfig
