from quarters.jobdescription import JobDescription
import uuid
import os
import urllib.request

class SVN:
    ''' an scm that fetches new jobs based on new entries from the aur rss feed '''
    def __init__( self, config ):
        self.prev_pkgname = ''
        self.config = config
        self.master = config[ 'master' ]
        self.master_port = config[ 'master_port' ]
        self.master_root = config[ 'master_root' ]
        self.svn_root = config[ 'svn_root' ]

    def get_jobs( self ):
        ''' returns a list of new jobdescriptions '''
        ret = []
        svnup_cmd = [ 'svn', 'up' ]
        pkgs = set()

        with subprocess.Popen( svnup_cmd, cwd=self.svn_root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT ) as proc:
            lines = proc.communicate()[0].splitlines()
            #return_code = proc.returncode

        # find unique pkgnames
        for line in lines[0:-1]:
            pkgname = line.split('/')[1]
            pkgs.add( pkgname )

        makepkg_cmd = [ 'makepkg', '--source' ]
        for pkg in pkgs:
            new_ujid = str( uuid.uuid4() )

            # create a srcpkg
            pkg_path = '/var/tmp/quarters/svn-packages/' + pkg + '/trunk'
            subprocess.Popen( makepkg_cmd, cwd=pkg_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
            # TODO: find a pythonic way of doing this
            srcpkg_path = '/var/tmp/quarters/srcpkgs' + new_ujid + '.src.tar.gz'
            mvcmd = '/bin/mv -f ' + pkg_path + '/' + pkg + '*.src.tar.gz ' + srcpkg_path
            mv_return_code = subprocess.call( mvcmd , shell=True )
            # job description: ujid, cur_pkgname, pkgsrc, sha256sum of srcpkg, architecture to build (x86_64,i686,any)
            # TODO fill in sha256sum
            jd = JobDescription( new_ujid, pkgname, 'file:///var/tmp/quarters/svn-packages/' + pkg + '/trunk/' + new_ujid + '.src.tar.gz', 'sha256sumgoeshere', 'x86_64' )
            ret.append( jd )

        return ret
