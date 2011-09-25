#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='concurrent_tree_crawler',
    version='0.7.1',
    author='Mateusz Kobos',
    author_email='mateusz@mkobos.com',
    packages=find_packages(),
    include_package_data = True, ## Include non-source code files (which have to be additionally specified in `MANIFEST.in` file)
    scripts=['bin/make_documentation.sh', 'bin/run_sample_crawler.sh',
    	'bin/run_sample_download_crawler.py', 'bin/run_tests.py'],
    url='http://github.com/mkobos/tree_crawler',
    license='MIT-LICENSE.txt',
    description='A generic concurrent tree crawling algorithm with a '\
    	'sample implementation for website crawling.',
    long_description=open('README.markdown').read(),
    install_requires=[
        "nose",
        "mechanize",
    ],
    test_suite='nose.collector', ## Add ability to run tests in the code through the setup.py script
)
