
'''
Creates an action or callback
The point of the class is so all parameters, including ints are now
referenced when a parameter is changed, it changes in this class
'''
class Action:
  def __init__(self, function, params=[], kwargs={}):
    '''
    Initializes the action
    @param function - the function to call
    @param params - list of non-named parameters
    @kwargs - ditionary of variable names to their values
    '''
    self.function = function
    self.params = params
    self.kwargs = kwargs

  def execute(self):
    '''
    Executes the action's function
    '''
    self.function(*self.params, **self.kwargs)
