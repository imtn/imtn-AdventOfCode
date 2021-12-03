import sys
from threading import Thread, Lock, Event
import matplotlib.pyplot as plt

#Globals for sharing data between intcode and maincode
globalInput = []
globalOutput = []
inputMutex = Lock()
outputMutex = Lock()
inputFlag = Event() # Set when globalInput is populated
outputFlag = Event() # Set when globalOutput is populated 


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
	return userInput



def setOutput(output):
	outputMutex.acquire()
	try:
		globalOutput.append(output)
		if len(globalOutput) == 2: #TODO adjust for particular problem
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
	# This is the plan for how to implement this
	# intcodeProgram runs in a separate thread. I use mutexes
	# 	to blackbox it into an input-output thread, instead of
	# 	worrying about how it functions as well
	# Have a dictionary mapping (x,y) to (color, number of times painted)
	# 	color is black by default
	# While the intcode program runs:
	# 	1. provide input by putting color of tile in global input
	# 	2. wait for globalOutput to have two elements
	# 	3. take output, paint panel, move robot

	# For facing, 0 is up, 1 is right, 2 is down, 3 is left
	# This allows me to just add or subtract 1, %4, to change direction

	robot = (0,0)
	facing = 0
	hullMap = dict()
	intcodeProgram = Thread(target = intcode, args = ("input.txt", ))
	intcodeProgram.start()

	while(intcodeProgram.is_alive()):

		# First, provide input of color of square robot is on
		if not inputMutex.acquire(timeout = 3):
			print("inputMutex timed out, program thread is alive? " + str(intcodeProgram.is_alive()))
			break

		currColor = hullMap.get(robot, [0])[0]
		try:
			globalInput.append(currColor)
			inputFlag.set()
		finally:
			inputMutex.release()

		# Then, wait for output flag to get newColor and direction
		if not outputFlag.wait(3):
			print("outputFlag timed out, program thread is alive? " + str(intcodeProgram.is_alive()))
			break

		if not outputMutex.acquire(timeout = 3):
			print("outputMutex timed out, program thread is alive? " + str(intcodeProgram.is_alive()))
			break
		try:
			direction = globalOutput.pop()
			newColor = globalOutput.pop()
		finally:
			outputMutex.release()
			outputFlag.clear()

		# paint the square the robot is on
		if robot not in hullMap:
			hullMap[robot] = (0,0)
		hullMap[robot] = (newColor, hullMap[robot][1] + 1)

		#Move robot
		facing = facing + 1 if direction else facing - 1
		facing = facing % 4
		if facing == 0:
			#up
			robot = (robot[0], robot[1] + 1)
		elif facing == 1:
			#right
			robot = (robot[0] + 1, robot[1])
		elif facing == 2:
			# down
			robot = (robot[0], robot[1] - 1)
		elif facing == 3:
			# left
			robot = (robot[0] - 1, robot[1])
		else:
			print("facing is actually " + str(facing))
			sys.exit()

	print("intcode program done")
	totalSum = len([value for value in hullMap.values() if value[1] >= 1])
	print(totalSum)
	print(len(hullMap)) # same thing ... duh

def part2():
	# This is the plan for how to implement this
	# intcodeProgram runs in a separate thread. I use mutexes
	# 	to blackbox it into an input-output thread, instead of
	# 	worrying about how it functions as well
	# Have a dictionary mapping (x,y) to (color, number of times painted)
	# 	color is black by default
	# While the intcode program runs:
	# 	1. provide input by putting color of tile in global input
	# 	2. wait for globalOutput to have two elements
	# 	3. take output, paint panel, move robot

	# For facing, 0 is up, 1 is right, 2 is down, 3 is left
	# This allows me to just add or subtract 1, %4, to change direction

	robot = (0,0)
	facing = 0
	hullMap = dict()
	hullMap[(0,0)] = (1,0) # Robot starts on a white square
	intcodeProgram = Thread(target = intcode, args = ("input.txt", ))
	intcodeProgram.start()

	while(intcodeProgram.is_alive()):

		# First, provide input of color of square robot is on
		if not inputMutex.acquire(timeout = 3):
			print("inputMutex timed out, program thread is alive? " + str(intcodeProgram.is_alive()))
			break

		currColor = hullMap.get(robot, [0])[0]
		try:
			globalInput.append(currColor)
			inputFlag.set()
		finally:
			inputMutex.release()

		# Then, wait for output flag to get newColor and direction
		if not outputFlag.wait(3):
			print("outputFlag timed out, program thread is alive? " + str(intcodeProgram.is_alive()))
			break

		if not outputMutex.acquire(timeout = 3):
			print("outputMutex timed out, program thread is alive? " + str(intcodeProgram.is_alive()))
			break
		try:
			direction = globalOutput.pop()
			newColor = globalOutput.pop()
		finally:
			outputMutex.release()
			outputFlag.clear()

		# paint the square the robot is on
		if robot not in hullMap:
			hullMap[robot] = (0,0)
		hullMap[robot] = (newColor, hullMap[robot][1] + 1)

		#Move robot
		facing = facing + 1 if direction else facing - 1
		facing = facing % 4
		if facing == 0:
			#up
			robot = (robot[0], robot[1] + 1)
		elif facing == 1:
			#right
			robot = (robot[0] + 1, robot[1])
		elif facing == 2:
			# down
			robot = (robot[0], robot[1] - 1)
		elif facing == 3:
			# left
			robot = (robot[0] - 1, robot[1])
		else:
			print("facing is actually " + str(facing))
			sys.exit()

	print("intcode program done")
	print(hullMap.keys())
	# xs = [tup[0] for tup in hullMap.keys()]
	# ys = [tup[1] for tup in hullMap.keys()]
	xs = []
	ys = []
	for key in hullMap.keys():
		if hullMap[key][0] == 1:
			xs.append(key[0])
			ys.append(key[1])
	plt.scatter(xs, ys)
	plt.show()

def main():
	#part1()
	part2()

main()