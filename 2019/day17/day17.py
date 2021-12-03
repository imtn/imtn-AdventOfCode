import os, sys, time
from threading import Thread, Lock, Event

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
	print("get input")
	if len(globalInput) == 0:
		inputFlag.wait()
		inputMutex.acquire()
		try:
			userInput = globalInput.pop(0)
		finally:
			inputMutex.release()
			inputFlag.clear()
	else:
		userInput = globalInput.pop(0)
		print("got output")
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

def isPresentAndScaffold(scaffoldMap, coordinate):
	# scaffoldMap is map of (x,y)=>block
	# coordinate is (x,y)
	return coordinate in scaffoldMap and scaffoldMap[coordinate] == "#"

def part1():
	# chr(num) takes in an ascii number and returns the appropriate ascii character
	
	intcodeProgram = Thread(target = intcode, args = ("input1.txt", ))
	intcodeProgram.start()

	intcodeProgram.join()
	print(len(globalOutput))
	xCounter = 0
	yCounter = 0
	xMax = 0
	yMax = 0
	scaffoldMap = dict() # maps (x,y) to block
	for number in globalOutput:
		if number != 10:
			# if not newline, then add it
			scaffoldMap[(xCounter, yCounter)] = chr(number)
			xCounter += 1
			if xCounter > xMax: xMax = xCounter
		elif number == 10:
			xCounter = 0
			if yCounter > yMax: yMax = yCounter
			yCounter += 1
		else:
			print("Found weird number " + str(number))
			return

	for y in range(yMax):
		for x in range(xMax):
			sys.stdout.write(scaffoldMap[(x, y)])
		print()

	# loop through scaffoldMap
	# check if is an intersection
	# 	is intersection if current is "#" and surrounded by four "#"
	# if intersection, calculate alignment parameter
	# add alignment parameter to running sum

	alignParamSum = 0
	for y in range(yMax):
		for x in range(xMax):
			if (scaffoldMap[(x, y)] == "#" and
				isPresentAndScaffold(scaffoldMap, (x,y+1)) and
				isPresentAndScaffold(scaffoldMap, (x,y-1)) and
				isPresentAndScaffold(scaffoldMap, (x+1,y)) and
				isPresentAndScaffold(scaffoldMap, (x-1,y))
				):
				# we found intersection
				# add alignment parameter to sum
				alignParamSum += (x*y)
	print("Sum is " + str(alignParamSum))


def part2():
	# This doesn't use part 1 at all
	intcodeProgram = Thread(target = intcode, args = ("input2.txt", ))
	intcodeProgram.start()

	MAIN = "A,B,A,B,C,B,C,A,C,C"
	A = "R,12,L,10,L,10"
	B = "L,6,L,12,R,12,L,4"
	C = "L,12,R,12,L,6"
	newline = "10"

	string = ""

	time.sleep(1)
	for num in globalOutput:
		string += chr(num)
	print(string)

	# first provide input
	# 	end each with a newline
	# 	provide main
	# 	provide A
	# 	provide B
	# 	provide C
	# 	then provide y or n for continuous video feed

	# provide all of the inputs at once
	inputMutex.acquire()
	try:
		for letter in MAIN:
			globalInput.append(ord(letter))
		globalInput.append(newline)
		for letter in A:
			globalInput.append(ord(letter))
		globalInput.append(newline)
		for letter in B:
			globalInput.append(ord(letter))
		globalInput.append(newline)
		for letter in C:
			globalInput.append(ord(letter))
		globalInput.append(newline)
		globalInput.append(ord("n"))
		globalInput.append(newline)
	finally:
		inputFlag.set()
		inputMutex.release()

	intcodeProgram.join()
	print("Done!")
	for item in globalOutput:
		try:
			sys.stdout.write(chr(item))
		except ValueError:
			sys.stdout.write(str(item))
		finally:
			pass
	print()

def main():
	#part1()
	part2()

main()