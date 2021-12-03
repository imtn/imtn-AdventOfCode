# Adds the val to the turn in the turns dictionary
# turns is a dictionary mapping a val to a list of turns
# turn is an int representing the turn
# val is the value to add to the list
def addToTurns(turns, turn, val):
	if val not in turns:
		turns[val] = []
	turns[val].append(turn)

def part1():
	inputStr = '12,20,0,6,1,17,7'
	# inputStr = '0,3,6' # This is the test string
	startingNumbers = [int(x) for x in inputStr.strip().split(',')]

	turns = dict()
	prevNum = -1
	turn = 0
	for num in startingNumbers:
		addToTurns(turns, turn, num)
		prevNum = num
		turn += 1
		# print(str(turn) + ' ' + str(prevNum))
	while turn < 2020:
		if len(turns[prevNum]) == 1:
			prevNum = 0
		else:
			prevNum = turns[prevNum][-1] - turns[prevNum][-2]
		addToTurns(turns, turn, prevNum)
		turn += 1
		# print(str(turn) + ' ' + str(prevNum))
	print(prevNum)

def part2():
	inputStr = '12,20,0,6,1,17,7'
	# inputStr = '0,3,6' # This is the test string
	startingNumbers = [int(x) for x in inputStr.strip().split(',')]

	turns = dict()
	prevNum = -1
	turn = 0
	for num in startingNumbers:
		addToTurns(turns, turn, num)
		prevNum = num
		turn += 1
		# print(str(turn) + ' ' + str(prevNum))
	while turn < 30000000:
		if len(turns[prevNum]) == 1:
			prevNum = 0
		else:
			prevNum = turns[prevNum][-1] - turns[prevNum][-2]
		addToTurns(turns, turn, prevNum)
		turn += 1
		# print(str(turn) + ' ' + str(prevNum))
	print(prevNum)

def main():
	part1()
	part2()
main()