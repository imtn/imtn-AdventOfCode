import os, sys
from threading import Thread, Lock, Event

#Globals for sharing data between intcode and maincode
globalInput = []
globalOutput = []
inputMutex = Lock()
outputMutex = Lock()
inputFlag = Event() # Set when globalInput is populated
outputFlag = Event() # Set when globalOutput is populated 

def getRight(currentDirection):
	# 1 north, 2 south, 3 west, 4 east
	if currentDirection == 1:
		return 4
	elif currentDirection == 2:
		return 3
	elif currentDirection == 3:
		return 1
	elif currentDirection == 4:
		return 2
	else:
		print("Trying to get right for direction: " + str(currentDirection))
		return

def getLeft(currentDirection):
	# 1 north, 2 south, 3 west, 4 east
	if currentDirection == 1:
		return 3
	elif currentDirection == 2:
		return 4
	elif currentDirection == 3:
		return 2
	elif currentDirection == 4:
		return 1
	else:
		print("Trying to get left for direction: " + str(currentDirection))
		return

def getCoordinateInDirection(robot, currentDirection):
	# robot is an (x,y) tuple
	# currentDirection is 1-4

	if currentDirection == 1:
		return (robot[0], robot[1] - 1)
	elif currentDirection == 2:
		return (robot[0], robot[1] + 1)
	elif currentDirection == 3:
		return (robot[0] - 1, robot[1])
	elif currentDirection == 4:
		return (robot[0] + 1, robot[1])
	else:
		print("Tried to get coordinate for direction " + str(currentDirection))
		return

def getInput():
	#userInput = input("getInput() >>> ")

	# wait for inputFlag to be true
	inputFlag.wait()
	inputMutex.acquire()
	try:
		userInput = globalInput.pop()
	finally:
		inputMutex.release()
		inputFlag.clear()
	if userInput == -1:
		print("exiting intcode")
		sys.exit(0)
	return userInput



def setOutput(output):
	outputMutex.acquire()
	try:
		globalOutput.append(output)
		outputFlag.set()
	finally:
		outputMutex.release()
	#print("setOutput() >>> " + str(output))


def getAddrGivenParamMode(programDict, paramDigit, dictIndex, relativeBase):
	# programDict is the dictionary that represents the program. All memory outside program defaults to 0
	# paramDigit is a single positive digits that represents how to get the value
	# 	0 - position mode - return programDict[dictIndex] as the new index
	# 	1 - immediate mode - return dictIndex
	# 	2 - relative mode - take programDict[dictIndex] as baseModifier,
	#							and then return relativeBase + baseModifier as the new index
	# dictIndex is the index of programDict that this paramDigit decides how we get
	# relativeBase is the relative base for relative mode
	# returns the address and not the value that paramDigit, dictIndex, and relativeBase indicate
	paramDigit = int(paramDigit)

	if paramDigit == 0:
		# position mode

		return programDict.get(dictIndex, 0)

	elif paramDigit == 1:
		# immediate mode

		return dictIndex

	elif paramDigit == 2:
		# relative mode

		baseModifier = programDict.get(dictIndex, 0) # I don't see this happening, but just in case
		return baseModifier + relativeBase

	else:
		print("Got weird paramDigit: " + str(paramDigit) + str(type(paramDigit)))
		sys.exit()
		return

