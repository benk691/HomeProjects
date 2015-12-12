from decimal import Decimal
from AllocationManager import AllocationManager
from General.Common import InfoMsg, DebugMsg, TWOPLACES, setContext, DEBT_KEY

class MoneyManager:
	def __init__(self, moneyPath, allocationPath, savingsPath):
		setContext()
		self._moneyPath = moneyPath
		self._savingsPath = savingsPath
		# Allocation manager
		self.allocationManager = AllocationManager(allocationPath)
		self._readMoney()
		self._readSavings()

	def deposit(self, amount=None):
		'''
		Deposits money according to the percentages of all the allocations
		'''
		if amount == None:
			amount = Decimal(raw_input("How much money to deposit? "))
		self.allocationManager.deposit(amount)

	def withdraw(self, amount=None):
		'''
		Withdraws money out of an allocation and checks if withdrawal is over budget
		'''
		self.allocationManager.withdraw()		

	def status(self):
		self.allocationManager.status()

	def update(self):
		self.allocationManager.update()

	def calculateSavings(self):
		'''
		Adds the amount in each 
		'''
		bankAccountMoney = Decimal("0.00")
		creditAccountMoney = Decimal("0.00")
		savings = Decimal("0.00")
		bankAccounts = int(raw_input("How many bank accounts do you have? "))
		creditCards = int(raw_input("How many credit cards do you have? "))

		for ba in xrange(bankAccounts):
			baName = raw_input("What is the name of one of your bank accounts? ")
			bankAccountMoney += Decimal(raw_input("How much money is in your {0} account? ".format(baName)))

		for cc in xrange(creditCards):
			ccName = raw_input("What is the name of one of your credit card accounts? ")
			creditAccountMoney += (-1 * Decimal(raw_input("How much money do you owe for your {0} account? ".format(ccName))))

		actualSavings = bankAccountMoney + creditAccountMoney
		budgetSavings = self.allocationManager.calculateSavings()
		InfoMsg("Your actual savings are ${0}.".format(actualSavings.quantize(TWOPLACES)))
		InfoMsg("Your budget savings are ${0}.".format(budgetSavings.quantize(TWOPLACES)))
		InfoMsg("The difference is ${0}.".format((actualSavings - budgetSavings).quantize(TWOPLACES)))

	def finalize(self):
		self._writeMoney()
		self._writeSavings()
		self.allocationManager.finalize()

	def _readMoney(self):
		'''
		Get current money out of CSV file
		'''
		with open(self._moneyPath, 'r') as mFile:
			mlines = mFile.readlines()
			for i in xrange(len(mlines)):
				if i == 0:
					continue
				category, money = mlines[i].strip().split(',')
				if category != DEBT_KEY:
					self.allocationManager.allocationMap[category].extraMoney = Decimal(money)
				else:
					self.allocationManager.allocationMap[category].debt = Decimal(money)
					self.allocationManager.allocationMap[category].debtReg = Decimal(money)

	def _readSavings(self):
		'''
		Get current savings out of CSV file
		'''
		with open(self._savingsPath, 'r') as sFile:
			slines = sFile.readlines()
			for i in xrange(len(slines)):
				if i == 0:
					continue
				category, product, percent, priority, savings, totalCost = slines[i].strip().split(',')
				self.allocationManager.addSubAllocation(cat=category, product=product, percent=percent, priority=priority, savings=savings, totalCost=totalCost)

	def _writeMoney(self):
		with open(self._moneyPath, 'w') as mFile:
			mFile.write("Category,Money\n")
			for cat in self.allocationManager.allocationMap:
				if cat != DEBT_KEY:
					mFile.write("{0},{1}\n".format(cat, self.allocationManager.allocationMap[cat].extraMoney.quantize(TWOPLACES)))
				else:
					mFile.write("{0},{1}\n".format(cat, self.allocationManager.allocationMap[cat].debt.quantize(TWOPLACES)))

	def _writeSavings(self):
		with open(self._savingsPath, 'w') as sFile:
			sFile.write("Category,Product,Percent,Priority,Savings,Total Cost\n")
			for cat in self.allocationManager.allocationMap:
				for subAlloc in self.allocationManager.allocationMap[cat].subAllocs:
					sFile.write(str(subAlloc))

