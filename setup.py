import os
import sys
from codecs import open
from os import path

from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kik_desktop',

    version='0.0.4',

    description='Kik Desktop',
    long_description=long_description,

    url='https://github.com/Jaapp-/kik-desktop',

    author='Jaap Heijligers',
    author_email='mail@heijligers.me',

    license='GPLv2',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',

        'Intended Audience :: End Users/Desktop',

        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        'Topic :: Communications :: Chat',
    ],

    keywords='kik desktop chat',

    install_requires=['PyQt5', 'appdirs', 'kik-unofficial'],

    executables = [
        Executable("kik_desktop/app.py",
            icon="icon/ic_launcher.ico",
            targetName="Kik Desktop.exe",
            shortcutName="Kik Desktop",
            shortcutDir="StartMenuFolder"
            )
        ]
)
