import sys

'''
Expand to make a yes/no menu for simple yes or no questions
'''
class Menu:
	OPTION_INDEX = 0
	CALLBACK_INDEX = 1
	ARGS_INDEX = 2

	def __init__(self, quitCallback=None, *quitArgs):
		self.optionList = []
		self.quitCallback = quitCallback
		self.quitArgs = quitArgs

	def run(self):
		self.display()
		return self.choose()

	def display(self):
		print '=' * 10 + ' Menu ' + '=' * 10
		for i in xrange(len(self.optionList)):
			print '{0}) {1}'.format(i+1, self.optionList[i][Menu.OPTION_INDEX])

	def choose(self):
		done = False
		choice = None
		while not done:
			choice = raw_input('Select one of the options or enter "q" to quit: ')
			if choice == 'q':
				done = True
			else:
				try:
					choice = int(choice)
					if choice >= 1 and choice <= len(self.optionList):
						done = True
				except:
					pass
		args = None
		callback = None
		if choice == 'q':
			args = self.quitArgs
			callback = self.quitCallback
		elif choice >= 1 and choice <= len(self.optionList):
			args = self.optionList[choice - 1][Menu.ARGS_INDEX]
			callback = self.optionList[choice - 1][Menu.CALLBACK_INDEX]
		else:
			raise Exception("Invalid choice: {0}".format(choice))

		if args is not None and callback is not None:
			callback(*args)
			
		return choice

	def option(self, option):
		index = -1
		for i in xrange(len(self.optionList)):
			if self.optionList[i][0] == option:
				index = i
		return index

	def addOption(self, option, callback=None, *args):
		self.optionList.append([option, callback, args])

	def updateOption(self, option, callback=None, *args):
		index = self.option(option)
		if index >= 0:
			self.optionList[index] = [option, callback, args]
