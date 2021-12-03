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
	def __init__(self, node1, node2, distance, doorSet):
		self.node1 = node1
		self.node2 = node2
		self.distance = distance
		self.doorSet = doorSet

	def __str__(self):
		return str(self.node1) + " to " + str(self.node2) + " with distance " + str(self.distance) + " and doorSet " + str(self.doorSet)

	def getOtherNode(self, thisNode):
		if thisNode == self.node1:
			return self.node2
		elif thisNode == self.node2:
			return self.node1
		else:
			print("This node isn't related to this vertex.")
			return None

	# Returns True if every door in this vertex can be unlocked
	def canPassThrough(self, keySet):
		for door in self.doorSet:
			if door.lower() not in keySet:
				return False
		return True


class Path:
	# a single path, represents a single search
	# a path has the following data/variables
	# 	current coordinates, to know where it came from
	# 	coordinates of where it was one step ago, to know in which direction to move
	# 	steps, how many steps it has taken to get to where it is now
	# 	a set of keys it already has

	def __init__(self, currPos, steps, doorSet):
		self.currPos = currPos # (x, y)
		self.steps = steps # a positive integer
		self.doorSet = doorSet # a set of lowercase characters

	def __str__(self):
		return "currPos: " + str(self.currPos) + " steps: " + str(self.steps) + " doorSet: " + str(self.doorSet)

	# Moves this path one step to the new position, which is assumed to be one step away from currPos
	def advance(self, newPos):
		self.steps += 1
		self.currPos = newPos

	def addDoor(self, door):
		self.doorSet.add(door)

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

# Returns a tuple of (numerical minimum distance, set of doors passed through)
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
			currentPaths.append(Path(coords, 0, set()))
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
				return (thisPath.steps, thisPath.doorSet)


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

def part1():
	tunnelMap = dict() # maps (x, y) => block
	keySet = set()
	with open("test.txt") as f:
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
					(minDistance, doorSet) = findShortestDistanceWithDoorsBFS(fromKey, toKey, tunnelMap)
					fromNode.addVertex(Vertex(fromNode, toNode, minDistance, doorSet))

	# Now use dijkstra's to find shortest path traversing the graph, starting at @
	unvisitedNodes = set()
	for node in nodes.values():
		unvisitedNodes.add(node)
	currNode = startNode

	while True:
		# for the current Node, if it has no unvisited neighbors, then we're done. print distance of current node
		# otherwise, loop through all unvisited neighbors
		# 	if this tentative distance is smaller than the node's distance, update distance and dKeySet
		# 		although if it has a door that we can't go to, then leave ignore it
		# after looping through all unvisited neighbors, move current node from unvisited to visited
		# 	we don't worry about things in visited, so there's no need to keep a set of them
		# choose the closest neighbor as the next currentNode

		# because every node is linked to every other, unvisitedNeighbors is unvisited - currNode
		unvisitedNeighbors = [n for n in unvisitedNodes if n != currNode]
		# if no unvisited neighbors, break and return
		if not unvisitedNeighbors:
			print("Calc'd shortest path to be ", currNode.distance)
			break

		# add key to keyset
		if currNode.value != "@":
			currNode.addKey(currNode.value)

		print("Considering node ", currNode.value, " with keys ", currNode.dKeySet, " and distance ", currNode.distance)

		# for each unvisited neighbor
		for otherNode in unvisitedNeighbors:
			sharedVertex = currNode.getVertexTo(otherNode)
			# calculate a tentative distance
			tentativeDistance = currNode.distance + sharedVertex.distance
			# if we have the keys to go through the doors
			if sharedVertex.canPassThrough(currNode.dKeySet):
				# update the other node's distance
				otherNode.distance = min(otherNode.distance, tentativeDistance)
				# if the distance was update with the tentative distance, then update the keyset to
				if otherNode.distance == tentativeDistance:
					otherNode.dKeySet = currNode.dKeySet

		# mark current node as visited
		unvisitedNodes.remove(currNode)

		# set next node to be the closest neighbor
		minNeighborDistance = sys.maxsize
		for otherNode in unvisitedNeighbors:
			if otherNode.distance < minNeighborDistance:
				minNeighborDistance = otherNode.distance
				currNode = otherNode
		print("Going to node ", currNode.value, " dist ", currNode.distance)
		

def part2():
	pass

def main():
	part1()
	part2()

main()