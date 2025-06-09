# Maintainer: <pepperplease3@gmail.com>
pkgname=python-calculator
pkgver=1.0.0
pkgrel=1
pkgdesc="Simple calculator built with Python and CustomTkinter"
arch=('any')
url="https://github.com/Pepzer1/python-calculator/tree/aur"
license=('MIT')
depends=('python' 'python-pip')  # системные зависимости
makedepends=('git')              # для сборки, если нужно git
source=("git+https://github.com/Pepzer1/python-calculator.git#branch=aur")
md5sums=('SKIP')

build() {
  cd "$srcdir/$pkgname" || exit 1
  # сборка не требуется
}

package() {
  cd "$srcdir/$pkgname" || exit 1

  # Установка Python-зависимостей в директорию пакета
  pip install --root="$pkgdir" --prefix=/usr -r requirements.txt

  # Сделать файл исполняемым
  chmod +x calculator.py

  # Установка основного скрипта в /usr/bin с именем python-calculator
  mkdir -p "$pkgdir/usr/bin"
  install -Dm755 calculator.py "$pkgdir/usr/bin/python-calculator"

  # Установка иконки
  mkdir -p "$pkgdir/usr/share/icons/hicolor/256x256/apps"
  install -Dm644 python-calculator.png "$pkgdir/usr/share/icons/hicolor/256x256/apps/python-calculator.png"

  # Установка десктоп-файла
  mkdir -p "$pkgdir/usr/share/applications"
  install -Dm644 python-calculator.desktop "$pkgdir/usr/share/applications/python-calculator.desktop"
}
