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
            # empty config
            return defaultconfig
    except ( IOError, yaml.YAMLError ) as e:
        # file not found, yaml syntax error
        return defaultconfig

    # check if there is something useful in the config
    if 'master' not in loadedconfig and 'builders' not in loadedconfig:
        return defaultconfig
    else:
        return loadedconfig
