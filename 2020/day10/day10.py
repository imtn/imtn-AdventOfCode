# counts the number of valid arrangements 
# adapters is a list of integers, each representing the joltage of that adapter
# returns an integer representing the number of adapter arrangements there are
def getAdapterArrangementCount(adapters):
	pathCounts = dict() # pathCounts is a dict mapping each adapter to how many paths reach it
	adapters.sort()
	adapterStep = 3

	for a in adapters:
		pathCounts[a] = 0

	# Setting the initial condition
	pathCounts[0] = 1

	# Algo: for each adapter, increment the pathCount for every adapter it can reach
	for i in range(len(adapters) - 1):
		ada = adapters[i]
		for ada2 in range(ada+1, ada+4):
			# print("For ada " + str(ada) + " checking ada2 " + str(ada2))
			if ada2 in pathCounts:
				pathCounts[ada2] += pathCounts[ada]
				# print("Updated ada2 to " + str(pathCounts[ada2]))

	return pathCounts[adapters[-1]]

def part1():
	adapters = []
	with open('input.txt') as f:
		for line in f:
			adapters.append(int(line.strip()))

	adapters.append(0)
	adapters.append(max(adapters) + 3)
	adapters.sort()

	oneJoltDiff = 0
	threeJoltDiff = 0


	for i in range(len(adapters) - 1):
		if adapters[i+1] - adapters[i] == 1:
			oneJoltDiff += 1
		if adapters[i+1] - adapters[i] == 3:
			threeJoltDiff += 1

	# print(oneJoltDiff)
	# print(threeJoltDiff)
	print(oneJoltDiff*threeJoltDiff)

def part2():
	adapters = []
	with open('input.txt') as f:
		for line in f:
			adapters.append(int(line.strip()))

	adapters.append(0)
	adapters.append(max(adapters) + 3)
	adapters.sort()

	print(getAdapterArrangementCount(adapters))

def main():
	part1()
	part2()
main()