def intcode(filename):
	with open(filename) as f:
		program = dict() # store the program as a dictionary so we can access memory outside the program
		inputArray = f.readlines()[0].split(',')
		for index, value in enumerate(inputArray):
			program[index] = int(value) # Make each value an integer, not a string

		# Run the opcode program, stop on 99
		index = 0 # this is the pointer
		relativeBase = 0 # this is the relative base
		while True:
			num = program[index]
			param = str(num // 100).zfill(3)
			op = num % 100
			# print("index is " + str(index))
			# print("four numbers are " + str(num) + " " + str(program[index+1]) + " " + str(program[index+2]) + " " + str(program[index+3]))

			if op == 99:
				# End Processing, and do whatever needs to happen before exiting
				print("Finished processing.")
				return

			elif op == 1:
				# Take val1 at pos1, add it to val2 at pos2, and store it in pos3

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				pos3 = getAddrGivenParamMode(program, param[0], index + 3, relativeBase)
				program[pos3] = val1 + val2

				index += 4

			elif op == 2:
				# Take val1 at pos1, multiply it to val2 at pos2, and store it in pos3

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				pos3 = getAddrGivenParamMode(program, param[0], index + 3, relativeBase)
				program[pos3] = val1 * val2

				index += 4

			elif op == 3:
				# Get input and store in pos1

				pos1 = getAddrGivenParamMode(program, param, index + 1, relativeBase)
				program[pos1] = int(getInput())

				index += 2

			elif op == 4:
				# Output value in pos1

				val1 = program.get(getAddrGivenParamMode(program, int(param), index + 1, relativeBase), 0)
				setOutput(val1)

				index += 2

			elif op == 5:
				# jump if true
				# if val1 is non-zero, set index to val2
				# otherwise, advance index normally

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				if val1 != 0:
					index = val2
				else:
					index += 3

			elif op == 6:
				# jump if not true
				# if val1 is zero, set index to val2
				# otherwise, advance index normally

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				if val1 == 0:
					index = val2
				else:
					index += 3

			elif op == 7:
				# less than
				# if val1 < val2 then store ONE in pos3
				# else store 0 in pos3

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				pos3 = getAddrGivenParamMode(program, param[0], index + 3, relativeBase)
				program[pos3] = 1 if val1 < val2 else 0

				index += 4

			elif op == 8:
				# equal to
				# if val1 == val2 then store ONE in pos3
				# else store 0 in pos3

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				pos3 = getAddrGivenParamMode(program, param[0], index + 3, relativeBase)
				program[pos3] = 1 if val1 == val2 else 0

				index += 4

			elif op == 9:
				# adjust relative base
				# relative base += val1
				# val1 may be negative

				val1 = program.get(getAddrGivenParamMode(program, int(param), index + 1, relativeBase), 0)
				relativeBase += val1

				index += 2

			else:
				print("Found a different opcode: " + str(op))
				print("Exiting...")
				sys.exit()

def part1():

	# inputs to intcode
	# 	1 - north
	# 	2 - south
	# 	3 - west
	# 	4 - east
	# 	-1 - personally created, causes intcode thread to exit

	# outputs from intcode
	# 	0 - hit a wall. position not changed
	# 	1 - droid moved one step in direction
	# 	2 - droid moved one step in direction and found oxygen system

	intcodeProgram = Thread(target = intcode, args = ("input.txt", ))
	intcodeProgram.start()
	robot = (0,0)

	# maps (x,y) => block
	# block mapping:
	# 	D = robot
	# 	# = wall
	# 	* = oxygen
	# 	. = confirmed empty
	# 	empty space = undiscovered
	# 	! = robot on top of oxygen
	oxygenMap = dict() # maps (x,y)=>block
	oxygenMap[robot] = "D"

	# My plan is, at a high-level, manually enter directions and visually verify map
	# then repeatedly do this until I identify the location of the oxygen supply

	# every loop, give input, get output, build map, print it, repeat
	while True:
		# get input (from user)
		# pass in input
		# get output
		# update map
		# print map
		# 	dynamically print map sounds hard
		# 	I would have to identify the min and max for x and y
		# 	so, for now, have set map dimensions
		# 	of, say, from -50 to 50 on both the x and y dimensions
		# 	when drawing, of course. the data can go as far as it wants

		# get input from user
		robotInput = 0
		while robotInput not in [-1, 1, 2, 3, 4]:
			try:
				robotInput = int(input("provide robot input or -1 to exit >>> "))
			except:
				print("You probably didn't give a valid input")
			finally:
				pass
		# pass in input
		inputMutex.acquire()
		try:
			globalInput.append(robotInput)
			inputFlag.set()
		finally:
			inputMutex.release()

		# if -1, exit
		if robotInput == -1:
			print("exiting main thread")

		# get output
		outputFlag.wait()
		outputMutex.acquire()
		try:
			print("Global Output length")
			print(len(globalOutput))
			robotOutput = globalOutput.pop(0)
		finally:
			outputFlag.clear()
			outputMutex.release()

		# get target coordinates for updating map
		if robotInput == 1:
			# north
			target = (robot[0], robot[1] - 1)
		elif robotInput == 2:
			# south
			target = (robot[0], robot[1] + 1)
		elif robotInput == 3:
			# west
			target = (robot[0] - 1, robot[1])
		elif robotInput == 4:
			# east
			target = (robot[0] + 1, robot[1])
		else:
			print("Got weird robotInput: " + str(robotInput))
			sys.exit(0)

		print("robot moved " + str())

		# update map
		if robotOutput == 0:
			print("hit wall")
			# hit a wall, don't move robot, update map with wall
			oxygenMap[target] = "#"
		elif robotOutput == 1:
			print("moved")
			# robot successfully moved
			# if robot on oxygen, move robot, leave oxygen
			if oxygenMap[robot] == "!":
				oxygenMap[robot] = "*"
				oxygenMap[target] = "D"
				robot = target
			else:
				# move robot here
				# leave period in previous space
				oxygenMap[target] = "D"
				oxygenMap[robot] = "."
				robot = target
		elif robotOutput == 2:
			print("moved onto oxygen")
			# robot successfully moved onto oxygen
			# assumes only one oxygen in area
			oxygenMap[target] = "!"
			oxygenMap[robot] = "."
			robot = target
		else:
			print("Got weird output: " + str(robotOutput))
			sys.exit(0)

		#print map - statically, not dynamically
		for y in range(-29, 40):
			for x in range(-29, 40):
				if x == 0 and y == 0:
					sys.stdout.write("X") # starting spot, not stored this way
				else:
					sys.stdout.write(oxygenMap.get((x, y), " "))
			print()

def part2():

	# inputs to intcode
	# 	1 - north
	# 	2 - south
	# 	3 - west
	# 	4 - east
	# 	-1 - personally created, causes intcode thread to exit

	# outputs from intcode
	# 	0 - hit a wall. position not changed
	# 	1 - droid moved one step in direction
	# 	2 - droid moved one step in direction and found oxygen system

	intcodeProgram = Thread(target = intcode, args = ("input.txt", ))
	intcodeProgram.start()
	robot = (0,0)

	# maps (x,y) => block
	# block mapping:
	# 	D = robot
	# 	# = wall
	# 	* = oxygen
	# 	. = confirmed empty
	# 	empty space = undiscovered
	# 	! = robot on top of oxygen

	oxygenMap = dict() # maps (x,y)=>block
	oxygenMap[robot] = "D"
	unmappedBlocks = [] # list of (x,y) that have not been discovered yet
	facing = 2 # facing south, to better map the corner where the robot starts
	oxygen = (0,0) # not really, we'll populate this when uncovering the map

	# add any unmapped blocks around, to the list of unmapped blocks
	# unmappedBlocks.extend([getCoordinateInDirection(robot, dire) for dire in range(1,5) if getCoordinateInDirection(robot, dire) not in oxygenMap])
	for i in range(1,5):
		block = getCoordinateInDirection(robot, i)
		if block not in oxygenMap and block not in unmappedBlocks:
			unmappedBlocks.append(block)

	# My plan is, at a high-level, manually enter directions and visually verify map
	# then repeatedly do this until I identify the location of the oxygen supply

	# every loop, give input, get output, build map, print it, repeat
	while True:
		# get input (from user)
		# pass in input
		# get output
		# update map
		# print map
		# 	dynamically print map sounds hard
		# 	I would have to identify the min and max for x and y
		# 	so, for now, have set map dimensions
		# 	of, say, from -50 to 50 on both the x and y dimensions
		# 	when drawing, of course. the data can go as far as it wants

		# update - to map whole maze for part 2, input is gotten automatically
		# 	the robot will try to follow the wall on the right hand side
		# 	until there are no unmapped areas reachable from within the maze
		# so, the get automatic input will look like this
		# 	if the area to the right of where the robot is facing is unmapped
		# 	then go there. otherwise, if it is mapped:
		# 		if it is a wall, then keep trying to go forward, and turning left if we can't go forwards
		# 		if it is empty space or oxygen, go there
		# 	but before getting any movement, it first looks at the four cardinal directions around
		# 		and adds any ones not in the oxygenMap to unmappedBlocks
		# 		whenever we discover a block by checking the output
		# 		we remove it from unmappedBlocks if it's in there
		# 		we break when there are no unmappedBlocks
		# 		and display the map at the end.

		# get input automatically
		rightDirection = getRight(facing)
		robotRight = getCoordinateInDirection(robot, rightDirection)
		if robotRight not in oxygenMap:
			# print("AUTO: map right")
			# if the spot to the right of the robot is unmapped, then map it
			# if it is space and we move there, need to change facing when we get output
			robotInput = rightDirection
			triedToMapRight = True
		elif oxygenMap[robotRight] in [".", "*"]:
			# print("AUTO: move right")
			# if spot to right of robot is a traversable space, then go there
			facing = rightDirection
			robotInput = rightDirection
		elif oxygenMap[robotRight] == "#":
			# print("AUTO: wall on right")
			# if spot to right is wall, then try to go forward while we can, otherwise turn left try go forward
			forward = getCoordinateInDirection(robot, facing)

			# while there is a wall in front of us, turn left and check again
			# if unmapped space in front, we try to go there
			# which is same action we would take if there was space or oxygen ahead
			while oxygenMap.get(forward, ".") == "#": 
				facing = getLeft(facing) # turn left
				forward = getCoordinateInDirection(robot, facing) # get new forward to check

			# forward should not be something other than wall right now
			# go forward
			robotInput = facing
			# print("AUTO: now facing " + str(facing))

		else:
			print("Couldn't identify robotRight: " + str(oxygenMap[robotRight]))
			return

		# pass in input
		inputMutex.acquire()
		try:
			globalInput.append(robotInput)
			inputFlag.set()
		finally:
			inputMutex.release()

		# if -1, exit
		if robotInput == -1:
			print("exiting main thread")

		# get output
		outputFlag.wait()
		outputMutex.acquire()
		try:
			robotOutput = globalOutput.pop(0)
		finally:
			outputFlag.clear()
			outputMutex.release()

		# get target coordinates for updating map
		if robotInput == 1:
			# north
			target = (robot[0], robot[1] - 1)
		elif robotInput == 2:
			# south
			target = (robot[0], robot[1] + 1)
		elif robotInput == 3:
			# west
			target = (robot[0] - 1, robot[1])
		elif robotInput == 4:
			# east
			target = (robot[0] + 1, robot[1])
		else:
			print("Got weird robotInput: " + str(robotInput))
			sys.exit(0)

		# every time we move, we may map something
		# so if something is mapped, remove it from unmapped
		if target in unmappedBlocks:
			unmappedBlocks.remove(target)

		# update map
		if robotOutput == 0:
			# print("hit wall")
			# hit a wall, don't move robot, update map with wall
			oxygenMap[target] = "#"
			triedToMapRight = False
		elif robotOutput == 1:
			# print("moved")
			if triedToMapRight:
				facing = getRight(facing)
				triedToMapRight = False
			# robot successfully moved
			# if robot on oxygen, move robot, leave oxygen
			if oxygenMap[robot] == "!":
				oxygenMap[robot] = "*"
				oxygenMap[target] = "D"
				robot = target
			else:
				# move robot here
				# leave period in previous space
				oxygenMap[target] = "D"
				oxygenMap[robot] = "."
				robot = target
		elif robotOutput == 2:
			if triedToMapRight:
				facing = getRight(facing)
				triedToMapRight = False
			# print("moved onto oxygen")
			# robot successfully moved onto oxygen
			# assumes only one oxygen in area
			oxygenMap[target] = "!"
			oxygenMap[robot] = "."
			oxygen = target
			robot = target
		else:
			print("Got weird output: " + str(robotOutput))
			sys.exit(0)

		# print("Facing " + str(facing))

		#print map - statically, not dynamically
		# for y in range(-29, 40):
		# 	for x in range(-29, 40):
		# 		if x == 0 and y == 0:
		# 			sys.stdout.write("X") # starting spot, not stored this way
		# 		else:
		# 			sys.stdout.write(oxygenMap.get((x, y), " "))
		# 	print()	

		# input()
		# os.system("clear")

		for i in range(1,5):
			block = getCoordinateInDirection(robot, i)
			if block not in oxygenMap and block not in unmappedBlocks:
				unmappedBlocks.append(block)

		if len(unmappedBlocks) == 0:
			print("Done!")
			break

	# maze fully mapped
	# spread oxygen per loop
	# each loop, take the current list of adjacentBlocks
	# for each one, mark as "O" and add any neighbors not in adjacentBlocks and not "O" to a new list
	# set adjacentBlocks to be this new list
	# increment minute counter
	oxygenMap[robot] = "." if oxygenMap[robot] == "D" else "*" # remove robot from map
	oxygenMap[oxygen] = "O"
	adjacentBlocks = [getCoordinateInDirection(oxygen, direction) for direction in range(1,5) if oxygenMap[getCoordinateInDirection(oxygen, direction)] == "."]
	minuteCounter = 0
	# print("Oxygen is " + str(oxygen))
	# print(adjacentBlocks)
	while adjacentBlocks:
		# input()
		os.system("clear")
		newAdjacentBlocks = []
		for block in adjacentBlocks:
			# print("for block " + str(block))
			oxygenMap[block] = "O"
			for i in range(1,5):
				# for each adjacent, if it's not in adjacentBlocks or newAdjacentBlocks
				# and if it's not already oxygen, then add to newAdjacentBlocks
				adjacent = getCoordinateInDirection(block, i)
				if adjacent not in adjacentBlocks and getCoordinateInDirection(block, i) not in newAdjacentBlocks and oxygenMap[getCoordinateInDirection(block, i)] == ".":
					# print("Adding block to adjacentBlocks " + str(adjacent))
					newAdjacentBlocks.append(adjacent)
		adjacentBlocks = newAdjacentBlocks
		minuteCounter += 1

		#print map - statically, not dynamically
		for y in range(-29, 40):
			for x in range(-29, 40):
				if x == 0 and y == 0:
					sys.stdout.write("X") # starting spot, not stored this way
				else:
					sys.stdout.write(oxygenMap.get((x, y), " "))
			print()

	print("It took this many minutes: " + str(minuteCounter))


def main():
	#part1()
	part2()

main()