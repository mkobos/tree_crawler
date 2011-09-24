#!/usr/bin/env python

from distutils.core import setup

setup(
    name='ConcurrentTreeCrawler',
    version='0.7.1',
    author='Mateusz Kobos',
    author_email='mateusz@mkobos.com',
    packages=['concurrent_tree_crawler', 
    	'concurrent_tree_crawler.html_multipage_navigator',
    	'concurrent_tree_crawler.html_multipage_navigator.cmdln'],
    scripts=['bin/make_documentation.sh', 'bin/run_sample_crawler.sh',
    	'bin/run_sample_download_crawler.py', 'bin/run_tests.py'],
    url='http://pypi.python.org/pypi/ConcurrentTreeCrawler/',
    license='MIT-LICENSE.txt',
    description='A generic concurrent tree crawling algorithm with a sample implementation for website crawling.',
    long_description=open('README.markdown').read(),
    install_requires=[
        "nose",
        "mechanize",
    ],
)
