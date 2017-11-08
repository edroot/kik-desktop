from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kik_desktop',

    version='0.0.1',

    description='Kik Desktop',
    long_description=long_description,

    url='https://github.com/Jaapp-/kik-desktop',

    author='Jaap Heijligers',
    author_email='mail@heijligers.me',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],

    keywords='kik desktop im',

    packages=find_packages(exclude=['docs', 'test']),

    install_requires=['PyQt5', 'appdirs'],

    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={
        'kik_desktop': [],
    },

    entry_points={
        'console_scripts': [
            'kik-desktop=kik_desktop.app:execute',
        ],
    },
)
