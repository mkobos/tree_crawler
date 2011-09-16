import datetime

class AbstractActivitySchedule:
	"""
	Activity and inactivity time schedule. 
	
	We Assume that the time axis consists of two types of periods: activity and
	inactivity. Each time point belongs either to activity or inactivity 
	period.
	"""
	
	def get_activity_info(self, now=None):
		"""
		@param now: current time, by default, it is the value of
			L{datetime.datetime.now()}
		@type now: L{datetime.datetime}
		@return: activity information relative to C{now}
		@rtype: L{ActivityInfo} 
		"""
		raise NotImplementedError()

class ActivityInfo:
	def __init__(self, is_in_activity_period, time_to_mode_change):
		self.is_in_activity_period = is_in_activity_period
		"""C{True} iff we are in activity period"""
		
		self.future_mode_change = time_to_mode_change
		"""Time (L{date.datetime}) of the closest future mode change 
			(i.e. change from the activity to inactivity period or 
			from inactivity to activity period). It can have C{None} value when
			the mode will not change in the future."""

class AlwaysActiveSchedule(AbstractActivitySchedule):
	def get_activity_info(self, now=None):
		return ActivityInfo(True, None)

class DaySchedule(AbstractActivitySchedule):

	def __init__(self, activity_start_time, activity_end_time):
		"""
		@type activity_start_time: L{datetime.time}
		@type activity_end_time: L{datetime.time}
		"""
		self.__start = activity_start_time
		self.__end = activity_end_time
	
	def __get_closest_event_interval(self, now):
		"""
		Return current event interval (if C{now} lies in event interval) or 
		future closest event interval (if C{now} doesn't lie in event interval)
		
		@param now: current time (L{datetime.datetime})
		@return: (start, end), where both values are of type 
			L{date.datetime}.
		"""
		## Legend to the comments drawings:
		## **** : activity time
		## ---- : inactivity time
		## |0| : 0th hour
		## |23| : 23rd hour
		## |s| : schedule.__start
		## |e| : schedule.__end
		today = now
		tomorrow = today+datetime.timedelta(1)
		yesterday = today-datetime.timedelta(1)
		## |0|----|s|****|e|----|23|
		if self.__start < self.__end :
			if ((today.time() < self.__start) or 
				(today.time() > self.__start and today.time() < self.__end)):
				return (self.__get_datetime(today, self.__start), 
					self.__get_datetime(today, self.__end))
			else:
				return (self.__get_datetime(tomorrow, self.__start), 
					self.__get_datetime(tomorrow, self.__end))
		## |0|****|e|----|s|****|23|
		else:
			if ((today.time() > self.__end and today.time() < self.__start) or 
				today.time() > self.__start):
				return (self.__get_datetime(today, self.__start), 
				 	self.__get_datetime(tomorrow, self.__end))
			else:
				return (self.__get_datetime(yesterday, self.__start), 
					self.__get_datetime(today, self.__end))

	def get_activity_info(self, now=None):
		if now is None:
			now = datetime.datetime.now()
		(start, end) = self.__get_closest_event_interval(now)
		if now < start:
			return ActivityInfo(False, start)
		else:
			return ActivityInfo(True, end)
	
	@staticmethod
	def __get_datetime(date, time_):
		return datetime.datetime(date.year, date.month, date.day, 
			time_.hour, time_.minute, time_.second, time_.microsecond)