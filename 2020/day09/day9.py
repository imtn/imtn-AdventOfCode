# returns whether or not the value can be created by adding two values of the preamble
# preamble is a list of integer
# value is an integer
# Returns True if two values in preamble add to the value, or False if none of them do.
def hasSumFromPreamble(preamble, evalValue):
	for index, value1 in enumerate(preamble):
		for value2 in preamble[index+1:]:
			if value1 != value2 and value1 + value2 == evalValue:
				return True
	return False

# returns the contiguous range of numbers from numList that add up to value
# numList is a list of integers
# value is an integer
# Returns a list, specifically a sublist of numList, that holds the contiguous range of integers that add up to value
# Returns None if it doesn't find the range
def findContiguousRange(numList, value):
	for index1 in range(len(numList)+1):
		for index2 in range(index1+1,len(numList)+1):
			if sum(numList[index1:index2]) == value:
				return numList[index1:index2]
	return None

def part1():
	XMASList = []
	with open('input.txt') as f:
		for line in f:
			XMASList.append(int(line.strip()))

	startIndex = 0
	evalIndex = 25
	# we are evaluating if XMASList[evalIndex] has a preamble sum from XMASList[startIndex:evalIndex]
	while evalIndex < len(XMASList):
		if not hasSumFromPreamble(XMASList[startIndex:evalIndex], XMASList[evalIndex]):
			print("Found no sum: " + str(XMASList[evalIndex]))
			break
		startIndex += 1
		evalIndex += 1

def part2():
	XMASList = []
	with open('input.txt') as f:
		for line in f:
			XMASList.append(int(line.strip()))

	startIndex = 0
	evalIndex = 25
	noSumIndex = 0
	noSumValue = 0
	# we are evaluating if XMASList[evalIndex] has a preamble sum from XMASList[startIndex:evalIndex]
	while evalIndex < len(XMASList):
		if not hasSumFromPreamble(XMASList[startIndex:evalIndex], XMASList[evalIndex]):
			print("Found no sum: " + str(XMASList[evalIndex]))
			noSumIndex = evalIndex
			noSumValue = XMASList[evalIndex]
			break
		startIndex += 1
		evalIndex += 1

	print(noSumIndex)
	rangeList = findContiguousRange(XMASList[0:noSumIndex], noSumValue)
	print("Min is " + str(min(rangeList)))
	print("Max is " + str(max(rangeList)))
	print("Sum is " + str(min(rangeList) + max(rangeList)))

def main():
	part1()
	part2()
main()