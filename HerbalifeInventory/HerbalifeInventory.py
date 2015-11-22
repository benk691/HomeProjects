import decimal
from decimal import Decimal, Context
from General.Menu import Menu
from General.Color import Color

inventoryPath = "./TextFiles/HerbalifeInventory.csv"
productKey='Product'
quantityKey='Quantity'
quantityPerMealKey='Quantity/Meal'
mealPerDayKey='Meal/Day'
daysLeftkey='Days Left'
invContext = Context(rounding=decimal.ROUND_DOWN)
TWOPLACES = Decimal('0.01')

def readInventory():
	inventoryTable = dict()
	with open(inventoryPath, 'r') as iFile:
		iLines = iFile.readlines()
		for i in xrange(len(iLines)):
			if i == 0:
				continue
			product, quantity, qPerM, mPerD, days = iLines[i].strip().split(',')
			subTable = dict()
			subTable.update({productKey : product})
			subTable.update({quantityKey : Decimal(quantity)})
			subTable.update({quantityPerMealKey : Decimal(qPerM)})
			subTable.update({mealPerDayKey : Decimal(mPerD)})
			subTable.update({daysLeftkey : Decimal(days)})
			inventoryTable.update({product : subTable})
	return inventoryTable

def decStr(value):
	return value.quantize(TWOPLACES)

def writeInventory(inventoryTable):
	with open(inventoryPath, 'w') as iFile:
		iFile.write("Product,Quantity,Quantity/Meal,Meal/Day,Days Left\n")
		for product in inventoryTable:
			quantity = inventoryTable[product][quantityKey]
			qPerM = inventoryTable[product][quantityPerMealKey]
			mPerD = inventoryTable[product][mealPerDayKey]
			days = inventoryTable[product][daysLeftkey]
			iFile.write("{0},{1},{2},{3},{4}\n".format(product, decStr(quantity), decStr(qPerM), decStr(mPerD), decStr(days)))

def calculateDaysLeft(inventoryTable):
	for product in inventoryTable:
		quantity = inventoryTable[product][quantityKey]
		qPerM = inventoryTable[product][quantityPerMealKey]
		mPerD = inventoryTable[product][mealPerDayKey]
		if quantity == 0 or qPerM == 0 or mPerD == 0:
			# This will result in 0 or divide by 0 error so default it to 0
			inventoryTable[product][daysLeftkey] = Decimal("0.00")
			continue
		inventoryTable[product][daysLeftkey] = quantity / (qPerM * mPerD)

def dailyUsage(inventoryTable):
	'''
	Takes off one day of use for every product
	'''
	for product in inventoryTable:
		quantity = inventoryTable[product][quantityKey]
		qPerM = inventoryTable[product][quantityPerMealKey]
		mPerD = inventoryTable[product][mealPerDayKey]
		if quantity > Decimal("0.00"):
			inventoryTable[product][quantityKey] = quantity - (qPerM * mPerD)
			if inventoryTable[product][quantityKey] < Decimal("0.00"):
				inventoryTable[product][quantityKey] = Decimal("0.00")

def status(inventoryTable):
	calculateDaysLeft(inventoryTable)
	print "{0} Status {1}".format('=' * 10, '=' * 10)
	for product in inventoryTable:
		info = ""
		if inventoryTable[product][daysLeftkey] == Decimal("0.00"):
			info = "{0}{1}(EMPTY!){2}".format(Color.BLINKING, Color.RED, Color.END)
		elif inventoryTable[product][daysLeftkey] <= Decimal("10.00"):
			info = "{0}{1}(LOW!){2}".format(Color.BLINKING, Color.YELLOW, Color.END)
		print "{0}: Days Left = {1} {2}".format(product, inventoryTable[product][daysLeftkey].quantize(TWOPLACES), info)

def createMenu(inventoryTable):
	menu = Menu(writeInventory, inventoryTable)
	menu.addOption("Status", status, inventoryTable)
	menu.addOption("Daily Deduction", dailyUsage, inventoryTable)
	return menu

def run(inventoryTable):
	menu = createMenu(inventoryTable)
	while menu.run() != 'q' : pass

def main():
	decimal.setcontext(invContext)
	inventoryTable = readInventory()
	run(inventoryTable)
	return 0

if __name__ == "__main__":
	main()