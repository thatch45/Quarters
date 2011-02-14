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
import quarters.pkgbuild

class SVN:
    '''
    Manage svn repos
    '''
    def __init__(self, opts, pacman):
        self.opts = opts
        self.pacman = pacman
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

    def _find_pkgbuilds(self, base, lines):
        '''
        Takes a list of stings as output from the svn commands and finds which
        lines are pkgbuilds.
        '''
        ret = []
        for line in lines:
            if line.startswith('Checked'):
                continue
            fn_ = line.split()[1]
            if fn_.endswith('PKGBUILD'):
                ret.append(os.path.join(base, fn_))
        return ret

    def _update_repos(self):
        '''
        Prepare the reposiroties, return dict with repo information:
        {'<repo dir>': {'last_rev': '<last revision number>',
                         'files': '<list of files changed since last revision>'}
        '''
        repo_info = {}
        for base in self.roots:
            repo_info[base] = {}
            if not os.path.isdir(base):
                # checkout the repo
                co_cmd = 'svn co ' + self.roots[base] + ' ' + base
                lines = bytes.decode(subprocess.getoutput(co_cmd)).splitlines()
                repo_info[base]['last_rev'] = None
                repo_info[base]['files'] = self._find_pkgbuilds(base, lines)
            else:
                # Check the release numbers and run an update
                l_cmd = 'svn info ' + base + " | grep Revision: | awk '{print $2}'"
                l_rev = int(subprocess.getoutput(i_cmd).strip())
                repo_info['last_rev'] = str(l_rev)
                r_cmd = 'svn info ' + self.roots[base] + " | grep Revision: | awk '{print $2}'"
                r_rev = int(subprocess.getoutput(r_cmd).strip())
                if r_rev > l_rev:
                    # The local repo is out of date, update!
                    u_cmd = 'svn up ' + base
                    lines = bytes.decode(subprocess.getoutput(u_cmd)).splitlines()
                    repo_info[base]['files'] = self._find_pkgbuilds(base, lines)
        return repo_info

    def fresh_pkgs(self):
        '''
        Return a dict of all packages that need to be built!
        {'<package name>': {'version': '<pkgver>',
                            'deps': '<unavailable deps>'}
        '''
        # Things to check:
        # PKGBUILD version vs the bin version
        # If there is a corresponding bin_pkg
        # Get a list of package deps, and list only the ones that cannot be met
        repo_info = self._update_repos()
        bin_pkgs = self.pacman.repo_pkgs()
        pkgs = {}


