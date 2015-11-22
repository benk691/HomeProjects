import decimal
from decimal import Decimal, Context

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

def main():
	decimal.setcontext(invContext)
	inventoryTable = readInventory()
	print inventoryTable
	return 0

if __name__ == "__main__":
	main()