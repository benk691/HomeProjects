import decimal
from decimal import Decimal, Context
from Menu import Menu
from MoneyManager import MoneyManager
from MoneySandbox import MoneySandbox

allocationPath = "./Text Files/allocations.csv"
moneyPath = "./Text Files/money.csv"
savingsPath = "./Text Files/savings.csv"
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

'''
IDEAS:
- When you reach the totalCost of a product the status will inform you. 
- Make test area/sandbox to play around with money and potential incomes or do whatever without 
  any changes but have the option to commit all the changes once you are done, if you want to
- Add in option to change allocation percentages & priorities
- Track transactions for the past month or something so that there can be comparisons
- Instead of using CSV write to a SQL database (ie: Heroku)
- Make a debt category where if you go over in any category then it goes to debt. Then when you deposit, 
  the debt is first subtracted off of the income and then deposited amongst the allocations. Make choices
  either have the debt made up with your next income or have it sit in negative in that allocation until
  it gets made up (in which case at least 75% of the allocated income goes to making up the debt until it is fully)
  made up for
'''

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