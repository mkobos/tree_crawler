#!/usr/bin/env python

from setuptools import setup, find_packages
from concurrent_tree_crawler.common.version import get_git_version

setup(
    name='concurrent_tree_crawler',
    version=get_git_version(),
    author='Mateusz Kobos',
    author_email='mateusz@mkobos.com',
    packages=find_packages(),
    include_package_data = True, ## Include non-source code files (which have to be additionally specified in `MANIFEST.in` file)
    url='http://github.com/mkobos/tree_crawler',
    license='MIT-LICENSE.txt',
    description='A generic concurrent tree crawling algorithm with a '\
    	'sample implementation for website crawling.',
    long_description=open('README.rst').read(),
    install_requires=[
        "nose",
        "mechanize",
    ],
    test_suite='nose.collector', ## Add ability to run tests in the code through the setup.py script
    keywords=["concurrent", "tree", "website", "crawler"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Operating System :: OS Independent",
    ],
)
