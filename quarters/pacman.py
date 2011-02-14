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
        self.roots = self.__setup_env()
        self.repos = self.__grep_repos()
        self.sync_pacman()

    def __setup_env(self):
        '''
        Prepare the 2 arch's pacman environments for executing pacman queries.
        '''
        roots = {'i686': os.path.join(self.opts['pacman_root'], 'i686'),
                 'x86_64': os.path.join(self.opts['pacman_root'], 'x86_64')]
        for root in roots:
            p_dir = os.path.join(roots[root], 'var/lib/pacman')
            if not os.path.exists(roots[root]):
                os.makedirs(roots[root])
            if not os.path.exists(p_dir):
                os.makedirs(p_dir)
            # This needs fixing, so that there is a single pacman.conf that 
            # controls this stuff but is read like a template
            shutil.copy(os.path.join('/etc/quarters/pacman.', root + '.conf' ),
                    os.path.join(roots[root], 'pacman.conf')
        return roots

    def __grep_repos(self):
        '''
        returns the repos that are active in the pacman configurations used
        for the repos
        '''
        repos = {}
        for root in self.roots:
            repos[root] = []
            pac_conf = os.path.join(self.roots[root], 'pacman.conf')
            lines = open(pac_conf, 'r').readlines()
            for line in lines:
                if line.startswith('#'):
                    continue
                if line.startswith('[options]'):
                    continue
                if line.startswith('['):
                    repos[root].append(line.split('[')[1].split(']')[0])
        return repos

    def sync_pacman(self):
        '''
        Just run pacman -Sy for the pacman environments
        '''
        for root in self.roots:
            cmd = 'pacman --root ' + root + ' --config '\
                + os.path.join(self.roots[root], 'pacman.conf') + ' -Sy'
            subprocess.getoutput(cmd, shell=True)

    def repo_pkgs(self):
        '''
        Returns a dict of dictonaries of packages:
        {'<package name>': {'version': '<version>',
                            'repo': '<repo>'}
        '''
        self.sync_pacman()
        pkgs = {}
        for root in self.roots:
            pkgs[root] = {}
            cmd = 'pacman --root ' + root + ' --config '\
                + os.path.join(self.roots[root], 'pacman.conf')\
                + ' -Sl ' + ' '.join(self.repos[root])
            for line in subprocess.getoutput(cmd).splitlines():
                comps = bytes.decode(line).split()
                pkgs[root][comps[1]] = {'repo': comps[0], 'version': comps[2]}
        return pkgs
