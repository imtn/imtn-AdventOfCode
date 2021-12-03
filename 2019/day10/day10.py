import math, sys
from sortedcontainers import SortedList

# astMap is the dictionary mapping (x, y) to asteroid/space
# x and y are the coordinates of the current asteroid we are looking from
# totalAsteroidCount is the total number of asteroids in astMap
# returns the number of asteroids in sight from current asteroid
def getAsteroidsInSight(astMap, currX, currY, totalAsteroidCount):
	blockedCount = 0
	for coordinate in astMap.keys():
		# check if coordinate is different from input (currX, currY) and is an asteroid
		if coordinate != (currX, currY) and astMap[coordinate] == "#":
			# For this one coordinate,
			# determine if there are any asteroids in between this one and (currX, currY)
			(thisX, thisY) = coordinate
			vectorX = thisX - currX
			vectorY = thisY - currY
			divisor = math.gcd(vectorX, vectorY)
			smallestIntVectorX = vectorX / divisor
			smallestIntVectorY = vectorY / divisor

			# Loop through each asteroid in line and check if any is an asteroid
			# For example, if we want to check for asteroids between (5, 3) and (11, 6)
			# We want to loop over [(7, 4), (9, 5)]
			xIter = currX
			yIter = currY
			while True:
				xIter += smallestIntVectorX
				yIter += smallestIntVectorY
				if (xIter, yIter) == coordinate:
					# We finished looping and didn't find any blocking asteroids
					break

				if astMap[(xIter, yIter)] == "#":
					blockedCount += 1
					print("From asteroid " + str((currX, currY)) + " to asteroid " + str(coordinate) + " we are blocked by " + str((xIter, yIter)))
					break # We found something blocked, break out of while loop

	return totalAsteroidCount - blockedCount - 1 # minus one so it doesn't count itself

# For part 2, calculate the distance between the passed in coordinate and the laser.
def calculateDistance(coordinate):
	laser = (11, 19)
	return math.sqrt( (coordinate[1] - laser[1])**2 + (coordinate[0] - laser[0])**2 )

def part1():

	# Store data in a dict
	# Where keys are the tuple (x, y)
	# And value is whether we have an asteroid or not
	astMap = dict()
	xValue = 0
	yValue = 0
	totalAsteroidCount = 0
	# I got the below hard-coded values by looking at the input
	width = 25
	height = 25

	with open("input.txt") as f:
		for line in f:
			line = line.strip()
			for char in line:
				astMap[(xValue, yValue)] = char
				xValue += 1
				if char == "#":
					totalAsteroidCount += 1
			yValue += 1
			xValue = 0

	# To find asteroid with best line of sight
	# Loop through each field in map and determine if current place is asteroid
	# If it is an asteroid, then loop through all other asteroids and determine if the other asteroid is blocked
	# Asteroids in sight equals totalAsteroidCount - # of blocked asteroids
	# Keep track of the x, y coordinate of asteroid with most in sight, as well as that number

	optimalTuple = (-1, -1)
	maxAsteroidsInSight = -1
	for x in range(width):
		for y in range(height):
			if astMap[(x, y)] == "#":
				astInSight = getAsteroidsInSight(astMap, x, y, totalAsteroidCount)
				#print("Asteroid " + str((x, y)) + " can see a total asts of " + str(astInSight))
				if astInSight > maxAsteroidsInSight:
					maxAsteroidsInSight = astInSight
					optimalTuple = (x, y)

	print("Best Asteroid is " + str(optimalTuple) + " which can see amt of asteroids = " + str(maxAsteroidsInSight))

def part2():
	# Monitoring station is on this coordinate as determined by part 1
	laser = (11, 19)
	# Dictionary mapping angles in degrees to a list of all asteroids with that angle, in order with the closest one last
	anglesTOcoors = dict()
	
	# Store data in a dict
	# Where keys are the tuple (x, y)
	# And value is whether we have an asteroid or not
	astMap = dict()
	xValue = 0
	yValue = 0
	totalAsteroidCount = 0

	with open("input.txt") as f:
		for line in f:
			line = line.strip()
			for char in line:
				astMap[(xValue, yValue)] = char
				xValue += 1
				if char == "#":
					totalAsteroidCount += 1
			yValue += 1
			xValue = 0

	# We have full asteroid map now
	# Now, loop through each asteroid except laser and determine its angle with atan2
	# Then keep a mapping of angle -> asteroids
	for coordinate in astMap.keys():
		# If this coordinate is not the laser, but it is an asteroid,
		# find its angle and register it in anglesTOcoors
		if coordinate != laser and astMap[coordinate] == "#":
			degreesTemp = math.degrees(math.atan2(coordinate[1] - laser[1], coordinate[0] - laser[0]))
			angle = degreesTemp if degreesTemp > 0 else 360 + degreesTemp
			angle = (angle+90)%360 # This is to compensate for how in programming, origin is at the top left, while in math, origin is at the lower left
			print("Coordinate " + str(coordinate) + " has temp " + str(degreesTemp) + " and angle " + str(angle))

			# if angle doesn't exist in anglesTOcoors then create a new sorted list
			# otherwise add into existing list
			if angle not in anglesTOcoors.keys():
				anglesTOcoors[angle] = SortedList(key = calculateDistance)

			anglesTOcoors[angle].add(coordinate)

	# print(totalAsteroidCount)
	# print(sum([len(sortList) for sortList in anglesTOcoors.values()]))

	# Get anglesTOcoors keys in increasing order,
	# and then go through each key and pop the first (closest) asteroid
	# keep track of each one we delete
	# print the asteroid's coordinates and which number it is
	numberLasered = 0
	while anglesTOcoors: # if this dictionary is empty it defaults to false
		anglesTemp = sorted(anglesTOcoors.keys()) # regen'd every loop for cases when key is removed
		for angle in anglesTemp:
			# For each angle
			# Increment the count
			# Print the count and coordinate
			# Pop the coordinate from the sortedlist in anglesTOcoors
			# Pop the angle key if the sortedlist is empty
			numberLasered += 1
			print("Lasered number " + str(numberLasered) + ", " + str(anglesTOcoors[angle].pop(0)) + " with angle " + str(angle))
			if not anglesTOcoors[angle]:
				del anglesTOcoors[angle]


def main():
	#part1()
	part2()

main()