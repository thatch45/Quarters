'''
Quarters pacman utilities
'''
import os
import subprocess

def find_deps(pkgbuild):
    '''
    Pkgbuild parser, parses the pkgbuild for the variables we care about.
    '''
    deps = []
    if not os.path.exists(pkgbuild):
        return deps
    for line in open(pkgbuild, 'r').readlines():
        line = line.strip()
        if line.startswith('#'):
            continue
        # Look for things we care about
        root = line.split('=')[0]
        if root == 'makedepends' or root == 'depends':
            comps = line.split('=')
            if len(comps) < 2:
                continue
            deps = comps[1].strip('(').strip(')').split()
            for dep in deps:
                dep = dep.strip('"')
                dep = dep.strip("'")
                deps.append(dep)
    return deps

class Pacman:
    '''
    Pacman calls need to occur to track the state data of the active pacman 
    environments, this class is used to track these interactions and is used
    to ensure that they occur in an up to date issolated environment.
    '''
    def __init__(self, opts):
        '''
        Creates a pacman object
        '''
        self.opts = opts
        self.last_sync = 0
        self.__setup_env()

    def __setup_env(self):
        '''
        Prepare the 2 arch's pacman environments for executing pacman queries.
        '''
        pass

    def sync_pacman(self):
        '''
        Just run pacman -Sy
        '''
        cmd = 'pacman -Sy'
        subprocess.getoutput(cmd, shell=True)

    def check_packages(self, names, repos):
        '''
        Check to see if the packages are available in a repo. Returns the packages
        that are not available
        Arguments - names - set()
                    repos - []
        returns - names - set()
        '''
        cmd = 'pacman -Sl ' + ' '.join(repos)
        out = subprocess.getoutput(cmd)
        if out.startswith('error:'):
            return names
        pkgs = set()
        for line in out.split('\n'):
            pkgs.add(line.split()[1])
        return names.difference(pkgs)

    def get_pacman_pkgs(self, repos=['core', 'community', 'extra', 'multilib']):
        '''
        Returns a dict of {'pkg_name': 'version'} of all available packages from
        pacman.
        '''
        cmd = 'pacman -Sl ' + repos
        out = subprocess.getoutput(cmd)
        if out.startswith('error:'):
            return names
        pkgs = {}
        for line in out.split('\n'):
            comps = line.split
            pkgs[comps[1]] = comps[2]
        return pkgs

