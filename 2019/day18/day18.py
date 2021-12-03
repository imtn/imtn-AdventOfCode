import copy, sys

class Node:
	def __init__(self, value, vertexSet):
		self.value = value # a-z or @
		self.vertexSet = vertexSet

		#Attribute related to applying dijkstra's
		self.distance = sys.maxsize
		self.dKeySet = set()

	def __str__(self):
		string = "Node " + str(self.value) + " linked to: "
		for vertex in self.vertexSet:
			string += "(" + str(vertex.getOtherNode(self).value) + str(vertex.distance) + ") "
		return string

	def addVertex(self, newVertex):
		self.vertexSet.add(newVertex)

	# returns true if this node has a vertex with the other node
	def getVertexTo(self, otherNode):
		for vertex in self.vertexSet:
			if vertex.node1  == otherNode or vertex.node2 == otherNode:
				return vertex

	def addKey(self, key):
		self.dKeySet.add(key)

class Vertex:
	def __init__(self, node1, node2, distance, doorSet, kITM):
		self.node1 = node1
		self.node2 = node2
		self.distance = distance
		self.doorSet = doorSet
		self.keysInTheMiddle = kITM # set of keys

	def __str__(self):
		return str(self.node1) + " to " + str(self.node2) + " with distance " + str(self.distance) + " and doorSet " + str(self.doorSet) + " and kITM " + str(self.keysInTheMiddle)

	def getOtherNode(self, thisNode):
		if thisNode == self.node1:
			return self.node2
		elif thisNode == self.node2:
			return self.node1
		else:
			print("This node isn't related to this vertex: ", thisNode, type(thisNode), " | ", self, type(self))
			return None

	# Returns True if every door in this vertex can be unlocked
	def canPassThrough(self, keys):
		for door in self.doorSet:
			if door.lower() not in keys:
				return False
		return True

	# Returns False if any keys in the middle are not in the key
	def hasAllMiddleKeysCollected(self, keys):
		for key in self.keysInTheMiddle:
			if key not in keys:
				return False
		return True

	# Combination of the above two
	# Returns true if both conditions are satisfied
	def canPassThroughAndHasAllMiddleKeysCollected(self, keys):
		for door in self.doorSet:
			if door.lower() not in keys:
				return False
		for key in self.keysInTheMiddle:
			if key not in keys:
				return False
		return True

class Path:
	# a single path, represents a single search
	# a path has the following data/variables
	# 	current coordinates, to know where it came from
	# 	coordinates of where it was one step ago, to know in which direction to move
	# 	steps, how many steps it has taken to get to where it is now
	# 	a set of keys it already has

	def __init__(self, currPos, steps, doorSet, kITM):
		self.currPos = currPos # (x, y)
		self.steps = steps # a positive integer
		self.doorSet = doorSet # a set of uppercase characters
		self.keysInTheMiddle = kITM # set of lowercase characters

	def __str__(self):
		return "currPos: " + str(self.currPos) + " steps: " + str(self.steps) + " doorSet: " + str(self.doorSet)

	# Moves this path one step to the new position, which is assumed to be one step away from currPos
	def advance(self, newPos):
		self.steps += 1
		self.currPos = newPos

	def addDoor(self, door):
		self.doorSet.add(door)

	def addKey(self, key):
		self.keysInTheMiddle.add(key)

def printMap(tunnelMap, xMax, yMax):
	for y in range(yMax):
		for x in range(xMax):
			sys.stdout.write(tunnelMap[(x, y)])
		print()

# returns a list of blocks around pos that are not in the list/set of excludedTiles or a wall
def getAdjacentBlocksNotWalls(pos, tunnelMap, excludedTiles = None):
	# for every block in a cardinal position around this block
	# if it's not in the list/set of excludedTiles, add it to the return list
	returnThis = []
	if (pos[0], pos[1] + 1) not in excludedTiles and tunnelMap[(pos[0], pos[1] + 1)] != "#":
		returnThis.append((pos[0], pos[1] + 1))
	if (pos[0], pos[1] - 1) not in excludedTiles and tunnelMap[(pos[0], pos[1] - 1)] != "#":
		returnThis.append((pos[0], pos[1] - 1))
	if (pos[0] + 1, pos[1]) not in excludedTiles and tunnelMap[(pos[0] + 1, pos[1])] != "#":
		returnThis.append((pos[0] + 1, pos[1]))
	if (pos[0] - 1, pos[1]) not in excludedTiles and tunnelMap[(pos[0] - 1, pos[1])] != "#":
		returnThis.append((pos[0] - 1, pos[1]))
	return returnThis

