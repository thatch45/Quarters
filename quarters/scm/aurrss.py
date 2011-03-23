from quarters.jobdescription import JobDescription
import uuid
import os
import urllib.request

class AURRSS:
    ''' an scm that fetches new jobs based on new entries from the aur rss feed '''
    def __init__( self ):
        self.prev_pkgname = ''

    def get_jobs( self ):
        ''' returns a list of new jobdescriptions '''
        temp = urllib.request.urlopen( 'http://aur.archlinux.org/rss.php' ).read().decode( 'ascii' ).split('\n')[16].split('>')[1].split('<')[0]

        if self.prev_pkgname == temp:
            return []

        self.prev_pkgname = temp
        pkgname = temp
        new_ujid = str( uuid.uuid4() )
        pkgurl = 'http://' + self.master + ':' + str( self.master_port ) + '/' + str( new_ujid ) + '/' + pkgname + '.tar.gz'

        job_path = os.path.join( self.master_root, str( new_ujid ) )
        pkgsrc_path = os.path.join( job_path, pkgname + '.tar.gz' )
        remote_url = 'https://aur.archlinux.org/packages/' + pkgname + '/' + pkgname + '.tar.gz'
        os.makedirs( job_path, exist_ok=True )
        urllib.request.urlretrieve( remote_url, pkgsrc_path )

        # job description: ujid, pkgname, pkgsrc, sha256sum of srcpkg, architecture to build (x86_64,i686,any)
        jd = JobDescription( str( new_ujid ), pkgname, pkgurl, 'sha256sumgoeshere', 'x86_64' )

        return [ jd ]
