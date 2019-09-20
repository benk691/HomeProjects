import decimal
import time
from decimal import Decimal, Context
from General.Menu import Menu
from MoneyManager import MoneyManager
from MoneySandbox import MoneySandbox

allocationPath = "./TextFiles/allocations.csv"
moneyPath = "./TextFiles/money.csv"
savingsPath = "./TextFiles/savings.csv"
lastLoggedPath = "./TextFiles/savingsLastLogged.txt"
catKey = 'Category'
percentKey = 'Percent'
priorityKey = 'Priority'
moneyKey = 'Money'
extraKey = 'Extra'
productKey = 'Product'
savingsKey = 'Savings'
totalCostKey = 'Total Cost'
budgetContext = Context(rounding=decimal.ROUND_DOWN)
TWOPLACES = Decimal('0.01')

def main():
	decimal.setcontext(budgetContext)
	run()
	return 0

def run():
	moneyManager = MoneyManager(moneyPath, allocationPath, savingsPath)
	menu = createMenu(moneyManager)
	while menu.run() != 'q':
		menu.updateOption('Create a sandbox', MoneySandbox, moneyManager)
	moneyManager.finalize()
	logTime()

def createMenu(moneyManager):
	menu = Menu()
	menu.addOption('Deposit', moneyManager.deposit)
	menu.addOption('Withdraw', moneyManager.withdraw)
	menu.addOption('Status', moneyManager.status)
	menu.addOption('Update', moneyManager.update)
	menu.addOption('Calculate Savings', moneyManager.calculateSavings)
	menu.addOption('Create a sandbox', MoneySandbox, moneyManager)
	return menu

def logTime():
	with open(lastLoggedPath, 'w') as logFile:
		logFile.write(time.strftime("%m/%d/%Y %H:%M:%S"))

if __name__ == '__main__':
	main()