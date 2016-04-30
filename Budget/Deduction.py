class Deduction:
	def __init__(self, deductionsPath):
		self._deductionsPath = deductionsPath

	def _readDeductions(self):
		'''
		Get deductions out of CSV file
		'''
		with open(self._deductionsPath, 'r') as sFile:
			dlines = sFile.readlines()
			for i in xrange(len(dlines)):
				if i == 0:
					continue
				dlines[i].strip().split(',')