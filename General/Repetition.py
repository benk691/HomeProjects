import re
from Common import WarningMsg, ErrorMsg

'''
This solves the repetition problem by using a repetition string:

#Y#M#W#D#H#I#S (month is M and minute is I)

Every number is followed by a letter the letter specifies 
(year, month, week, day, hour, min, sec) respectively
'''
class Repetition:
	repRe = re.compile(r"\d+[YMWDHISymwdhis]")

	class TimeStruct:
		def __init__(self, y=0, m=0, w=0, d=0, h=0, i=0, s=0):
			'''
			Initialize the time struct
			@param y - years
			@param m - months
			@param w - weeks
			@param d - days
			@param h - hours
			@param i - minutes
			@param s - seconds
			'''
			self.years = y
			self.months = m
			self.weeks = w
			self.days = d
			self.hours = h
			self.minutes = i
			self.seconds = s

		def _toStr(self):
			'''
			Converts class into the string format: #Y#M#W#D#H#I#S 
			(month is M and minute is I)
			'''
			return "{0}Y{1}M{2}W{3}D{4}H{5}I{6}S".format(self.years, self.months, 
				self.weeks, self.days, self.hours, self.minutes, self.seconds)

		def __repr__(self):
			return self._toStr()

		def __str__(self):
			return self._toStr()

	def __init__(self, repetitionString):
		'''
		Initialize a repetition instance
		@param repetitionString - string in the form of #Y#M#W#D#H#I#S 
		(month is M and minute is I)
		'''
		# Variable init
		self._repTimeStruct = None
		self._decodeString(repetitionString)

	def applyRepetition(self, time):
		'''
		Applies the repeition to a time
		@param t - time
		'''
		# Add specified amount of time to the time class passed in
		time.changeTime(self._repTimeStruct.years, self._repTimeStruct.months, 
			self._repTimeStruct.weeks, self._repTimeStruct.days, 
			self._repTimeStruct.hours, self._repTimeStruct.minutes, 
			self._repTimeStruct.seconds)


	def _decodeString(self, repetitionString):
		'''
		Decodes the read in repetition string and puts it into a struct 
		so the program can use it more easily
		@param repetitionString - the repetition string to decode
		'''
		y = 0 # Years
		m = 0 # Months
		w = 0 # Weeks
		d = 0 # Days
		h = 0 # Hours
		i = 0 # Minutes
		s = 0 # Seconds

		# Convert everything to uppercase
		breakdownList = [ b.upper() for b in Repetition.repRe.findall(repetitionString) ]

		# Create some kind of date/time thing to take care of the reoccurrence
		# Do a += in case there are multiple instances of (YMWDHIS) in the string
		for b in breakdownList:
			if b[-1] == 'Y':
				y += int(b[ : -1])
			elif b[-1] == 'M':
				m += int(b[ : -1])
			elif b[-1] == 'W':
				w += int(b[ : -1])
			elif b[-1] == 'D':
				d += int(b[ : -1])
			elif b[-1] == 'H':
				h += int(b[ : -1])
			elif b[-1] == 'I':
				i += int(b[ : -1])
			elif b[-1] == 'S':
				s += int(b[ : -1])
			else:
				# This should never happen, but if it does, it is an error
				ErrorMsg("Repetition: Unknown argument in repetition string: {0}".format(b))

		# Create the reptition time struct to base the repetition on
		self._repTimeStruct = Repetition.TimeStruct(y, m, w, d, h, i, s)

	def __repr__(self):
		return str(self._repTimeStruct)

	def __str__(self):
		return str(self._repTimeStruct)

