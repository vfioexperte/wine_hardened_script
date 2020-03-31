# Maintainer: vfio_experte
pkgname="wine_hardened_script_gui"
pkgver=0.8b
pkgrel=1
pkgdesc="wine_hardened_script_gui"
arch=( 'x86_64')
url=""
license=('GPL2' )
provides=('vfio_experte')
source=('wine_hardened_script_gui.py' 'steam_security.py' 'install.py')
md5sums=('SKIP' 'SKIP' 'SKIP')

pkgver() {
  cd "$srcdir/"
  python3 wine_hardened_script_gui.py -version
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

