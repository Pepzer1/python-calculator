# python-calculator (AUR branch)

This branch contains packaging files for the Arch Linux User Repository (AUR) or local installation via `makepkg`.

## About
A simple Python calculator using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).
Installs with a .desktop entry and icon for easy launching from app menus.

For source code and development, see the [main branch](https://github.com/Pepzer1/python-calculator/tree/main).

## Installation (Local)

Clone the repo and build the package:

```bash
git clone --branch aur https://github.com/Pepzer1/python-calculator.git
cd python-calculator
makepkg -si
