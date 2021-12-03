import sys

def getInput():
	userInput = input("getInput() >>> ")
	return userInput

def setOutput(output):
	print("setOutput() >>> " + str(output))

# This deprecated for getAddrGivenParamMode()
def getValueGivenParamMode(programDict, paramDigit, dictIndex, relativeBase):
	# programDict is the dictionary that represents the program. All memory outside program defaults to 0
	# paramDigit is a single positive digits that represents how to get the value
	# 	0 - position mode - take programDict[dictIndex] to be a newIndex,
	#							and then return programDict[newIndex]
	# 	1 - immediate mode - return programDict[dictIndex]
	# 	2 - relative mode - take programDict[dictIndex] as baseModifier,
	#							and then return programDict[relativeBase + baseModifier]
	# dictIndex is the index of programDict that this paramDigit decides how we get
	# relativeBase is the relative base for relative mode
	# returns the value at the address that paramDigit, dictIndex, and relativeBase indicate

	paramDigit = int(paramDigit)

	if paramDigit == 0:
		# position mode

		address = programDict.get(dictIndex, 0) # Unlikely but possible
		return programDict.get(address, 0)
	elif paramDigit == 1:
		# immediate mode

		return programDict.get(dictIndex, 0)
	elif paramDigit == 2:
		# relative mode

		baseModifier = programDict.get(dictIndex, 0) # I don't see this happening, but just in case
		# print("Relative mode sum is " + str(relativeBase + baseModifier))
		return programDict.get(relativeBase + baseModifier, 0)
	else:
		print("Got weird paramDigit: " + str(paramDigit) + str(type(paramDigit)))
		sys.exit()
		return

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


def part1():
	with open('input.txt') as f:
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

def part2():
	# part 2 is to run part 1, but with input value 2 instead of 1
	pass

def main():
	part1()
	part2()

main()