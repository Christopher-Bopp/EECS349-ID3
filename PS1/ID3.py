from node import Node
import math
import parse
import random
"""
1. can we hardcode 'y' and 'n' as the stored values for keys in the dictionaries.   (ANSWER) keep those as variables AND there can be more than 2
2. does randomizing work? (ANSWER) don't want that when calculating our entropy (if we're pruning at that point or if we don't have a good split)
3. 

important note: the default class is just a class to default to if we have no idea what else to do
"""
'''
things to work on
1. update choose attribute to not rely on previous attributes list
'''


def ID3(examples, default):
  tree = Node()
  tree.listOfPeople = examples
  tree.mode = MODE(tree.listOfPeople)
  listAttributeStates = []
  listClasses = []

  if  len(examples)==0:
    tree.label = default
    #print('empty node')
    return tree
  else:
    for item in examples:
      if item['Class'] in listClasses:
        continue
      else:
        listClasses.append(item['Class'])

    listAttributes = list(examples[0].keys())
    listAttributes.remove('Class')

    for item in examples:
      for attribute in listAttributes:
        if item[attribute] in listAttributeStates:
          continue
        else:
          listAttributeStates.append(item[attribute])

    if entropy(examples,listClasses) == 0 :
      tree.label = MODE(examples)
      tree.listOfPeople = examples
      #print('entropy of 0')
      return tree

    else:   
      bestAttributeName = chooseAttribute(examples,listAttributeStates, listAttributes, listClasses)
      #print(bestAttributeName)
      if bestAttributeName == None:
        tree.label = MODE(examples)
        return tree

      tree.attribute = bestAttributeName
      for attributeState in listAttributeStates:
        if attributeState == '?':
          continue
        else:
          tree.orderedListOfAttributeStates.append(attributeState)
          testList = []
          for example in examples:
            testList.append(example)

          tree.listOfChildren.append(ID3(createBranchList(attributeState, bestAttributeName, testList),default))

  return tree



def createBranchList (attributeState, attributeName, examples):
  #print('the  ' + attributeState + '  branch of:  ' + attributeName)
  newListOfPeople = []
  for example in examples:
    newListOfPeople.append(example.copy())
  listOfPeople = []
  for person in newListOfPeople:
    if person[attributeName] == attributeState:
      listOfPeople.append(person)
    elif person[attributeName] == '?':
      listOfPeople.append(person)
  for person in listOfPeople:
    person.pop(attributeName)

  return listOfPeople




def entropy(LOP,listClasses): #H(S) = -p(+) log2 p(x) - p(-) log2 p(-)
  e = 0
  total = len(LOP)

  if total != 0:
    for Class in listClasses:
      numClass = 0
      for person in LOP:
        if person['Class'] == Class:
          numClass+=1
      e += (-1 * float(numClass/total) * logHelper(float(numClass/total)))

  return e



def logHelper(num):
  if num == 0:
    return 0
  else:
    return math.log2(num)


def informationGain(LOP, listAttributeStates, attributeName, listClasses):
  H_prior = entropy(LOP, listClasses)
  numQuestionMarks = 0
  for person in LOP:
    if person[attributeName] =='?':
      numQuestionMarks +=1
    else:
      continue

  relevantLength = len(LOP) - numQuestionMarks

  if relevantLength == 0:
    return 0
    
  for attributeState in listAttributeStates:
    listObejctsWithState = []
    for person in LOP:
      if person[attributeName] == attributeState:
        listObejctsWithState.append(person)

    H_prior -= ((len(listObejctsWithState)/relevantLength) * entropy(listObejctsWithState, listClasses))

  return H_prior



def chooseAttribute(examples,listAttributeStates, listAttributes, listClasses): #returns the best attribute to split on next 
  bestGain = 0
  bestAttributeName = None

  for attribute in listAttributes:
    gain = informationGain(examples,listAttributeStates, attribute, listClasses)
    if gain > bestGain:
      bestGain = gain
      bestAttributeName = attribute
  return bestAttributeName


def MODE(examples): #returns most frequent class label in examples
  count = []
  for e in examples:
    count.append(e['Class'])
  return max(set(count), key=count.count)





def percentClass(examples, currentClass):
  total = len(examples)
  totalCorrect = 0
  for example in examples:
    if example['Class'] == currentClass:
      totalCorrect+=1

  return float(totalCorrect/total)



def prune(node, examples):
  modeOfNode = node.mode
  accuracyIfPrune = percentClass(examples, modeOfNode)


  wrongIter = 0

  for example in examples:
    exampleCopy = example.copy()
    correctResult = exampleCopy.pop('Class')
    ans = evaluate(node, exampleCopy)
    if ans != correctResult:
      wrongIter +=1

  accuracyIfNotPrune = float((len(examples)-wrongIter) / len(examples))


  if accuracyIfPrune > accuracyIfNotPrune:
    node.label = modeOfNode
    node.listOfChildren = []
    #print(len(node.listOfPeople))
    #print('eliminated a node')
  else:
    for child in node.listOfChildren:
      prune(child, examples)

  return node

  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  classCorrect = 0
  accuracy = 0

  for example in examples:
    evaluateFunc = evaluate(node, example)
    if evaluateFunc == example['Class']:
        classCorrect += 1

  if len(examples) == 0:
    return 0
  accuracy = float(classCorrect)/float(len(examples))
  return accuracy


def evaluate(node, example):
  while node.label == None:
    exampleResult = example[node.attribute]
    attributeStateIndex = 0

    if exampleResult != '?':
      iterator = 0
      for i in node.orderedListOfAttributeStates:
        if i == exampleResult:
          attributeStateIndex = iterator
        else:
          iterator +=1
    else:
      attributeStateIndex= random.randint(0, (len(node.orderedListOfAttributeStates)-1))

    node=node.listOfChildren[attributeStateIndex]

  return node.label  






