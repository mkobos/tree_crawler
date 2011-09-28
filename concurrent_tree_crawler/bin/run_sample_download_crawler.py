#!/usr/bin/env python

import sys
import os
import os.path
import datetime
import urllib

def set_path_to_package_root():
	"""
	Calling this function esures that: 1) if this script is placed inside
	the C{concurrent_tree_crawler} package files, when importing the 
	C{concurrent_tree_crawler} package it uses these package files, 
	2) otherwise, in situation when the script is in some other place and
	we want to use the library C{concurrent_tree_crawler} installed in the
	system, it uses this library when importing the C{concurrent_tree_crawler}.
	"""
	import sys
	import os.path
	sys.path[0]=os.path.join(sys.path[0], '../..')
set_path_to_package_root()

def get_website_address():
	"""
	This function is used to fetch the path to the location of the sample 
	web site from the package.
	"""
	import concurrent_tree_crawler
	package_path = os.path.dirname(concurrent_tree_crawler.__file__)
	url = urllib.pathname2url("{}/test/data/original_site/issues_1.html".\
		format(package_path))
	return "file:"+url

website_address = get_website_address()
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
dst_dir = "./tmp"
now = datetime.datetime.now()
sleep_time = (now + datetime.timedelta(seconds=4), 
	now + datetime.timedelta(seconds=9))
sleep_time_str = ("{}:{}:{}".format(sleep_time[0].hour, sleep_time[0].minute, sleep_time[0].second), 
	"{}:{}:{}".format(sleep_time[1].hour, sleep_time[1].minute, sleep_time[1].second))
pages_per_second_download_limit = 4

os.system('{script_dir}/sample_download_crawler.py -v -v --log_file "{dst_dir}/log.txt" --max_pages_per_second {download_limit} --daily_schedule {activity_start}-{activity_end} "{dst_dir}/state.xml" {website_address} "{dst_dir}/tmp/download" '.format(download_limit=pages_per_second_download_limit, script_dir=script_dir, dst_dir=dst_dir, activity_start=sleep_time_str[1], activity_end=sleep_time_str[0], website_address=website_address))
print "\nNote that if above an information about problems during tree exploration has been printed, it is expected. It stems from the fact that some of the pages we want to download from our testing web site are missing."
