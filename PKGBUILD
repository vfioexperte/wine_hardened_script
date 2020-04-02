# Maintainer: vfio_experte
pkgname="wine-security"
pkgver=0.8b
pkgrel=1
pkgdesc="wine-security-script_gui"
arch=( 'x86_64')
url=""
depend=('python' 'protontricks' 'python-pyqt5')
license=('GPL3' )
provides=('vfio_experte')
source=('wine-security::git+https://github.com/vfioexperte/wine_hardened_script#branch=beta')
md5sums=('SKIP')

pkgver() {
  cd "$srcdir/wine-security"
  python3.8 wine_hardened_script_gui.py -version
}
#prepare() {
  
#}

build() { 
   cd "$srcdir/wine-security"
}

package() {
   cd "$srcdir/wine-security"
   python3.8 install.py "$pkgdir/"
}

