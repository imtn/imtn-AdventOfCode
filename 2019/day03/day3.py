import sys

def getManhattanDistance(point):
	(x, y) = point
	return abs(x) + abs(y)

def getSet(arr):
	retset = set()
	startPoint = (0, 0)
	for vector in arr:
		mag = int(vector[1:])
		if vector.startswith('U'):
			for num in range(1, mag + 1):
				retset.add((startPoint[0], startPoint[1] + num))
			startPoint = (startPoint[0], startPoint[1] + mag)
		elif vector.startswith('D'):
			for num in range(1, mag + 1):
				retset.add((startPoint[0], startPoint[1] - num))
			startPoint = (startPoint[0], startPoint[1] - mag)
		elif vector.startswith('L'):
			for num in range(1, mag + 1):
				retset.add((startPoint[0] - num, startPoint[1]))
			startPoint = (startPoint[0] - mag, startPoint[1])
		elif vector.startswith('R'):
			for num in range(1, mag + 1):
				retset.add((startPoint[0] + num, startPoint[1]))
			startPoint = (startPoint[0] + mag, startPoint[1])
		else:
			print("Found a weird word.")
			print(vector)
			sys.exit()
	return retset

def getSetWithSteps(arr):
	# Like getSet(arr), but the tuple also includes steps for each intersection

	retset = set()
	startPoint = (0, 0, 0) # (x, y, steps)
	for vector in arr:
		mag = int(vector[1:])
		if vector.startswith('U'):
			for num in range(1, mag + 1):
				retset.add((startPoint[0], startPoint[1] + num, startPoint[2] + num))
			startPoint = (startPoint[0], startPoint[1] + mag, startPoint[2] + mag)
		elif vector.startswith('D'):
			for num in range(1, mag + 1):
				retset.add((startPoint[0], startPoint[1] - num, startPoint[2] + num))
			startPoint = (startPoint[0], startPoint[1] - mag, startPoint[2] + mag)
		elif vector.startswith('L'):
			for num in range(1, mag + 1):
				retset.add((startPoint[0] - num, startPoint[1], startPoint[2] + num))
			startPoint = (startPoint[0] - mag, startPoint[1], startPoint[2] + mag)
		elif vector.startswith('R'):
			for num in range(1, mag + 1):
				retset.add((startPoint[0] + num, startPoint[1], startPoint[2] + num))
			startPoint = (startPoint[0] + mag, startPoint[1], startPoint[2] + mag)
		else:
			print("Found a weird word.")
			print(vector)
			sys.exit()
	return retset

def getDictWithSteps(arr):
	# Key is tuple of point, value is steps of the first time we come here

	retdict = dict()
	startPoint = (0, 0, 0)
	for vector in arr:
		mag = int(vector[1:])
		if vector.startswith('U'):
			for num in range(1, mag + 1):
				if ((startPoint[0], startPoint[1] + num) not in retdict):
					retdict[(startPoint[0], startPoint[1] + num)] = startPoint[2] + num
			startPoint = (startPoint[0], startPoint[1] + mag, startPoint[2] + mag)
		elif vector.startswith('D'):
			for num in range(1, mag + 1):
				if ((startPoint[0], startPoint[1] - num) not in retdict):
					retdict[(startPoint[0], startPoint[1] - num)] = startPoint[2] + num
			startPoint = (startPoint[0], startPoint[1] - mag, startPoint[2] + mag)
		elif vector.startswith('L'):
			for num in range(1, mag + 1):
				if ((startPoint[0] - num, startPoint[1]) not in retdict):
					retdict[(startPoint[0] - num, startPoint[1])] = startPoint[2] + num
			startPoint = (startPoint[0] - mag, startPoint[1], startPoint[2] + mag)
		elif vector.startswith('R'):
			for num in range(1, mag + 1):
				if ((startPoint[0] + num, startPoint[1]) not in retdict):
					retdict[(startPoint[0] + num, startPoint[1])] = startPoint[2] + num
			startPoint = (startPoint[0] + mag, startPoint[1], startPoint[2] + mag)
		else:
			print("Found a weird word.")
			print(vector)
			sys.exit()
	return retdict

def getDictIntersectionWithSteps(arr1, arr2):
	#Returns a dictionary of all points in both arr1 and arr2, along with their summed intersection
	retdict = dict()
	arr1keys = arr1.keys()
	arr2keys = arr2.keys()
	return arr1keys & arr2keys

def part1():
	with open("input.txt") as f:
		wire1 = f.readline()
		wire2 = f.readline()
		arr1 = wire1.split(',')
		arr2 = wire2.split(',')
		wire1set = getSet(arr1) #Keep a set of all points the wire occupies
		wire2set = getSet(arr2)
		intersection = wire1set & wire2set
		print(len(intersection))
		minDistance = getManhattanDistance(next(iter(intersection)))
		for point in intersection:
			#print(point)
			#print(getManhattanDistance(point))
			minDistance = minDistance if minDistance < getManhattanDistance(point) else getManhattanDistance(point)
		print("Min is " + str(minDistance))

def part2():
	with open("input.txt") as f:
		wire1 = f.readline()
		wire2 = f.readline()
		arr1 = wire1.split(',')
		arr2 = wire2.split(',')
		# wire1set = getSetWithSteps(arr1)
		# wire2set = getSetWithSteps(arr2)
		wire1dict = getDictWithSteps(arr1)
		wire2dict = getDictWithSteps(arr2)
		intersection = wire1dict.keys() & wire2dict.keys()
		minSum = sys.maxsize
		for point in intersection:
			#print(point)
			#print(getManhattanDistance(point))
			tempsum = wire1dict[point] + wire2dict[point]
			minSum = minSum if minSum < tempsum else tempsum
		print("Min is " + str(minSum))

def main():
	#part1()
	part2()

main()