from decimal import Decimal
from Allocation import Allocation
from General.Common import ErrorMsg, EXTRA_KEY, DEBT_KEY, TWOPLACES, setContext
from General.Menu import Menu

class AllocationManager:
	def __init__(self, allocationPath):
		setContext()
		self._allocationPath = allocationPath
		self.allocationMap = dict()
		self.withdrawMenu = Menu()
		self.withdrawMenuList = []
		self._readAllocations()
		self._createWithdrawMenu()

	def addSubAllocation(self, cat, product, percent, priority, savings, totalCost):
		self.allocationMap[cat].addSubAllocation(cat, product, percent, priority, savings, totalCost)

	def deposit(self, amount):
		if amount <= Decimal("0.00"):
			return
		currentAmount = amount
		for cat in self.allocationMap:
			deduction = amount * self.allocationMap[cat].percent
			retAmount = Decimal("0.00")
			if deduction >= currentAmount:
				retAmount = self.allocationMap[cat].deposit(currentAmount)
				currrentAmount = ("0.00")
				# stop here can't deposit anymore
				return
			else:
				retAmount = self.allocationMap[cat].deposit(deduction)

			currentAmount -= deduction

			if retAmount > Decimal("0.00"):
				ErrorMsg("Did not deposit the full amount into category {0}, you have ${0} left!".format(cat, retAmount))

			elif retAmount < Decimal("0.00"):
				ErrorMsg("Over deposited amount into category, you are ${0} in debt!".format(cat, retAmount))

		if currentAmount > Decimal("0.00"):\
			self.allocationMap[EXTRA_KEY].extraMoney += currentAmount
		elif currentAmount < Decimal("0.00"):
			ErrorMsg("Over deposited amount, you are ${0} in debt!".format(currentAmount))

	def withdraw(self):
		print "What did you spend money on?"
		choice = self.withdrawMenu.run()
		if choice != 'q':
			amount = Decimal(raw_input("How much money did you spend? "))
			if amount <= Decimal("0.00"):
				return
			cat = self.withdrawMenuList[choice - 1]
			self.allocationMap[cat].withdraw(amount)

	def status(self):
		totalPercent = Decimal("0.00")
		print "{0} Status {1}".format('=' * 10, '=' * 10)
		for cat in self.allocationMap:
			self.allocationMap[cat].status()
			totalPercent += self.allocationMap[cat].percent
		print "{0}/100% has been allocated.".format(totalPercent.quantize(TWOPLACES) * 100)

	def update(self):
		pass

	def finalize(self):
		self._writeAllocations()

	def _createWithdrawMenu(self):
		for cat in self.allocationMap:
			self.withdrawMenu.addOption(cat)
			self.withdrawMenuList.append(cat)

	def _readAllocations(self):
		with open(self._allocationPath, 'r') as aFile:
			alines = aFile.readlines()
			for i in xrange(len(alines)):
				if i == 0:
					continue
				category, percent, priority = alines[i].strip().split(',')
				self.allocationMap.update({category : Allocation(cat=category, percent=percent, priority=priority)})
		self.allocationMap.update({EXTRA_KEY: Allocation(cat=EXTRA_KEY, percent=Decimal("0.00"), priority=(len(self.allocationMap) + 1))})
		self.allocationMap.update({DEBT_KEY: Allocation(cat=DEBT_KEY, percent=Decimal("0.00"), priority=(len(self.allocationMap) + 1))})

	def _writeAllocations(self):
		with open(self._allocationPath, 'w') as aFile:
			aFile.write("Category,Percentage,Priority\n")
			for cat in self.allocationMap:
				if cat != EXTRA_KEY and cat != DEBT_KEY:
					aFile.write(str(self.allocationMap[cat]))


