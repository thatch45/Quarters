'''
The svn module is used to manage svn repositories containing ArchLinux packages
Check out the repo
detect if the repo has been checked out previously
Get a list of all of the packages in the repo
Compare the packages to what pacman can get
check the previous revision
'''
# Import python modules
import os
import subprocess
import hashlib
# Import quarters libs
import quarters.pacman
import quarters.pkgbuild

class SVN:
    '''
    Manage svn repos
    '''
    def __init__(self, opts):
        self.opts = opts
        self.roots = self.__prepare_roots()

    def __prepare_roots(self):
        '''
        The root directories in the cache dir need to be reproducable and
        unique, so we make hashes of the path.
        '''
        roots = {}
        for root in self.opts['svn']:
            b_root = str.encode(root)
            base = hashlib.sha512(b_root).hexdigest()
            roots[os.path.join(self.opts['svn_root'], base)] = root
        return roots

    def _setup_repos(self):
        '''
        Prepare the initial repositories
        '''
        for base in self.roots:
            if not os.path.isdir(base):
                # checkout the repo
                co_cmd = 'svn co ' + self.roots[base] + ' ' + base
                subprocess.getoutput(co_cmd)
            else:
                # Check the release numbers and run an update
                l_cmd = 'svn info ' + base + " | grep Revision: | awk '{print $2}'"
                l_rev = int(subprocess.getoutput(i_cmd).strip())
                r_cmd = 'svn info ' + self.roots[base] + " | grep Revision: | awk '{print $2}'"
                r_rev = int(subprocess.getoutput(r_cmd).strip())
                if r_rev > l_rev:
                    # The local repo is out of date, update!
                    u_cmd = 'svn up ' + base
                    subprocess.getoutput(u_cmd)

    def _get_pkgs(self):
        '''
        Return a dict of all packages that are in svn, but not up to date
        '''
        pass

