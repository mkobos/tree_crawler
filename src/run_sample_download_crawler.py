#!/usr/bin/env python

import sys
import os
import os.path

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.system('python {script_dir}/sample_download_crawler.py -V --log "{script_dir}/../tmp/log.txt" --pages_download_limit 10 "file://{script_dir}/crawler/test/data/original_site/issues_1.html" "{script_dir}/../tmp/download" "{script_dir}/../tmp/state.xml"'.format(script_dir=script_dir))
