import decimal
from decimal import Decimal, Context
from General.Menu import Menu
from MoneyManager import MoneyManager
from MoneySandbox import MoneySandbox

allocationPath = "./TextFiles/allocations.csv"
moneyPath = "./TextFiles/money.csv"
savingsPath = "./TextFiles/savings.csv"
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


def createMenu(moneyManager):
	menu = Menu()
	menu.addOption('Deposit', moneyManager.deposit)
	menu.addOption('Withdraw', moneyManager.withdraw)
	menu.addOption('Status', moneyManager.status)
	menu.addOption('Update', moneyManager.update)
	menu.addOption('Create a sandbox', MoneySandbox, moneyManager)
	return menu

def run():
	moneyManager = MoneyManager(moneyPath, allocationPath, savingsPath)
	menu = createMenu(moneyManager)
	while menu.run() != 'q':
		menu.updateOption('Create a sandbox', MoneySandbox, moneyManager)
	moneyManager.finalize()

def main():
	decimal.setcontext(budgetContext)
	run()
	return 0

if __name__ == '__main__':
	main()