# Returns a tuple of (numerical minimum distance, set of doors passed through, set of keys in the middle)
# Returns none if no path from fromKey to toKey
def findShortestDistanceWithDoorsBFS(fromKey, toKey, tunnelMap):
	# fromKey and toKey are the lowercase strings that represent the keys
	# keep a set of tiles we've already explored
	# keep a list of tiles we currently want to explore
	# every while loop, go through every path in paths
	# 	if current node is a door, then add that door to the doorSet
	# 	if current node is toKey, then return with tuple
	# 	otherwise, get all adjacent tiles, add them to the list
	# 	and then add the current node to the visited set
	visitedSet = set() # set of (x, y)
	currentPaths = [] # list of path objects

	# First, find coordinates of fromKey
	for coords, block in tunnelMap.items():
		if block == fromKey:
			currentPaths.append(Path(coords, 0, set(), set()))
			break

	if not currentPaths:
		print("Didn't find key ", fromKey)
		sys.exit()

	while currentPaths:
		newPaths = []
		for thisPath in currentPaths:
			pos = thisPath.currPos
			block = tunnelMap[pos]

			if block.isupper(): thisPath.addDoor(block)
			if block == toKey:
				return (thisPath.steps, thisPath.doorSet, thisPath.keysInTheMiddle)
			if block.islower() and block not in (fromKey, toKey):
				thisPath.addKey(block)


			adjacentAvailableBlocks = getAdjacentBlocksNotWalls(pos, tunnelMap, visitedSet)
			visitedSet.add(pos)
			if len(adjacentAvailableBlocks) == 1:
				thisPath.advance(adjacentAvailableBlocks[0])
				newPaths.append(thisPath)
			else:
				for adjBlock in adjacentAvailableBlocks:
					newPath = copy.deepcopy(thisPath)
					newPath.advance(adjBlock)
					newPaths.append(newPath)

		currentPaths = newPaths

	return None

# Returns the number of steps to travel the keystring
def getStepCount(keyString, nodeMap):
	stepCount = 0
	for i in range(len(keyString) - 1):
		stepCount += nodeMap[keyString[i]].getVertexTo(nodeMap[keyString[i+1]]).distance
	return stepCount

# Recursive method to find the minimal distance to go through all keys
# sso is a search string
# nodes maps each key (lowercase string) to a Node object
# reachableKeyCache maps a sorted ss and current key to a list of reachable keys
# recurseCache maps a sorted ss and current key to the findMinDist result, and the min distance to the next key
def findMinDist(ss, nodes, reachableKeyCache, recurseCache):
	result = sys.maxsize
	sortedSS = ''.join(sorted(ss))
	reachableKeys = []

	if (sortedSS, ss[-1]) in reachableKeyCache:
		reachableKeys = reachableKeyCache[(sortedSS, ss[-1])]
	else:
		for key in nodes.keys():
			if key not in ss and nodes[ss[-1]].getVertexTo(nodes[key]).canPassThroughAndHasAllMiddleKeysCollected(ss):
				reachableKeys.append(key)
		reachableKeyCache[(sortedSS, ss[-1])] = reachableKeys

	if not reachableKeys:
		return 0 # we have traversed everything

	for key in reachableKeys:
		distanceToKey = nodes[ss[-1]].getVertexTo(nodes[key]).distance
		if (sortedSS, ss[-1]) in recurseCache:
			tempDist = recurseCache[(sortedSS, ss[-1])]
		else:
			tempDist = findMinDist(ss + key, nodes, reachableKeyCache, recurseCache) + distanceToKey
		if tempDist < result: result = tempDist

	recurseCache[(sortedSS, ss[-1])] = result
	# print("distance is ", result, " for string ", ss)
	# input()
	return result

