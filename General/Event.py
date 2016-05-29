import datetime
from Repetition import Repetition
from Time import Time

TIME_KEY = 'Time'
REP_KEY = 'Rep'

'''
Creates a scehduled event that can reoccur or only occur once
'''
class Event:

	def __init__(self, name):
		'''
		Initialize an event instance
		@param name - the name of the event
		'''
		self.name = name
		self.executionDate = None
		self.dateList = []
		self.actionList = []

	def setExecutionDate(self, timestamp=None):
		'''
		Sets the execution date to execute up to so you can run this event 
		to the future if you need to
		@param timestamp The timestamp of the date and time this event is to occur
		if timestamp is None then the current date is used
		'''
		if timestamp is None:
			currentDatetime = datetime.datetime.today()
			self.executionDate = Time.fromDatetime(currentDatetime)
		else:
			self.executionDate = Time(timestamp)

	def execute(self):
		'''
		How do we check that the event is occurring??
		(a) Give a time frame from point a to b and check
		(b) threaded run
		Go through the Times if the time has past then execute its action and perform its repetition
		until the date has passed the current time
		'''
		if self.executionDate is None:
			self.setExecutionDate()
		for date in self.dateList:
			self._performToCompletion(date)

	def addDate(self, timestamp, repetitionString=None):
		'''
		Adds a date to the event and how often from the date it occurs
		This method adds to a date list
		@param timestamp The timestamp of the date and time this event is to occur
		@param repetitionString a string specifying how often this event will repeat
		TODO: Do you want this as 
		(a) threaded thing always running?
		(b) one time run that does the calcs only when you run the program
		'''
		'''
		Create this time list then a file where you have a day that the event was last 
		accounted for?
		The point is that we want to see how many paychecks you have 
		until the 'Event' occurs and how much we need to deduct
		If the date has no repetition string then when it is executed the actions will be performed once
		and the date will be updated to the current date
		'''
		dateDict = dict()
		dateDict.update({ TIME_KEY : Time(timestamp) })
		if repetitionString is not None:
			dateDict.update({ REP_KEY : Repetition(repetitionString) })
		else:
			dateDict.update({ REP_KEY : False })
		self.dateList.append(dateDict)

	def addAction(self, action):
		'''
		Adds a function callback taht will be performed everytime the event occurs
		@param action Action class
		'''
		self.actionList.append(action)

	def _performToCompletion(self, date):
		'''
		Performs the actions of the event on a the given date until the repetition has 
		caught up with the current date or if there is no repetition
		@param date - the date item from the dateList to perform the event actions on
		'''
		# Check the repeition flag
		if date[REP_KEY]:
			# Keep updating until the date is in the future
			while date[TIME_KEY] <= self.executionDate:
				self._performActions()
				date[REP_KEY].applyRepetition(date[TIME_KEY])
		else:
			# Perform the actions for this event once and update the time to the execution date
			self._performActions()
			date[TIME_KEY] = self.executionDate

	def _performActions(self):
		''' 
		Performs all the actions for this event
		'''
		for action in self.actionList:
			action.execute()



'''
Give a date in the CSV once the event hits that date then it updates the date to when the event should next
occur, when the event is finialized it writes the next date that didn't happen in the pay period
into the CSV file
'''