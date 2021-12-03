# bpString is a string of one boarding pass, from the puzzle input
# Returns tuple (row, col)
def getRowCol(bpString):
	rows = 128
	cols = 8
	rowTuple = (0,rows-1)
	colTuple = (0,cols-1)

	minRow, maxRow = getIDRecursive(bpString[:7], rowTuple)
	minCol, maxCol = getIDRecursive(bpString[-3:], colTuple)

	if minRow != maxRow or minCol != maxCol:
		print("Failed to get row and col: " + str(minRow) + ' ' + str(maxRow) + ' ' + str(minCol) + ' ' + str(maxCol))
		quit()
	return (minRow, minCol)


# bStr is either a string composed of F and B, or composed of L and R
# minMaxTuple looks like (min, max)
# This returns a tuple (newMin, newMax)
# Assumes seats number starting from 0
def getIDRecursive(bStr, minMaxTuple):
	oldMin, oldMax = minMaxTuple
	newMin = oldMin
	newMax = oldMax
	bChar = bStr[0]
	halfNumOfSeats = int((oldMax - oldMin + 1) / 2)
	if bChar == 'F': # lower half
		newMax = oldMax - halfNumOfSeats
	elif bChar == 'L': # lower half
		newMax = oldMax - halfNumOfSeats
	elif bChar == 'B': # upper half
		newMin = oldMin + halfNumOfSeats
	elif bChar == 'R': # upper half
		newMin = oldMin + halfNumOfSeats
	else:
		print("Exception in recursive function: " + bStr + " " + minMaxTuple)
		quit()
	if len(bStr) == 1:
		return (newMin, newMax)
	else:
		return getIDRecursive(bStr[1:], (newMin, newMax))

def part1():
	highestSeatID = -1
	with open('input.txt') as f:
		for line in f:
			row, col = getRowCol(line.strip())
			thisSeatID = row * 8 + col
			# print((row,col))
			# print(thisSeatID)
			highestSeatID = thisSeatID if thisSeatID > highestSeatID else highestSeatID
	print(highestSeatID)

def part2():
	# Find a seatID where seatID != min and seatID != max and seatID+1 and seatID-1 are defined, but not seatID
	minID = 1000
	maxID = 0
	seatID = -1
	seatSet = set() # set of seatIDs

	with open('input.txt') as f:
		for line in f:
			row, col = getRowCol(line.strip())
			thisSeatID = row * 8 + col
			minID = thisSeatID if thisSeatID < minID else minID
			maxID = thisSeatID if thisSeatID > maxID else maxID
			seatSet.add(thisSeatID)

	print(len(seatSet))
	for x in range(minID+1, maxID): # for every ID that isn't the min or max ID
		if x not in seatSet and x-1 in seatSet and x+1 in seatSet:
			print(x)

def main():
	part1()
	part2()
main()