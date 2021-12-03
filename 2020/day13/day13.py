def part1():
	lines = open('input.txt').read().strip().split('\n')
	earliestTimestamp = int(lines[0])
	busIDs = [int(x) for x in lines[1].split(',') if x != 'x']
	earliestBus = -1 # By default set to -1. When we find this, it will be set to a positive number.
	earliestBusTimestamp = -1 # Same as above

	# Starting with the earliest timestamp, check every following minute.
	# For each following minute, if there is a bus who, moduled by timestamp equals 0, return that timestamp
	for timestamp in range(earliestTimestamp, earliestTimestamp + 9999):
		for bus in busIDs:
			if timestamp % bus == 0:
				earliestBus = bus
				earliestBusTimestamp = timestamp
				break
		if earliestBus != -1:
			break

	print("Found part 1: " + str(earliestBus * (earliestBusTimestamp - earliestTimestamp)))

def part2():
	lines = open('input.txt').read().strip().split('\n')
	# earliestTimestamp = int(lines[0])
	busIDs = [int(x) if x != 'x' else x for x in lines[1].split(',')]
	idModList = [] # list of [index, busIDs] or in math terms, [remainder, modulus number]
	for i, v in enumerate(busIDs):
		if v != 'x':
			idModList.append([i, v])
	idModList.sort(reverse=True, key=lambda l: l[1]) # sort in reverse using the modulus
	
	# Couldn't the problem have been something else besides 'you better know the chinese remainder theorem'?
	# Anyways, the basic gist of the algo is to loop over numbers that satisfy the first modulus, and find the first one that satisfies the second modulus
	# Then, using those, loop and find the first number that satisfies the third modulus, and so on.
	currNum = idModList[0][1] - idModList[0][0]
	incrementor = idModList[0][1]
	for bus in idModList[1:]:
		while True:
			if currNum % bus[1] == (bus[1] - bus[0]) % bus[1]:
				incrementor *= bus[1]
				break
			else:
				currNum += incrementor
	print("Part 2:")
	print(currNum)

def main():
	part1()
	part2()
main()