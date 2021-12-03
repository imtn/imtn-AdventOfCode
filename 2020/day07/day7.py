# This method finds out if the startBagColor bag can eventually hold the goalBagColor
# bagDict is a dictionary mapping a bag color to what bags it can contain
# startBagColor is a string representing the color of the starting bag
# goalBagColor is a string representing the color of the goal bag
# This returns the True boolean if the startBagColor bag can eventually hold the goalBagColor, and False otherwise.
def findBagRecursive(bagDict, startBagColor, goalBagColor):
	# first check if startBagColor cannot hold anything
	# then check if startBagColor can directly hold the goal
	# then recursively check if any bag that startBagColor contains, can eventually contain the goalBagColor
	# if none of the above, return False

	if bagDict[startBagColor] == []:
		return False

	for childBagTuple in bagDict[startBagColor]:
		childBagNumber, childBagColor = childBagTuple
		if childBagColor == goalBagColor:
			return True

	for childBagTuple in bagDict[startBagColor]:
		childBagNumber, childBagColor = childBagTuple
		if findBagRecursive(bagDict, childBagColor, goalBagColor):
			return True

	return False 

# This method returns the max number of bags the startBagColor bag can contain
# bagDict is a dictionary mapping a bag color to what bags it can contain
# startBagColor is a string representing the color of the starting bag
# This returns an integer representing the number of bags the startBagColor can contain, excluding the startBagColor bag itself
def countBagsInsideRecursive(bagDict, startBagColor):
	# if startBagColor cannot contain bags, return 0
	# if it can contain bags, loop over each bag recursively to count how many bags each one can hold

	count = 0
	for (childBagNumber, childBagColor) in bagDict[startBagColor]:
			count += childBagNumber
			count += childBagNumber * countBagsInsideRecursive(bagDict, childBagColor)
	return count

def part1():
	noBagString = 'no other'
	bagSet = set() # set of all bag colors
	bagRuleDict = dict() # store bag rules as a dictionary. key is outer bag color, value is list of tuples, tuple looks like (bagNumber, bagColor)

	with open('input.txt') as f:
		for line in f:
			outerBagString = line.split('contain')[0].strip()
			innerBagString = line.split('contain')[1].strip()
			outerBagColor = outerBagString.split('bags')[0].strip()
			innerBagList = innerBagString.split(',')
			# Assumes color names are only two words long
			innerBagList = []
			for innerBag in innerBagString.split(','):
				innerBagSplit = innerBag.strip().split(' ')
				if innerBagSplit[0] + ' ' + innerBagSplit[1] == noBagString:
					break
				else:
					bagNumber = int(innerBagSplit[0])
					bagColor = innerBagSplit[1] +  ' ' + innerBagSplit[2]
					innerBagList.append((bagNumber, bagColor))

			bagSet.add(outerBagColor)
			# assuming that no outer bag color is repeated, we create new dict entry from the outer bag color to a list (of tuples which we populate later)
			bagRuleDict[outerBagColor] = innerBagList
	
	numberOfShinyGoldBags = 0
	for bagColor in bagSet:
		if findBagRecursive(bagRuleDict, bagColor, 'shiny gold'):
			numberOfShinyGoldBags += 1
	print(numberOfShinyGoldBags)

def part2():
	noBagString = 'no other'
	bagSet = set() # set of all bag colors
	bagRuleDict = dict() # store bag rules as a dictionary. key is outer bag color, value is list of tuples, tuple looks like (bagNumber, bagColor)

	with open('input.txt') as f:
		for line in f:
			outerBagString = line.split('contain')[0].strip()
			innerBagString = line.split('contain')[1].strip()
			outerBagColor = outerBagString.split('bags')[0].strip()
			innerBagList = innerBagString.split(',')
			# Assumes color names are only two words long
			innerBagList = []
			for innerBag in innerBagString.split(','):
				innerBagSplit = innerBag.strip().split(' ')
				if innerBagSplit[0] + ' ' + innerBagSplit[1] == noBagString:
					break
				else:
					bagNumber = int(innerBagSplit[0])
					bagColor = innerBagSplit[1] +  ' ' + innerBagSplit[2]
					innerBagList.append((bagNumber, bagColor))

			bagSet.add(outerBagColor)
			# assuming that no outer bag color is repeated, we create new dict entry from the outer bag color to a list (of tuples which we populate later)
			bagRuleDict[outerBagColor] = innerBagList

	print(countBagsInsideRecursive(bagRuleDict, 'shiny gold'))

def main():
	part1()
	part2()
main()