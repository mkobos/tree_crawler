#!/usr/bin/env python

import sys
import os
import os.path
import datetime

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
now = datetime.datetime.now()
sleep_time = (now + datetime.timedelta(seconds=4), 
	now + datetime.timedelta(seconds=9))
sleep_time_str = ("{}:{}:{}".format(sleep_time[0].hour, sleep_time[0].minute, sleep_time[0].second), 
	"{}:{}:{}".format(sleep_time[1].hour, sleep_time[1].minute, sleep_time[1].second))
pages_per_second_download_limit = 4

os.system('python {script_dir}/sample_download_crawler.py -v -v --log_file "{script_dir}/../tmp/log.txt" --max_pages_per_second {download_limit} --daily_schedule {activity_start}-{activity_end} "{script_dir}/../tmp/state.xml" "file://{script_dir}/crawler/test/data/original_site/issues_1.html" "{script_dir}/../tmp/download" '.format(download_limit=pages_per_second_download_limit, script_dir=script_dir, activity_start=sleep_time_str[1], activity_end=sleep_time_str[0]))
print "\nNote that the information printed above about problems during tree exploration is expected. It stems from the fact that some of the pages we want to download from our testing web site are missing."
