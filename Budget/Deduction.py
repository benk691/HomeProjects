from decimal import Decimal
from General.static_vars import static_vars
from General.Common import TWOPLACES, setContext, ErrorMsg
from General.Action import Action
from General.Event import Event, TIME_KEY

class Deduction:
	def __init__(self, category, product, savings, amountPaid, totalCost, repetitionString, dueDateTimestamp):
		'''
		Initializes a specific deduction
		@param category - The main category the deduction falls under
		@param product - The name of the product associated with the deduction
		@param savings - The amount of money saved for paying off the deduction
		@param amountPaid - The amount paid for the deduction
		@param totalCost - The total amount of money the deduction costs
		@param repetitionString - The string that represents how often the deduction occurs
		@param dueDateTimestamp - The next due date that this deduction will occur
		'''
		setContext()
		self.category = category
		self.product = product
		self.savings = Decimal(savings)
		self.amountPaid = Decimal(amountPaid)
		self.totalCost = Decimal(totalCost)
		self.repetitionString = repetitionString
		self.dueDateTimestamp = dueDateTimestamp
		self.event = Event("{0}_{1}".format(category, product))
		self.event.addDate(self.dueDateTimestamp, self.repetitionString)
		self.debt = Decimal("0.0")
		self._calls = 0
		self._createActions()

	def deposit(self, amount):
		'''
		Deposits money into the deduction
		@param amount - the amount of money to deposit
		'''
		amount = Decimal(amount)
		pass

	def withdraw(self, amount):
		'''
		Withdraws money from the deduction
		Withdrawing could mean that you are reallocationg funds somewhere else so this
		does not assume you are paying off anything
		@param amount - the amount of money to withdraw
		'''
		amount = Decimal(amount)
		if amount >= self.savings:
			self.debt += self.savings - amount
			self.savings = Decimal("0.00")
			return self.debt
		else:
			self.savings -= amount
		return self.savings

	def pay(self, amount, executeCalling=False):
		'''
		This is a special third option where you withdraw and then pay 
		part of the total cost
		@param amount - the amount of money to withdraw and pay off
		'''
		if amount != self.totalCost:
			# Don't bother paying off until the amount is the total cost
			# The deduction manger will call this as soon as amount paid 
			# is equal to the total cost (This is how [partial amounts are handled])
			ErrorMsg("Can't pay off a partial amount, pay off the whole thing.")
		# Attribute teh amount to being paid off
		if amount >= self.savings:
			self.amountPaid += self.savings
		else:
			self.amountPaid += amount

		# Check whether this is paid off, if so perform the execution of the 
		# event to repeat
		#if self.amountPaid >= self.totalCost:
		if not executeCalling:
			self._calls = 0
			self.event.execute()

		# To avoid code depluication withdraw the amount now
		return self.withdraw(amount)

	def status(self):
		'''
		Reports the status of the deduction
		'''
		print "\t{0}: ${1} / ${2} (Due Dates: {3})".format(self.product, 
			self.savings.quantize(TWOPLACES), self.totalCost.quantize(TWOPLACES),
			self.dueDateTimestamp)

	def update(self):
		'''
		Updates the deduction
		'''
		pass

	def _multipleExectionAction(self):
		'''
		If the execution starts being performed multiple times if the date is late
		'''
		if self._calls > 0:
			# We need to execute this multiple times so keep reaching into the savings
			# and we need to pay off the total cost each time we are late
			self.pay(self.totalCost, executeCalling=True)
		else:
			self._calls +=1

	def _payoffAction(self):
		'''
		Performs the action of paying off the totalCost
		'''
		self.amountPaid = Decimal("0.00")
		# There should only be one date associated with this event
		self.dueDateTimestamp = self.event.dateList[0][TIME_KEY]

	def _createActions(self):
		'''
		Creates the actions for the event for this deduction
		'''
		payoffAction = Action(self._payoffAction)
		multipleExectionAction = Action(self._multipleExectionAction)
		self.event.addAction(payoffAction)
		self.event.addAction(multipleExectionAction)

	def _toStr(self):
		'''
		Converts the deduction into CSV form to get written back into the file
		'''
		return "{0},{1},{2},{3},{4},{5},{6}".format(self.category, self.product, 
			self.savings.quantize(TWOPLACES), self.totalCost.quantize(TWOPLACES),
			self.repetitionString, self.dueDateTimestamp)

	def __repr__(self):
		return self._toStr()

	def __str__(self):
		return self._toStr()

