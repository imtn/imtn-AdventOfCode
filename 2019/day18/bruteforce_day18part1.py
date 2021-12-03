import copy, sys

class path:
	# a single path, represents a single search
	# to find the shortest path, part1 will have an array of multiple paths
	# a path has the following data/variables
	# 	current coordinates, to know where it came from
	# 	coordinates of where it was one step ago, to know in which direction to move
	# 	steps, how many steps it has taken to get to where it is now
	# 	a set of keys it already has

	def __init__(self, currPos, prevPos, steps, keySet):
		self.currPos = currPos # (x, y)
		self.prevPos = prevPos # (x, y)
		self.steps = steps # a positive integer
		self.keySet = keySet # a set of lowercase characters

	def __str__(self):
		return "currPos: " + str(self.currPos) + " prevPos: " + str(self.prevPos) + " steps: " + str(self.steps) + " keySet: " + str(self.keySet)

	# Moves this path one step to the new position, which is assumed to be one step away from currPos
	def advance(self, newPos):
		self.steps += 1
		self.prevPos = self.currPos
		self.currPos = newPos

	def addKey(self, key):
		self.keySet.add(key)

def printMap(tunnelMap, xMax, yMax):
	for y in range(yMax):
		for x in range(xMax):
			sys.stdout.write(tunnelMap[(x, y)])
		print()

# returns a list of blocks around pos that are not the excludedTile or a wall
def getAdjacentBlocksNotWalls(pos, tunnelMap, excludedTile = None):
	# for every block in a cardinal position around this block
	# if it's not the excludedTile, add it to the return list
	returnThis = []
	if (pos[0], pos[1] + 1) != excludedTile and tunnelMap[(pos[0], pos[1] + 1)] != "#":
		returnThis.append((pos[0], pos[1] + 1))
	if (pos[0], pos[1] - 1) != excludedTile and tunnelMap[(pos[0], pos[1] - 1)] != "#":
		returnThis.append((pos[0], pos[1] - 1))
	if (pos[0] + 1, pos[1]) != excludedTile and tunnelMap[(pos[0] + 1, pos[1])] != "#":
		returnThis.append((pos[0] + 1, pos[1]))
	if (pos[0] - 1, pos[1]) != excludedTile and tunnelMap[(pos[0] - 1, pos[1])] != "#":
		returnThis.append((pos[0] - 1, pos[1]))
	return returnThis

# pos1 and pos2 are (x, y) tuples
def getManhattanDistance(pos1, pos2):
	return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# this should return a list of paths following the path passed in
