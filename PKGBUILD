# Maintainer: Thomas S Hatch <thatch45@gmail.com>
pkgname=quarters-git
pkgver=20110206
pkgrel=1
pkgdesc="Arch Linux build system"
arch=('any')
url="https://github.com/thatch45/Quarters"
license=('GPL3')
groups=()
depends=('python' 
         'python3-yaml')
makedepends=('git')

_gitroot="git://github.com/thatch45/Quarters.git"
_gitname="Quarters"

build() {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [ -d $_gitname ] ; then
    cd $_gitname && git pull origin
    msg "The local files are updated."
  else
    git clone $_gitroot $_gitname
  fi

  msg "GIT checkout done or server timeout"
  msg "Starting make..."

  rm -rf "$srcdir/$_gitname-build"
  git clone "$srcdir/$_gitname" "$srcdir/$_gitname-build"
  cd "$srcdir/$_gitname-build"

}

package() {
  cd "$srcdir/$_gitname-build"
  python setup.py install --root=$pkgdir/ --optimize=1
} 
