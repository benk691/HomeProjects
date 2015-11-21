from decimal import Decimal
from AllocationManager import AllocationManager
from General.Common import TWOPLACES, setContext

class MoneyManager:
	def __init__(self, moneyPath, allocationPath, savingsPath):
		setContext()
		self._moneyPath = moneyPath
		self._savingsPath = savingsPath
		# Allocation manager
		self.allocationManager = AllocationManager(allocationPath)
		self._readMoney()
		self._readSavings()

	def deposit(self):
		'''
		Deposits money according to the percentages of all the allocations
		'''
		depositAmount = Decimal(raw_input("How much money to deposit? "))
		self.allocationManager.deposit(depositAmount)

	def withdraw(self):
		'''
		Withdraws money out of an allocation and checks if withdrawal is over budget
		'''
		self.allocationManager.withdraw()		

	def status(self):
		self.allocationManager.status()

	def update(self):
		self.allocationManager.update()

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
				self.allocationManager.allocationMap[category].extraMoney = Decimal(money)

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
				mFile.write("{0},{1}\n".format(cat, self.allocationManager.allocationMap[cat].extraMoney.quantize(TWOPLACES)))

	def _writeSavings(self):
		with open(self._savingsPath, 'w') as sFile:
			sFile.write("Category,Product,Percent,Priority,Savings,Total Cost\n")
			for cat in self.allocationManager.allocationMap:
				for subAlloc in self.allocationManager.allocationMap[cat].subAllocs:
					sFile.write(str(subAlloc))

