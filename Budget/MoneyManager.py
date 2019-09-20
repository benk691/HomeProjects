from decimal import Decimal
from AllocationManager import AllocationManager
from General.Common import WarningMsg, InfoMsg, DebugMsg, TWOPLACES, setContext, DEBT_KEY, EXTRA_KEY

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
		Adds the amount in each allocation and compares it with bank holdings and credit debt.
		The functions takes the difference and puts it into the extra money category if positive, 
		otherwise adds the amount to your existing debt.
		'''
		bankAccountMoney = Decimal("0.00")
		creditAccountMoney = Decimal("0.00")
		savings = Decimal("0.00")
		bankAccounts = int(raw_input("How many bank accounts do you have? "))
		creditCards = int(raw_input("How many credit cards do you have? "))

		for ba in xrange(bankAccounts):
			bankAccountMoney += Decimal(raw_input("How much money is in your bank account #{0}? ".format(ba)))

		for cc in xrange(creditCards):
			creditCap = Decimal(raw_input("What is your credit line for credit card account #{0}? ".format(cc)))
			availCredit = Decimal(raw_input("What is your available credit for credit card account #{0}? ".format(cc)))
			creditAccountMoney += (-1 * abs(creditCap - availCredit))

		if bankAccounts > 0 or creditCards > 0:
			# Calculate your debt before continuing
			self.allocationManager.calculateDebt()
			actualSavings = bankAccountMoney + creditAccountMoney
			budgetSavings = self.allocationManager.calculateSavings()
			# This works for all values of actualSavings and budgetSavings.
			# For more description why look in the wiki
			diff = actualSavings - budgetSavings

			InfoMsg("Your actual savings are ${0}.".format(actualSavings.quantize(TWOPLACES)))
			InfoMsg("Your budget savings are ${0}.".format(budgetSavings.quantize(TWOPLACES)))
			
			if diff >= Decimal("0.00"):
				InfoMsg("Adding ${0} to your extra money.".format(diff.quantize(TWOPLACES)))
				self.allocationManager.allocationMap[EXTRA_KEY].extraMoney += diff
			else:
				InfoMsg("Adding ${0} to your debt.".format(diff.quantize(TWOPLACES)))
				self.allocationManager.allocationMap[DEBT_KEY].debtReg += diff
				self.allocationManager.calculateDebt()
				WarningMsg("You have accumulated a debt of ${0}!".format(self.allocationManager.allocationMap[DEBT_KEY].debt.quantize(TWOPLACES)))

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
				if mlines[i].strip():
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
				if slines[i].strip():
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

