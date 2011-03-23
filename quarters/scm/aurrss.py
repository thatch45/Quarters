from quarters.jobdescription import JobDescription
import uuid
import os
import urllib.request

class AURRSS:
    ''' an scm that fetches new jobs based on new entries from the aur rss feed '''
    def __init__( self, config ):
        self.prev_pkgname = ''
        self.config = config
        self.master = config[ 'master' ]
        self.master_port = config[ 'master_port' ]
        self.master_root = config[ 'master_root' ]

    def get_jobs( self ):
        ''' returns a list of new jobdescriptions '''
        cur_pkgname = urllib.request.urlopen( 'http://aur.archlinux.org/rss.php' ).read().decode( 'ascii' ).split('\n')[16].split('>')[1].split('<')[0]

        if self.prev_pkgname == cur_pkgname:
            return []

        new_ujid = str( uuid.uuid4() )
        pkgurl = 'http://' + self.master + ':' + str( self.master_port ) + '/' + str( new_ujid ) + '/' + cur_pkgname + '.tar.gz'

        job_path = os.path.join( self.master_root, str( new_ujid ) )
        pkgsrc_path = os.path.join( job_path, cur_pkgname + '.tar.gz' )
        remote_url = 'https://aur.archlinux.org/packages/' + cur_pkgname + '/' + cur_pkgname + '.tar.gz'
        os.makedirs( job_path, exist_ok=True )
        urllib.request.urlretrieve( remote_url, pkgsrc_path )

        # TODO verify sha256sum here

        # job description: ujid, cur_pkgname, pkgsrc, sha256sum of srcpkg, architecture to build (x86_64,i686,any)
        jd = JobDescription( str( new_ujid ), cur_pkgname, pkgurl, 'sha256sumgoeshere', 'x86_64' )

        self.prev_pkgname = cur_pkgname

        return [ jd ]
