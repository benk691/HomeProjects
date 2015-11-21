import decimal
from Color import Color
from decimal import Decimal, Context

TWOPLACES = Decimal('0.01')
EXTRA_KEY = 'Extra'
DEBT_KEY = 'Debt'

def InfoMsg(msg):
	print "{0}{1}INFO:{2} {3}{4}{5}".format(Color.BLINKING, Color.CYAN, Color.END, Color.CYAN, msg, Color.END)

def WarningMsg(msg):
	print "{0}{1}WARNING:{2} {3}{4}{5}".format(Color.BLINKING, Color.YELLOW, Color.END, Color.YELLOW, msg, Color.END)

def ErrorMsg(msg):
	print "{0}{1}ERROR:{2} {3}{4}{5}".format(Color.BLINKING, Color.RED, Color.END, Color.RED, msg, Color.END)
	raise Exception(msg)

def setContext():
	budgetContext = Context(rounding=decimal.ROUND_DOWN)
	decimal.setcontext(budgetContext)
