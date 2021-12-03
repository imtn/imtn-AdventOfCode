# produces a new dictionary where every number in a range in the input dictionary is a key in the dict
# fieldDict is a dictionary mapping fields to its number ranges
# returns a set of ints in any range in the fieldDict
def getFullRange(fieldDict):
	newSet = set()
	for field in fieldDict: # for each key
		for ranges in fieldDict[field]: # for each value (list of ranges)
			for val in ranges:
				newSet.add(val)
	return newSet

# determines if each value in values matches a range in field
# field is a list, len 2, of ranges
# values is a list of int values
# Returns True if every value in values is contained within a range in field, otherwise returns False
def fieldMatchesValues(field, values):
	for val in values:
		if val not in field[0] and val not in field[1]:
			return False
	return True

def part1():
	# State is what we're currently parsing from input
	# 0 while scanning field definitions
	# 1 while scanning my ticket
	# 2 while scanning nearby tickets
	scanningState = 0

	# fieldDict is a dictionary mapping the field to what number ranges it incorporates
	# key is a string representing the field
	# value is a list of ranges representing the valid numbers
	fieldDict = dict()

	# List of int fields in my ticket
	myTicket = []

	# List of lists
	# Outer list holds each ticket
	# Inner list represents one ticket, and each element is an int representing a field
	nearbyTickets = []

	errorRate = 0
	with open('input.txt') as f:
		for line in f:
			if scanningState == 0:
				if line == '\n':
					scanningState = 1
					continue

				field = line.split(':')[0]
				ranges = line.split(':')[1].strip().split(' or ')
				fieldDict[field] = []
				for r in ranges:
					rangeNums = r.split('-')
					fieldDict[field].append(range(int(rangeNums[0]), int(rangeNums[1]) + 1))
			elif scanningState == 1:
				if line == '\n':
					scanningState = 2
					continue

				if line[0] != 'y':
					myTicket = [int(x) for x in line.strip().split(',')]

			elif scanningState == 2:
				if line[0] != 'n':
					nearbyTickets.append([int(x) for x in line.strip().split(',')])

			else:
				print("Bad scanning state: " + str(scanningState))
				quit()

	fullRangeSet = getFullRange(fieldDict)
	for ticket in nearbyTickets:
		for num in ticket:
			if num not in fullRangeSet:
				errorRate += num
	print(errorRate)

def part2():
	# State is what we're currently parsing from input
	# 0 while scanning field definitions
	# 1 while scanning my ticket
	# 2 while scanning nearby tickets
	scanningState = 0

	# fieldDict is a dictionary mapping the field to what number ranges it incorporates
	# key is a string representing the field
	# value is a list of ranges representing the valid numbers
	fieldDict = dict()

	# List of int fields in my ticket
	myTicket = []

	# List of lists
	# Outer list holds each ticket
	# Inner list represents one ticket, and each element is an int representing a field
	nearbyTickets = []

	with open('input.txt') as f:
		for line in f:
			if scanningState == 0:
				if line == '\n':
					scanningState = 1
					continue

				field = line.split(':')[0]
				ranges = line.split(':')[1].strip().split(' or ')
				fieldDict[field] = []
				for r in ranges:
					rangeNums = r.split('-')
					fieldDict[field].append(range(int(rangeNums[0]), int(rangeNums[1]) + 1))
			elif scanningState == 1:
				if line == '\n':
					scanningState = 2
					continue

				if line[0] != 'y':
					myTicket = [int(x) for x in line.strip().split(',')]

			elif scanningState == 2:
				if line[0] != 'n':
					nearbyTickets.append([int(x) for x in line.strip().split(',')])

			else:
				print("Bad scanning state: " + str(scanningState))
				quit()

	fullRangeSet = getFullRange(fieldDict)
	badTickets = []
	for ticket in nearbyTickets:
		for num in ticket:
			if num not in fullRangeSet:
				badTickets.append(ticket)
				continue
	
	goodTickets = [ticket for ticket in nearbyTickets if ticket not in badTickets]

	# List of lists
	# outer list holds a list, each of which represents one ticket field
	# inner list holds a set of all values from all tickets for that field
	valuesList = [set() for _ in range(len(goodTickets[0]))]

	# For each ticket field, get all values from every nearby ticket for that field
	for goodTicket in goodTickets:
		for i, v in enumerate(goodTicket):
			valuesList[i].add(v)
	

	fieldColDict = dict()
	# for every ticket field, find the column that matches its ranges
	# save matching columns to fieldColDict
	for field in fieldDict:
		fieldColDict[field] = set()
		for i, v in enumerate(valuesList):
			if fieldMatchesValues(fieldDict[field], v):
				# print(field + ' matches column ' + str(i+1))
				fieldColDict[field].add(i)


	for field in sorted(list(fieldColDict.keys()), key=lambda f: len(fieldColDict[f])):
		for otherField in fieldColDict:
			if field != otherField:
				fieldColDict[otherField].discard(list(fieldColDict[field])[0])

	for field in fieldColDict:
		fieldColDict[field] = list(fieldColDict[field])[0]
	
	answer = 1
	for field in fieldColDict:
		if field.split(' ')[0] == 'departure':
			answer *= myTicket[fieldColDict[field]]
	print(answer)

def main():
	part1()
	part2()
main()