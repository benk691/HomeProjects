import calendar, datetime, time

class Time:
	pattern = '%Y-%m-%d_%H:%M:%S'

	def __init__(self, timestamp):
		'''
		@param timestamp - string in the format of %Y-%m-%d_%H:%M:%S
		'''
		self.timeStruct = None
		self.epoch = None
		self.dateTime = None
		self._readTimestamp(timestamp)

	def applyTimeDelta(self, weeks=0, days=0, hours=0, minutes=0, seconds=0):
		'''
		Applies a time delta with the passed in parameters
		NOTE:
		Figuring out months and years gets complicated
		'''
		delta = datetime.timedelta(weeks=weeks, days=days, hours=hours, 
			minutes=minutes, seconds=seconds)
		print 'delta =', delta
		self.dateTime += delta
		print 'new dateTime =', self.dateTime
		print ''

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
		print 'old dateTime =', self.dateTime
		timestamp = ''
		# Handle months
		while months >= 12:
			years += 1
			months -= 12

		# TODO: Test this case so we can feel comfortable about this
		if (self.dateTime.month + months) > 12:
			months = (self.dateTime.month + months) % 12
			if months == 0:
				months += 1
			self.dateTime = self.dateTime.replace(year=self.dateTime.year + 1, month=months)
			print 'reset dateTime =', self.dateTime
			timestamp = '{0}-{1}-{2}_{3}:{4}:{5}'.format(self.dateTime.year + years, self.dateTime.month, self.dateTime.day, self.dateTime.hour, self.dateTime.minute, self.dateTime.second)
		else:
			timestamp = '{0}-{1}-{2}_{3}:{4}:{5}'.format(self.dateTime.year + years, self.dateTime.month + months, self.dateTime.day, self.dateTime.hour, self.dateTime.minute, self.dateTime.second)

		print 'timestamp =', timestamp
		tmpTimeStruct = time.strptime(timestamp, Time.pattern)
		tmpEpoch = time.mktime(tmpTimeStruct)
		tmpDateTime = datetime.datetime.fromtimestamp(tmpEpoch)

		diff = tmpDateTime - self.dateTime

		days += diff.days
		seconds += diff.seconds

		self.applyTimeDelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)

		'''
		# Add 1 since the start index is 1 and not 0
		years = (years + 1) if years > 0 else datetime.MINYEAR
		years += 1969
		months = (months + 1) if months > 0 else 1
		days = (days + 1) if days > 0 else 1

		# Create a datetime with the given parameters
		changeDate = datetime.datetime(year=years, month=months, day=days, hour=hours, 
			minute=minutes, second=seconds)
		# Create number of seconds this offset is
		changeEpoch = calendar.timegm(changeDate.timetuple())

		print 'changeDate =', changeDate
		print 'changeEpoch =', changeEpoch

		self.applyTimeDelta()
		'''
		

	def _readTimestamp(self, timestamp):
		'''
		Reads in a timestamp that is in the format %Y-%m-%d_%H:%M:%S, and converts
		it into an epoch time and a time struct
		@param timestamp - string with a date in the format of %Y-%m-%d_%H:%M:%S
		'''
		self.timeStruct = time.strptime(timestamp, Time.pattern)
		self.epoch = time.mktime(self.timeStruct)
		self.dateTime = datetime.datetime.fromtimestamp(self.epoch)