# Recursive method to find the minimal distance to go through all keys
# keySet is a set of keys
# currentKeys is a list of the position of each current key
# nodes maps each key (lowercase character) to a Node object
# reachableKeyCache maps a keySet and current key to a list of reachable keys
# recurseCache maps a keySet and currentKeys to the findMinDist result, and the min distance to the next key
def findMinDistGivenMultipleCurrentKeys(keySet, currentKeys, nodes, reachableKeyCache, recurseCache):
	print("Method called with keyset: ", keySet, " and currentKeys ", currentKeys)
	result = sys.maxsize
	startingCharacters = ['@', '$', '%', '^']
	frozenKeySet = frozenset(keySet) # this can be used in dictionaries
	# sortedKeySet = ''.join(sorted(ss))
	# currentKey = ss[-1]
	reachableKeys = []

	if (sortedKeySet, currentKey) in reachableKeyCache:
		reachableKeys = reachableKeyCache[(sortedKeySet, currentKey)]
	else:
		for key in nodes.keys():
			if key not in ss and nodes[currentKey].getVertexTo(nodes[key]).canPassThroughAndHasAllMiddleKeysCollected(ss):
				reachableKeys.append(key)
		reachableKeyCache[(sortedKeySet, currentKey)] = reachableKeys

	if not reachableKeys:
		return 0 # we have traversed everything

	for key in reachableKeys:
		distanceToKey = nodes[currentKey].getVertexTo(nodes[key]).distance
		if (sortedKeySet, currentKey) in recurseCache:
			tempDist = recurseCache[(sortedKeySet, currentKey)]
		else:
			tempDist = findMinDist(ss + key, nodes, reachableKeyCache, recurseCache) + distanceToKey
		if tempDist < result: result = tempDist

	recurseCache[(sortedKeySet, currentKey)] = result

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	# get the reachable keys for each current key
	for currentKey in currentKeys:
		if (frozenKeySet, currentKey) in reachableKeyCache:
			reachableKeys.extend(reachableKeyCache[(frozenKeySet, currentKey)])
		else:
			# loop through all vertices of current node and see if we can pass through the vertex
			# reachable keys should not be in keySet
			tempReachableKeys = []
			for vert in nodes[currentKey].vertexSet:
				otherKey = vert.getOtherNode(nodes[currentKey]).value
				if vert.canPassThroughAndHasAllMiddleKeysCollected(keySet) and otherKey not in keySet and otherKey not in startingCharacters:
					tempReachableKeys.append(otherKey)
			reachableKeys.extend(tempReachableKeys)
			reachableKeyCache[(frozenKeySet, currentKey)] = tempReachableKeys

	if not reachableKeys:
		return 0 # we have traversed everything

	print("Can reach ", reachableKeys)
	input()

	# loop through reachable keys and get from cache, or recurse
	for key in reachableKeys:
		currentKey = '' # we find the current key for this key so that we can calculate distance
		distanceToKey = 0 # populated below
		for vert in nodes[key].vertexSet:
			if vert.getOtherNode(nodes[key]).value in currentKeys:
				currentKey = vert.getOtherNode(nodes[key]).value
				distanceToKey = vert.distance
				break
		if currentKey == '':
			print("Didn't find current key")
			return

		modifiedCurrentKeys = currentKeys.copy()
		modifiedCurrentKeys.remove(currentKey)
		modifiedCurrentKeys.append(key) # this is what we call the recursive method with
		frozenModCurrKeys = frozenset(modifiedCurrentKeys)
		
		if (frozenKeySet, frozenModCurrKeys) in recurseCache:
			tempDist = recurseCache[(frozenKeySet, frozenModCurrKeys)]
		else:
			updatedKeySet = keySet.copy()
			updatedKeySet.add(key)
			tempDist = findMinDistGivenMultipleCurrentKeys(updatedKeySet, modifiedCurrentKeys, nodes, reachableKeyCache, recurseCache) + distanceToKey
		if tempDist < result: result = tempDist

	recurseCache[(frozenKeySet, frozenset(currentKeys))] = result
	# print("Returning result ", result)
	return result


