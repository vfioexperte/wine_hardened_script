# Maintainer: vfio_experte
pkgname="wine-security"
pkgver=1.1a
pkgrel=1
pkgdesc="wine-security"
arch=( 'x86_64')
url=""
license=('GPL2' )
provides=('vfio_experte')
source=('wine_hardened_script_gui.py' 'steam_security.py' 'wine_no_internet.py' 'version' 'install.py')
md5sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')
depends=('python' 'python-pyqt5' 'wine' 'rsync' )
pkgver() {
  cd "$srcdir/"
  cat < version
}
#prepare() {
  
#}

build() { 
   cd "$srcdir/"
}

package() {
   cd "$srcdir/"
   python3.8 install.py "$pkgdir/"
}