# if, on the way, it acquires a key
# 	it prints the stepcount if it has numberOfKeys keys
def getNextPaths(thisPath, tunnelMap, numberOfKeys):
	# 	Move it forward (and around corners) until it hits a dead-end, a door it can't open, an intersection, or a key
	# 		If we hit a dead-end or an un-openable door, then don't append this path back
	# 		If we hit a door that we have a key for, just keep moving on
	# 		If we hit a key, add it to this path's collection, then make copies of path down each way
	# 		If we hit the special intersection, return all of the exits except the one we came from
	# 		if we hit an intersection, create copies of path to go down each way except the way we came from
	# 		If it is both key and intersection, treat it like a key

	# This is the 3x3 intersection in the middle of the map.
	specialIntersection = [(39, 39), (39, 40), (39, 41),
						   (40, 39), (40, 40), (40, 41),
						   (41, 39), (41, 40), (41, 41)]
   # This is a list of the exits for the special intersection
   # Mapped to the prevPos for that exit
	specialExits = {(38, 39): (39,39), (41,38): (41, 39), (42, 39): (41, 39),
					(42, 41): (41, 41), (41, 42): (41, 41), (39, 42): (39, 41)}
	nextPaths = []

	# this conditional covers the start, where we begin in the middle of a 3x3 room
	if thisPath.currPos == (40,40):
		for specialExit in specialExits.keys():
			# for each exit
			# create a copy of thisPath with a new currPos, new prevPos, and new steps
			newPath = path(specialExit, specialExits[specialExit], thisPath.steps + getManhattanDistance(thisPath.currPos, specialExit), thisPath.keySet.copy())
			nextPaths.append(newPath)
		return nextPaths


	# while loop keeps moving us forward if we haven't
	while True: #break at deadend, unopenable door, key, or intersection

		# if we are on a key not collected yet, collect it and then spread in all directions
		if tunnelMap[thisPath.currPos].islower() and tunnelMap[thisPath.currPos] not in thisPath.keySet:
			# add key to set
			# branch in all directions
			thisPath.addKey(tunnelMap[thisPath.currPos])

			# if we have found all keys
			if len(thisPath.keySet) == numberOfKeys:
				print("Found all keys!")
				print(thisPath)
				return []
			adjacentToKey = getAdjacentBlocksNotWalls(blockPos, tunnelMap)
			for keyAdjacentBlock in adjacentToKey:
				# if the adjacent block is not an unopenable door
				if not (tunnelMap[keyAdjacentBlock].isupper() and tunnelMap[keyAdjacentBlock].lower() not in thisPath.keySet):
					keyAdjacentPath = copy.deepcopy(thisPath) # make a copy of thisPath
					keyAdjacentPath.advance(keyAdjacentBlock) # advance it in a direction
					nextPaths.append(keyAdjacentPath) # add it to the returning set
			return nextPaths


		adjacentBlocks = getAdjacentBlocksNotWalls(thisPath.currPos, tunnelMap, thisPath.prevPos)
		if not adjacentBlocks:
			# if there are no paths forward, then dead end
			# kill this path, meaning don't return it again
			return []
		if len(adjacentBlocks) == 1:
			#if not an intersection
			blockPos = adjacentBlocks[0]
			block = tunnelMap[adjacentBlocks[0]]

			# if we come to an un-openable door, kill path
			if block.isupper() and block.lower() not in thisPath.keySet:
				return []

			# if we come to the special intersection
			elif blockPos in specialIntersection:
				# return a copy of the path in all directions
				for specialExit in specialExits.keys():
					# for each exit
					# if the prevPos for the exit isn't thisPath.currPos
					# then create a copy of thisPath with a new currPos, new prevPos, and new steps
					if specialExits[specialExit] != thisPath.currPos:
						newPath = path(specialExit, specialExits[specialExit], thisPath.steps + getManhattanDistance(thisPath.currPos, specialExit), thisPath.keySet.copy())
						nextPaths.append(newPath)
				return nextPaths

			# if we come to an openable door, just continue through it
			elif block.isupper() and block.lower() in thisPath.keySet:
				thisPath.advance(blockPos)

			# empty space or a key (have it or not), move there
			# keys are collected first
			elif block == "." or block.islower():
				thisPath.advance(blockPos)

			else:
				print("Found weird block: " + str(block) + " at position " + blockPos)
				sys.exit()
		else: # at an intersection
			for adjBlock in adjacentBlocks:
				# if it's not an  unopenable door, move there
				if not (tunnelMap[adjBlock].isupper() and tunnelMap[adjBlock].lower() not in thisPath.keySet):
					newPath = copy.deepcopy(thisPath)
					newPath.advance(adjBlock)
					nextPaths.append(newPath)
			return nextPaths




def part1():
	tunnelMap = dict() # maps (x, y) => block
	with open("input.txt") as f:
		xCounter = 0
		yCounter = 0
		xMax = 0
		yMax = 0
		numberOfKeys = 0
		start = (0,0) # not really, we'll populate this later
		for line in f:
			line = line.strip()
			for char in line:
				tunnelMap[(xCounter, yCounter)] = char
				if char == "@":
					start = (xCounter,yCounter)
				if char.islower():
					numberOfKeys += 1
				xCounter += 1
				if xMax < xCounter: xMax = xCounter
			xCounter = 0
			yCounter += 1
			if yMax < yCounter: yMax = yCounter

	# printMap(tunnelMap, xMax, yMax)

	paths = [path(start, start, 0, set())]

	# high-level: we go through the map,
	# and every time we come to an intersection,
	# we split and search down all paths except the one we came from
	# every time we come to a key
	# we split and search down all paths including the one we came from
	# every time we hit a door or a dead end
	# we kill this path
	# wait for paths to be empty to break the while loop
	# 	and hope we don't get an infinite loop somewhere :crossed_fingers:
	#
	# Have a special case for the middle 3x3 room
	# because otherwise, it would create lots of extra paths
	# and potentially cause an infinite loop around the perimeter

	while paths:

		# each loop, pop the first thing from paths
		# 	Move it forward until it hits a dead-end, a door it can't open, an intersection, or a key
		# 		If we hit a dead-end or an un-openable door, then don't append this path back
		# 		if we hit an intersection, create copies of path to go down each way except the way we came from
		# 		If we hit a key, add it to this path's collection, then make copies of path down each way
		# 		If it is both key and intersection, treat it like a key

		currPath = paths.pop(0)
		pathsToAppend = getNextPaths(currPath, tunnelMap, numberOfKeys)
		paths.extend(pathsToAppend)
		# print(len(paths))


def part2():
	pass

def main():
	part1()
	part2()

main()