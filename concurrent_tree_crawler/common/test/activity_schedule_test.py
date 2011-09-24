import unittest
import datetime
from concurrent_tree_crawler.common.activity_schedule import DaySchedule

simple_interval = [datetime.time(7, 5, 00), datetime.time(8, 10, 10)]
in_simple = datetime.datetime(2012, 7, 7, 7, 7, 7)
before_simple = datetime.datetime(2012, 7, 7, 7, 4, 7)
after_simple = datetime.datetime(2012, 7, 7, 8, 10, 12)

splitted_interval = [datetime.time(19, 5, 0), datetime.time(6, 10, 10)]
in_splitted_2nd = datetime.datetime(2012, 7, 7, 23, 7, 7)
in_splitted_1st = datetime.datetime(2012, 7, 7, 3, 7, 7)
out_of_splitted = datetime.datetime(2012, 7, 7, 15, 7, 7)

class DayScheduleTestCase(unittest.TestCase):
	def test_simple_interval(self):
		self.__check_activity_info(in_simple ,
			simple_interval[0], simple_interval[1],
			True, datetime.datetime(2012, 7, 7, 8, 10, 10))
		self.__check_activity_info(before_simple, 
			simple_interval[0], simple_interval[1],
			False, datetime.datetime(2012, 7, 7, 7, 5, 0))
		self.__check_activity_info(after_simple, 
			simple_interval[0], simple_interval[1],
			False, datetime.datetime(2012, 7, 8, 7, 5, 0))
		
	def test_splitted_interval(self):
		self.__check_activity_info(in_splitted_2nd, 
			splitted_interval[0], splitted_interval[1], 
			True, datetime.datetime(2012, 7, 8, 6, 10, 10))
		self.__check_activity_info(in_splitted_1st, 
			splitted_interval[0], splitted_interval[1], 
			True, datetime.datetime(2012, 7, 7, 6, 10, 10))
		self.__check_activity_info(out_of_splitted, 
			splitted_interval[0], splitted_interval[1], 
			False, datetime.datetime(2012, 7, 7, 19, 5, 0))
	
#	def test_open_interval(self):
#		self.__check_activity_info(in_simple, None, None, True, None)
#		self.__check_activity_info(in_simple, None, simple_interval[1], 
#			True, simple_interval[1])
#		self.__check_activity_info(after_simple, None, simple_interval[1], 
#			False, None)
#		self.__check_activity_info(in_simple, simple_interval[0], None, 
#			True, None)
#		self.__check_activity_info(before_simple, simple_interval[0], None, 
#			True, simple_interval[0])
	
	def __check_activity_info(self, now, 
		activity_start_time, activity_end_time, 
		expected_is_in_activity_period, expected_future_mode_change):
		
		schedule = DaySchedule(activity_start_time, activity_end_time)
		info = schedule.get_activity_info(now)
		self.assertEqual(expected_is_in_activity_period, 
			info.is_in_activity_period)
		self.assertEqual(expected_future_mode_change, 
			info.future_mode_change)