def part1():
	tunnelMap = dict() # maps (x, y) => block
	keySet = set()
	with open("part1input.txt") as f:
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
					keySet.add(char)
				xCounter += 1
				if xMax < xCounter: xMax = xCounter
			xCounter = 0
			yCounter += 1
			if yMax < yCounter: yMax = yCounter

	# printMap(tunnelMap, xMax, yMax)

	startNode = Node("@", set())
	startNode.distance = 0

	# high-level: first we get a graph of nodes and vertices, where
	# 	node = @ or key. has a set of vertices to other nodes
	# 	vertex = represents the shortest path between two nodes, knows the length/distance and what doors are in the way
	# 	we will do this with a BDS
	# Then, use Dijkstra's to find the shortest path traversing the graph, starting at @

	nodes = dict() # dict of all nodes, mapping key string to node object. Should be size 27, a-z + @
	nodes["@"] = startNode
	# create the node object entries
	for key in keySet:
		nodes[key] = Node(key, set())

	# get min distance between each key in nodes
	for fromKey in nodes.keys():
		for toKey in nodes.keys():
			if fromKey != toKey:
				fromNode = nodes[fromKey]
				toNode = nodes[toKey]

				# if a mapping already exists in the reverse direction
				# use that instead of calculating it from scratch
				if toNode.getVertexTo(fromNode):
					# Use same vertex object, because we don't need to modify it
					fromNode.addVertex(toNode.getVertexTo(fromNode))
				else: # BFS to find it
					(minDistance, doorSet, kITM) = findShortestDistanceWithDoorsBFS(fromKey, toKey, tunnelMap)
					fromNode.addVertex(Vertex(fromNode, toNode, minDistance, doorSet, kITM))

	# I can't use dijkstra's because it creates a tree, rather than a single path.
	# solution is to instead solve it recursively (maybe iteratively instead, because the input is large?).
	# in other words ...
	# from the current node and keys, look for all reachable nodes. keep track of distance.
	# return distance traveled when no reachable nodes
	# find the minimum of these
	# to make it faster, have a lookup table mapping (currentKey, keySet) => set of reachable keys

	lookupTable = dict() # maps a lowercase string of keys, sorted, to a list of reachable keys
	queue = ["@"] # current key is at the end of the string. keys were gotten in order from beginning to end of this string
	minSteps = sys.maxsize

	# print("Smallest step count is ", minSteps)
	minSteps = findMinDist("@", nodes, dict(), dict())
	print("Min distance is ", minSteps)

def part2():
	tunnelMap = dict() # maps (x, y) => block
	keySet = set()
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
					keySet.add(char)
				xCounter += 1
				if xMax < xCounter: xMax = xCounter
			xCounter = 0
			yCounter += 1
			if yMax < yCounter: yMax = yCounter

	# four keys are at (39,39), (41,39), (39,41), (41,41)
	# represented by @, $, %, ^ respectively

	nodes = dict() # dict of all nodes, mapping key string to node object. Should be size 30, a-z + @$%^
	startingCharacters = ['@', '$', '%', '^']
	for startingCharacter in startingCharacters:
		nodes[startingCharacter] = Node(startingCharacter, set())

	# create the node object entries
	for key in keySet:
		nodes[key] = Node(key, set())

	# get min distance between each key in nodes
	for fromKey in nodes.keys():
		for toKey in nodes.keys():
			if fromKey != toKey:
				fromNode = nodes[fromKey]
				toNode = nodes[toKey]

				# if a mapping already exists in the reverse direction
				# use that instead of calculating it from scratch
				if toNode.getVertexTo(fromNode):
					# Use same vertex object, because we don't need to modify it
					fromNode.addVertex(toNode.getVertexTo(fromNode))
				else: # BFS to find it
					shortestDistance = findShortestDistanceWithDoorsBFS(fromKey, toKey, tunnelMap)
					if shortestDistance: # if we can connect these two keys
						(minDistance, doorSet, kITM) = shortestDistance
						fromNode.addVertex(Vertex(fromNode, toNode, minDistance, doorSet, kITM))

	minSteps = findMinDistGivenMultipleCurrentKeys(set(), startingCharacters, nodes, dict(), dict())
	print("Min steps is ", minSteps)

def main():
	#part1()
	part2()

main()