import sys

def part1():
	# moon positions and velocities are stored in two separate dictionaries
	# mapping from moon name to 3-tuple of (x, y, z)
	pos = dict()
	vel = dict()
	names = ["io", "europa", "ganymede", "callisto"]
	with open("input.txt") as f:
		for line in f:
			splitLine = line.split(",")
			x = int(splitLine[0].split("=")[1])
			y = int(splitLine[1].split("=")[1])
			z = int(splitLine[2].split("=")[1].strip()[0:-1])
			name = names.pop(0)
			pos[name] = (x, y, z)
			vel[name] = (0, 0, 0)
	names = list(pos.keys())

	for i in range(1000):
		# update velocities
		for thisMoon in names:
			for otherMoon in names:
				if thisMoon != otherMoon:
					newX = vel[thisMoon][0]
					newY = vel[thisMoon][1]
					newZ = vel[thisMoon][2]

					if pos[otherMoon][0] > pos[thisMoon][0]:
						newX += 1
					elif pos[otherMoon][0] < pos[thisMoon][0]:
						newX -= 1

					if pos[otherMoon][1] > pos[thisMoon][1]:
						newY += 1
					elif pos[otherMoon][1] < pos[thisMoon][1]:
						newY -= 1

					if pos[otherMoon][2] > pos[thisMoon][2]:
						newZ += 1
					elif pos[otherMoon][2] < pos[thisMoon][2]:
						newZ -= 1

					vel[thisMoon] = (newX, newY, newZ)

		# update positions
		for moon in names:
			newX = pos[moon][0] + vel[moon][0]
			newY = pos[moon][1] + vel[moon][1]
			newZ = pos[moon][2] + vel[moon][2]
			pos[moon] = (newX, newY, newZ)


	totalEnergy = 0
	for moon in names:
		potentialEnergy = abs(pos[moon][0]) + abs(pos[moon][1]) + abs(pos[moon][2])
		kineticEnergy = abs(vel[moon][0]) + abs(vel[moon][1]) + abs(vel[moon][2])
		totalEnergy += potentialEnergy * kineticEnergy
	print(totalEnergy)

def part2():
	# every state has a unique previous and after state
	# Each axis (x, y, z) runs independent of each other
	# Find the cycle for each
	# And then find the Least Common Multiplier

	# moon positions and velocities are stored in two separate dictionaries
	# mapping from moon name to 3-tuple of (x, y, z)
	pos = dict()
	vel = dict()
	initialpos = dict()
	initialvel = dict()
	names = ["io", "europa", "ganymede", "callisto"]
	with open("input.txt") as f:
		for line in f:
			splitLine = line.split(",")
			x = int(splitLine[0].split("=")[1])
			y = int(splitLine[1].split("=")[1])
			z = int(splitLine[2].split("=")[1].strip()[0:-1])
			name = names.pop(0)
			pos[name] = (x, y, z)
			vel[name] = (0, 0, 0)
			initialpos[name] = (x, y, z)
			initialvel[name] = (0, 0, 0)
	names = list(pos.keys())

	# run until initial state detected
	stepCounter = 0
	while True:
		#Check if current x, y, or z equal to initial x, y, or z
		if xMatch(names, pos, vel, initialpos, initialvel):
			print("X axis matches at " + str(stepCounter) + " with pos " + str(pos) + " and vel " + str(vel))
		if yMatch(names, pos, vel, initialpos, initialvel):
			print("Y axis matches at " + str(stepCounter) + " with pos " + str(pos) + " and vel " + str(vel))
		if zMatch(names, pos, vel, initialpos, initialvel):
			print("Z axis matches at " + str(stepCounter) + " with pos " + str(pos) + " and vel " + str(vel))

		# update velocities
		for thisMoon in names:
			for otherMoon in names:
				if thisMoon != otherMoon:
					newX = vel[thisMoon][0]
					newY = vel[thisMoon][1]
					newZ = vel[thisMoon][2]

					if pos[otherMoon][0] > pos[thisMoon][0]:
						newX += 1
					elif pos[otherMoon][0] < pos[thisMoon][0]:
						newX -= 1

					if pos[otherMoon][1] > pos[thisMoon][1]:
						newY += 1
					elif pos[otherMoon][1] < pos[thisMoon][1]:
						newY -= 1

					if pos[otherMoon][2] > pos[thisMoon][2]:
						newZ += 1
					elif pos[otherMoon][2] < pos[thisMoon][2]:
						newZ -= 1

					vel[thisMoon] = (newX, newY, newZ)

		# update positions
		for moon in names:
			newX = pos[moon][0] + vel[moon][0]
			newY = pos[moon][1] + vel[moon][1]
			newZ = pos[moon][2] + vel[moon][2]
			pos[moon] = (newX, newY, newZ)

		stepCounter += 1

		# x cycles at 161428
		# y cycles at 231614
		# z cycles at 102356
		# find lcm
		# numpy.lcm.reduce([161428, 231614, 102356]) = 478373365921244

def xMatch(names, pos, vel, initialpos, initialvel):
	# If, for any moon, the x position doesn't match the initial position
	# 	or the x velocity doesn't match the initial velocity
	# Return false. Otherwise, return true
	for moon in names:
		if pos[moon][0] != initialpos[moon][0] or vel[moon][0] != initialvel[moon][0]:
			return False
	return True

def yMatch(names, pos, vel, initialpos, initialvel):
	# If, for any moon, the y position doesn't match the initial position
	# 	or the y velocity doesn't match the initial velocity
	# Return false. Otherwise, return true
	for moon in names:
		if pos[moon][1] != initialpos[moon][1] or vel[moon][1] != initialvel[moon][1]:
			return False
	return True

def zMatch(names, pos, vel, initialpos, initialvel):
	# If, for any moon, the z position doesn't match the initial position
	# 	or the z velocity doesn't match the initial velocity
	# Return false. Otherwise, return true
	for moon in names:
		if pos[moon][2] != initialpos[moon][2] or vel[moon][2] != initialvel[moon][2]:
			return False
	return True


def main():
	#part1()
	part2()

main()