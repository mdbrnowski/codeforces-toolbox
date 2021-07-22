#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()
with open('requirements.txt') as f:
    requirements = f.read().split('\n')

setup(
    name='codeforces-toolbox',
    version='1.0.0',
    description='Codeforces CLI that makes writing contests more efficient.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Michał Dobranowski',
    author_email='mdbrnowski@gmail.com',
    url='https://github.com/mdbrnowski/codeforces-tool',
    packages=['cft', 'cft.utils'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: MacOS',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python',
                 'Topic :: Terminals'],
    license='MIT',
    keywords=['cli', 'competitive-programming', 'codeforces'],
    install_requires=requirements,
    python_requires='>=3.7',
    entry_points={'console_scripts': ['cft=cft.main:main']},
)
