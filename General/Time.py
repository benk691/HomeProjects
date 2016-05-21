import calendar, datetime, time

class Time:
	pattern = '%Y-%m-%d_%H:%M:%S'

	def __init__(self, timestamp):
		'''
		@param timestamp - string in the format of %Y-%m-%d_%H:%M:%S
		'''
		self.dateTime = None
		self._readTimestamp(timestamp)

	@classmethod
	def fromDatetime(cls, inDatetime):
		'''
		Constructs a Time class from a datetime
		@param timestamp - string in the format of %Y-%m-%d_%H:%M:%S
		@return Constructed Time class
		'''
		timestamp = '%d-%02d-%02d_%02d:%02d:%02d' % (inDatetime.year, inDatetime.month, 
			inDatetime.day, inDatetime.hour, inDatetime.minute, inDatetime.second)
		return Time(timestamp)

	def applyTimeDelta(self, weeks=0, days=0, hours=0, minutes=0, seconds=0):
		'''
		Applies a time delta with the passed in parameters
		NOTE:
		Figuring out months and years gets complicated
		'''
		delta = datetime.timedelta(weeks=weeks, days=days, hours=hours, 
			minutes=minutes, seconds=seconds)
		self.dateTime += delta

	def changeTime(self, years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0):
		'''
		Adds time to the current time by the passed in values. 
		The values are added so if you want to go in the past then pass in 
		negative values
		NOTES:
		* This does not subtract time (maybe a future enhancement)
		* This assumes months will not be greater than 11
		* This assumes no other thing is over the greater time quantity 
		  (ie: seconds won't be greater than 60 you are expected to add a minute)
		'''
		timestamp = ''
		# Handle months
		while months >= 12:
			years += 1
			months -= 12

		if (self.dateTime.month + months) > 12:
			months = (self.dateTime.month + months) % 12
			if months == 0:
				months += 1
			self.dateTime = self.dateTime.replace(year=self.dateTime.year + 1, month=months)
			timestamp = '{0}-{1}-{2}_{3}:{4}:{5}'.format(self.dateTime.year + years, self.dateTime.month, 
				self.dateTime.day, self.dateTime.hour, self.dateTime.minute, self.dateTime.second)
		else:
			timestamp = '{0}-{1}-{2}_{3}:{4}:{5}'.format(self.dateTime.year + years, self.dateTime.month + months, 
				self.dateTime.day, self.dateTime.hour, self.dateTime.minute, self.dateTime.second)

		tmpDateTime = self._constructDateTime(timestamp)

		diff = tmpDateTime - self.dateTime

		days += diff.days
		seconds += diff.seconds

		self.applyTimeDelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
		
	def _readTimestamp(self, timestamp):
		'''
		Reads in a timestamp that is in the format %Y-%m-%d_%H:%M:%S, and converts
		it into an epoch time and a time struct
		@param timestamp - string with a date in the format of %Y-%m-%d_%H:%M:%S
		'''
		self.dateTime = self._constructDateTime(timestamp)

	def _constructDateTime(self, timestamp):
		'''
		Constructs a datetime object from a timestamp
		@param timestamp - string with a date in the format of %Y-%m-%d_%H:%M:%S
		@return datetime corresponding to the timestamp
		'''
		timeStruct = time.strptime(timestamp, Time.pattern)
		epoch = time.mktime(timeStruct)
		return datetime.datetime.fromtimestamp(epoch)

	def _toStr(self):
		'''
		Converts Time class into a string in the format of %Y-%m-%d_%H:%M:%S
		'''
		return '%d-%02d-%02d_%02d:%02d:%02d' % (self.dateTime.year, self.dateTime.month, 
			self.dateTime.day, self.dateTime.hour, self.dateTime.minute, self.dateTime.second)

	def __eq__(self, rhs):
		return self.dateTime == rhs.dateTime

	def __lt__(self, rhs):
		return self.dateTime < rhs.dateTime

	def __le__(self, rhs):
		return self.dateTime <= rhs.dateTime

	def __gt__(self, rhs):
		return self.dateTime > rhs.dateTime

	def __ge__(self, rhs):
		return self.dateTime >= rhs.dateTime
	
	def __repr__(self):
		return self._toStr()

	def __str__(self):
		return self._toStr()


