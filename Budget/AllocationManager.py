from decimal import Decimal
from Allocation import Allocation
from General.Common import DebugMsg, ErrorMsg, WarningMsg, InfoMsg, EXTRA_KEY, DEBT_KEY, TWOPLACES, setContext
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
		# Handle debt first
		currentAmount = self._handleDebt(amount)
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
			cat = self.withdrawMenuList[choice - 1]
			if cat == DEBT_KEY:
				WarningMsg("You can not withdraw money from your debt!")
				return
			amount = Decimal(raw_input("How much money did you spend? "))
			amount = self.allocationMap[cat].withdraw(amount)
			if amount < Decimal("0.00"):
				# We are in debt here so recalculate the total debt
				self._calculateDebt()
				WarningMsg("You have accumulated a debt of ${0}!".format(self.allocationMap[DEBT_KEY].debt.quantize(TWOPLACES)))

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

	def _handleDebt(self, amount):
		if self.allocationMap[DEBT_KEY].debt < Decimal("0.00"):
			debt = self.allocationMap[DEBT_KEY].debt
			posDebt = self.allocationMap[DEBT_KEY].debt * -1
			if posDebt > amount:
				ErrorMsg("You have accumulated more debt than you have deposited! You need ${0} more to resolve your debt!".format(((debt + amount) * -1).quantize(TWOPLACES)))
			amount += self.allocationMap[DEBT_KEY].debt
			self.allocationMap[DEBT_KEY].debt = Decimal("0.00")
			InfoMsg("Debt resolved. Depositing ${0}.".format(amount.quantize(TWOPLACES)))
		return amount

	def _calculateDebt(self):
		'''
		This functino is needed because the debt might occur in the same allocation twice and this will
		resolve that issue by calculating the debt from 0.
		'''
		self.allocationMap[DEBT_KEY].debt = self.allocationMap[DEBT_KEY].debtReg
		for cat in self.allocationMap:
			if cat != DEBT_KEY:
				self.allocationMap[DEBT_KEY].debt += self.allocationMap[cat].debt

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


