class Node:
  def __init__(self):
    self.label = None #title of party/ class ------- only have a label if it's a leaf node
    self.listOfChildren = []
    self.attribute = None
    self.listOfPeople = [] #list of all dictionaries remaining at that node
    self.mode = None
    self.orderedListOfAttributeStates = []
	# you may want to add additional fields here...