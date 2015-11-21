import copy
from decimal import Decimal
from General.Menu import Menu
from General.Color import Color

class MoneySandbox:
	def __init__(self, moneyManager):
		# Keep around a copy of the real reference if we decide to commit the changes
		self.realMoneyManager = copy.deepcopy(moneyManager)
		# Keep a backup that will never be erased until we are done with the sandbox
		self.backupMoneyManager = copy.deepcopy(moneyManager)
		# Copy the money manager
		self.sbMoneyManager = copy.deepcopy(moneyManager)
		self.sbMenu = Menu()
		self._createSBMenu()
		self.run()

	def run(self):
		'''
		Run sandbox
		'''
		while self.sbMenu.run() != 'q': pass

	def commitChanges(self):
		'''
		Commits the changes made in the sandbox to the money and allocations
		'''
		choice = 'q'
		while choice.lower != 'y' and choice.lower() != 'n':
			choice = raw_input("Are you sure you want to commit these changes? (y/n): ")
		if choice == 'y':
			# Commit changes to the real money manager
			self.realMoneyManager = copy.deepcopy(self.sbMoneyManager)

	def discardChanges(self):
		'''
		Discard all changes and start over
		'''
		# copy back the original
		self.sbMoneyManager = copy.deepcopy(self.realMoneyManager)

	def undoCommit(self):
		'''
		Undoes a commit action and starts over
		'''
		self.realMoneyManager = copy.deepcopy(self.backupMoneyManager)
		self.sbMoneyManager = copy.deepcopy(self.backupMoneyManager)

	def _createSBMenu(self):
		'''
		Create a sandbox menu
		'''
		self.sbMenu.addOption('Deposit', self.sbMoneyManager.deposit)
		self.sbMenu.addOption('Withdraw', self.sbMoneyManager.withdraw)
		self.sbMenu.addOption('Status', self.sbMoneyManager.status)
		self.sbMenu.addOption('Update', self.sbMoneyManager.update)
		self.sbMenu.addOption('Commit Changes', self.commitChanges)
		self.sbMenu.addOption('Discard Changes', self.discardChanges)
		self.sbMenu.addOption('Undo Last Commit', self.undoCommit)
