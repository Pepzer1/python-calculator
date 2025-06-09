# Maintainer: Твоё Имя <pepperplease3@gmail.com>
pkgname=python-calculator
pkgver=1.0.0
pkgrel=1
pkgdesc="Simple calculator built with Python and CustomTkinter"
arch=('any')
url="https://github.com/Pepzer1/python-calculator"
license=('MIT')
depends=('python' 'customtkinter')
source=("git+https://github.com/Pepzer1/python-calculator.git#branch=aur")
md5sums=('SKIP')  # для git-источников md5sums обычно ставят SKIP

build() {
  cd "$srcdir/repo" || exit 1
  # Если нужно, здесь можно запускать setup.py или другие скрипты сборки
}

package() {
  cd "$srcdir/repo" || exit 1
  # Копируем файлы в директорию пакета
  mkdir -p "$pkgdir/usr/bin"
  install -Dm755 protocalc.py "$pkgdir/usr/bin/python-calculator"
  
  # Копируем requirements (если нужно)
  install -Dm644 requirements.txt "$pkgdir/usr/share/python-calculator/requirements.txt"

  # Можно добавить иконку, .desktop, если есть
  mkdir -p "$pkgdir/usr/share/icons/hicolor/256x256/apps"
  install -Dm644 icon.png "$pkgdir/usr/share/icons/hicolor/256x256/apps/python-calculator.png"
  
  mkdir -p "$pkgdir/usr/share/applications"
  install -Dm644 python-calculator.desktop "$pkgdir/usr/share/applications/python-calculator.desktop"
}
