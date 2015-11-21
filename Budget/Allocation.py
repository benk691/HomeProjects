from decimal import Decimal
from General.Common import WarningMsg, ErrorMsg, TWOPLACES, setContext
from General.Menu import Menu

class Allocation:
	def __init__(self, cat, percent, priority, product=None, savings=None, totalCost=None, isSubAlloc=False):
		# Whether this is a allocation or not
		setContext()
		self._isSubAlloc = isSubAlloc
		self.category = cat
		self.percent = Decimal(percent) / Decimal("100.00")
		self.priority = int(priority)
		self.product = product
		self.savings = None if savings == None else Decimal(savings)
		self.totalCost = None if totalCost == None else Decimal(totalCost)
		# If there are no suballocations then everything goes into extra money 
		self.extraMoney = Decimal("0.00")
		self.debt = Decimal("0.00")
		self.subAllocs = []

	###################################################################################################
	#                                  GENERAL FUNCTIONS                                              #
	###################################################################################################
	def addSubAllocation(self, cat, product, percent, priority, savings, totalCost):
		'''
		Adds a suballocation to start saving towards for this allocation
		'''
		subAlloc = Allocation(cat=cat, product=product, percent=percent, priority=priority, savings=savings, totalCost=totalCost, isSubAlloc=True)
		self.subAllocs.append(subAlloc)
	
	def deposit(self, amount):
		'''
		Deposits the money directly into this allocation which will split it into the suballocations
		'''
		if amount <= Decimal("0.00"):
			return amount # Nothing left to deposit

		if not self._isSubAlloc:
			# Sort the suballocations by priority first
			self.subAllocs = sorted(self.subAllocs, reverse=True)
			amount = self._depositAlloc(amount)
			# We are done allocating to the general allocation so everything left over is extra
			self.extraMoney += amount
			amount = Decimal("0.00")
		# If this is a suballocation deposit it directly
		else:
			amount = self._depositSubAlloc(amount)

		return amount

	def withdraw(self, amount):
		'''
		Withdraws money directly from this allocation if this allocation has suballocations then check 
		which suballocation to pull from
		'''
		if amount <= Decimal("0.00"):
			return amount # Nothing to withdraw
		if not self._isSubAlloc:
			self._withdrawAlloc(amount)
			'''
			if amount < Decimal("0.00"):
				# TODO: FIX
				WarningMsg("Withdrew more than in allocation, taking ${0} out of extra reserve!".format(-1 * amount))
				if self.extraMoney > Decimal("0.00"):
					self._withdrawFromExtra(-1 * amount)
			'''
		# If this is a suballocation deposit it directly
		else:
			# If amount comes back negative than we handle it in the main allocation
			self._withdrawSubAlloc(amount)

		return self.debt if self.debt < Decimal("0.00") else self.extraMoney

	def status(self):
		'''
		Reports the full status of the allocation
		'''
		if not self._isSubAlloc:
			self._statusAlloc()
		else:
			self._statusSubAlloc()

	def update(self):
		'''
		Updates information like percentage or priority of this allocation
		'''
		if not self._isSubAlloc:
			self._updateAlloc()
		else:
			self._updateSubAlloc()

	###################################################################################################
	#                                ALLOCATION FUNCTIONS                                             #
	###################################################################################################
	def _depositAlloc(self, amount):
		currentAmount = amount
		for subAlloc in self.subAllocs:
			retAmount = Decimal("0.00")
			deduction = amount * subAlloc.percent
			if deduction >= currentAmount:
				# This is the last of the money so if we go over we only put what we have left over
				retAmount = subAlloc.deposit(currentAmount)
				currentAmount = retAmount
				if currentAmount == Decimal("0.00"):
					# stop here can't deposit anymore
					return currentAmount
			else:
				subAlloc.deposit(deduction)
				currentAmount -= deduction
		return currentAmount

	def _withdrawAlloc(self, amount):
		# Check if we even have suballocations to worry about
		if len(self.subAllocs) > 0:
			menu = Menu()
			for subAlloc in self.subAllocs:
				menu.addOption(subAlloc.product, subAlloc.withdraw, amount)
			menu.addOption("Extra", self._withdrawFromExtra, amount)
			print "What suballocation did you spend the money on?"
			choice = menu.run()
		else:
			amount = self._withdrawFromExtra(amount)
		return amount

	def _withdrawFromExtra(self, amount):
		if amount > self.extraMoney:
			self.debt += self.extraMoney - amount
			self.extraMoney = Decimal("0.00")
			return self.debt
		else:
			self.extraMoney -= amount
		return self.extraMoney

	def _statusAlloc(self):
		totalPercent = Decimal("0.00")
		print "{0} {1} ({2}%) {3}".format('-' * 5, self.category, (self.percent * 100).quantize(TWOPLACES), '-' * 5)
		for subAlloc in self.subAllocs:
			subAlloc.status()
			totalPercent += subAlloc.percent
		print '\tExtra: ${0}'.format(self.extraMoney.quantize(TWOPLACES))
		print '\tPercent allocated to savings: {0}/100%'.format((totalPercent * 100).quantize(TWOPLACES))

	def _updateAlloc(self):
		pass

	###################################################################################################
	#                               SUBALLOCATION FUNCTIONS                                           #
	###################################################################################################
	def _depositSubAlloc(self, amount):
		# Check to see if we have saved enough
		if self.savings >= self.totalCost:
			return amount
		# Add the full amount on, it is ok if we go over here, 
		# extra money will filter back into the allocation
		self.savings += amount
		return Decimal("0.00")

	def _withdrawSubAlloc(self, amount):
		if amount > self.savings:
			self.debt = self.savings - amount
			self.savings = Decimal("0.00")
			return self.debt
		else:
			self.savings -= amount
		return self.savings

	def _statusSubAlloc(self):
		diff = self.totalCost - self.savings
		print '\t{0}: ${1} / ${2} (${3} until goal)'.format(self.product, self.savings.quantize(TWOPLACES), self.totalCost.quantize(TWOPLACES), diff.quantize(TWOPLACES))

	def _updateSubAlloc(self):
		pass

	###################################################################################################
	#                                  SPECIFIC FUNCTIONS                                             #
	###################################################################################################
	def _allocStr(self):
		return "{0},{1},{2}\n".format(self.category, (self.percent * Decimal("100.00")).quantize(TWOPLACES), self.priority)

	def _suballocStr(self):
		return "{0},{1},{2},{3},{4},{5}\n".format(self.category, self.product, (self.percent * Decimal("100.00")).quantize(TWOPLACES), 
			self.priority, self.savings.quantize(TWOPLACES), self.totalCost.quantize(TWOPLACES))

	'''
	Comparisons done here are on the priority of an allocation. 0 being the highest possible priority.
	'''
	def __lt__(self, rhs):
		return self.priority > rhs.priority

	def __le__(self, rhs):
		return self.priority >= rhs.priority

	def __gt__(self, rhs):
		return self.priority < rhs.priority

	def __ge__(self, rhs):
		return self.priority <= rhs.priority

	def __repr__(self):
		return str(self)

	def __str__(self):
		'''
		Properly converts class into a CSV string depending on whether it is a regular allocation
		or a suballocation
		'''
		return self._allocStr() if not self._isSubAlloc else self._suballocStr()

