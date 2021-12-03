#imports

def calcOrbitNum(tree, obj):
	total = 0
	curr = (obj,0) #(current object, number of orbits)
	upcoming = []
	#iterate rather than recurse to prevent stack overflow
	#for current node
	#add number of orbits to total
	#add orbitors with incremented number of orbits to upcoming
	#change curr to first item in upcoming, pop it
	while True:
		total += curr[1]
		if curr[0] in tree:
			for orbitor in tree[curr[0]]:
				upcoming.append((orbitor, curr[1]+1))
		if upcoming:
			curr = upcoming.pop(0)
		else:
			return total

#Returns distance from obj to Santa if Santa is here or a child, or -1 if Santa isn't here.
#excludedObj is not allowed to enter the upcoming list
def getDistanceIfSantaIsHereOrBelow(tree, obj, excludedObj):
	curr = (obj, 0) # tuple of (object, distance)
	upcoming = []
	#for current node
	#if it is YSL, which Santa orbits around, return the distance
	#if it has children, add children with incremented distance to upcoming
	#if upcoming is not empty, then it becomes the next thing in the upcoming
	#else return -1 because upcoming is empty in the end
	while True:
		if curr[0] == "YSL":
			print("Found Santa!")
			return curr[1]
		if curr[0] in tree:
			for orbitor in tree[curr[0]]:
				if orbitor != excludedObj:
					upcoming.append((orbitor, curr[1] + 1))
		if upcoming:
			curr = upcoming.pop()
		else:
			return -1

def part1():
	with open("input.txt") as f:
		#create tree
		#traverse tree and count orbits for each node
		#use dict where key is string of object, and value is list of strings of objects that orbit current string
		orbits = dict()

		#Create Tree
		for line in f:
			arr = line.strip().split(")")

			#Add to orbits
			if arr[0] in orbits:
				#Append to existing list
				orbits[arr[0]].append(arr[1])
			else:
				#Create new list
				orbits[arr[0]] = [arr[1]]

		#Traverse tree and calculate sum
		num = calcOrbitNum(orbits, "COM")
		print(num)


def part2():
	with open("input.txt") as f:
		#create tree
		#search from YOU to SAN
		#use dict where key is string of object, and value is list of strings of objects that orbit current string
		orbits = dict() #maps an object to what orbits it
		inverseOrbits = dict() # map of an object to what it orbits. Unique keys, but multiple keys may map to the same object

		#Create Tree
		for line in f:
			arr = line.strip().split(")") #an object)what orbits it

			#Add to orbits
			if arr[0] in orbits:
				#Append to existing list
				orbits[arr[0]].append(arr[1])
			else:
				#Create new list
				orbits[arr[0]] = [arr[1]]

			#add to inverseOrbits
			#key should not exist already. assumes key doesn't exist.
			inverseOrbits[arr[1]] = arr[0]



		#Search from you to santa
		#YOU orbits around 3WJ
		#SAN orbits around YSL
		#Start from 3WJ, search children
		#keep going up one level, increasing distance and search from there
		#exclude the previous object we searched
		current = "3WJ"
		previous = None
		distance = 0
		while True:
			result = getDistanceIfSantaIsHereOrBelow(orbits, current, previous)
			print("Distance is " + str(distance))
			if result != -1:
				print("Found Total Distance!")
				print(distance + result)
				return
			else:
				previous = current
				current = inverseOrbits[current]
				distance += 1

def main():
	part1()
	part2()

main()