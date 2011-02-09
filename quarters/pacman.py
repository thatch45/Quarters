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
        return ret
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
    return ret

def sync_pacman():
    '''
    Just run pacman -Sy
    '''
    cmd = 'pacman -Sy'
    subprocess.call(cmd, shell=True)

def check_packages(names, repos):
    '''
    Check to see if the packages are available in a repo. Returns the packages
    that are not available
    Arguments - names - set()
                repos - []
    returns - names - set()
    '''
    # Figgin pyalpmm looks to be broken! I need to shell out :(
    cmd = 'pacman -Sl ' + ' '.join(repos)
    out = subprocess.Popen(cmd,
        shell=True, 
        stdout=subprocess.PIPE).communicate()[0]
    if out.startswith('error:'):
        return names
    pkgs = set()
    for line in out.split('\n'):
        pkgs.add(line.split()[1])
    return names.difference(pkgs)

def get_pacman_pkgs():
    '''
    Returns a dict of {'pkg_name': 'version'} of all available packages from
    pacman.
    '''
    cmd = 'pacman -Sl core extra community multilib'
    out = subprocess.Popen(cmd,
        shell=True, 
        stdout=subprocess.PIPE).communicate()[0]
    if out.startswith('error:'):
        return names
    pkgs = {}
    for line in out.split('\n'):
        comps = line.split
        pkgs[comps[1]] = comps[2]
    return pkgs


