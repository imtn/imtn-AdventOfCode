import itertools

# def getInput():
# 	userInput = input("getInput() >>> ")
# 	return userInput

def setOutput(output):
	print("Output is " + str(output))
	previousOutput = output
	return output

def part1intcode(inputs):
	#inputs is an array from which the input step will call "pop(0)" every time
	# in day 7 part 1 specifically, each time the code is ran there is only one thing output
	outputValue = -1

	with open('input.txt') as f:
		arr = f.readlines()[0].split(',')
		for index, value in enumerate(arr):
			arr[index] = int(value) # Make each value an integer, not a string

		# Run the opcode program, stop on 99
		index = 0 # this is the pointer
		while True:
			num = arr[index]
			param = str(num // 100).zfill(3)
			op = num % 100
			# print("index is " + str(index))
			# print("four numbers are " + str(num) + " " + str(arr[index+1]) + " " + str(arr[index+2]) + " " + str(arr[index+3]))

			if op == 99:
				# End Processing, and do whatever needs to happen before exiting
				print("Finished processing.")
				return outputValue

			elif op == 1:
				# Take val1 at pos1, add it to val2 at pos2, and store it in pos3
				# parameter mode compatible
				val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
				val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
				pos3 = arr[index + 3]
				arr[pos3] = val1 + val2

				index += 4

			elif op == 2:
				# Take val1 at pos1, multiply it to val2 at pos2, and store it in pos3
				# parameter mode compatible
				val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
				val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
				pos3 = arr[index + 3]
				arr[pos3] = val1 * val2

				index += 4

			elif op == 3:
				# Get input and store in pos1
				pos1 = arr[index + 1]
				arr[pos1] = inputs.pop(0)

				index += 2

			elif op == 4:
				# Output value in pos1
				# parameter mode compatible
				val1 = arr[arr[index+1]] if int(param) == 0 else arr[index+1]
				outputValue = val1

				index += 2

			elif op == 5:
				# jump if true
				# if val1 is non-zero, set index to val2
				# otherwise, advance index normally
				# param mode compatible
				val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
				val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
				if val1 != 0:
					index = val2
				else:
					index += 3

			elif op == 6:
				# jump if not true
				# if val1 is zero, set index to val2
				# otherwise, advance index normally
				# pmode compatible
				val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
				val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
				if val1 == 0:
					index = val2
				else:
					index += 3

			elif op == 7:
				# less than
				# if val1 < val2 then store ONE in pos3
				# else store 0 in pos3
				val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
				val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
				pos3 = arr[index + 3]
				arr[pos3] = 1 if val1 < val2 else 0

				index += 4

			elif op == 8:
				# equal to
				# if val1 == val2 then store ONE in pos3
				# else store 0 in pos3
				val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
				val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
				pos3 = arr[index + 3]
				arr[pos3] = 1 if val1 == val2 else 0

				index += 4

			else:
				print("Found a different opcode: " + str(op))
				print("Exiting...")
				sys.exit()

def part2intcode(inputs, phase = 0):
	#inputs will be the program, as an array of ints, the pointer, and the input. (array, pointer, input)
	#returns when outputting a value, and when op == 99
	#Return value when outputting is (array, pointer, output)
	#No return value when op == 99
	#phase is taken by input if it exists

	(arr, index, inputValue) = inputs


	# Run the opcode program
	while True:
		num = arr[index]
		param = str(num // 100).zfill(3)
		op = num % 100
		# print("index is " + str(index))
		# print("four numbers are " + str(num) + " " + str(arr[index+1]) + " " + str(arr[index+2]) + " " + str(arr[index+3]))

		if op == 99:
			# End Processing, and do whatever needs to happen before exiting
			print("Finished processing.")
			return 

		elif op == 1:
			# Take val1 at pos1, add it to val2 at pos2, and store it in pos3
			# parameter mode compatible
			val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
			val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
			pos3 = arr[index + 3]
			arr[pos3] = val1 + val2

			index += 4

		elif op == 2:
			# Take val1 at pos1, multiply it to val2 at pos2, and store it in pos3
			# parameter mode compatible
			val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
			val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
			pos3 = arr[index + 3]
			arr[pos3] = val1 * val2

			index += 4

		elif op == 3:
			# Get input and store in pos1
			pos1 = arr[index + 1]

			if phase != 0:
				arr[pos1] = phase
				phase = 0
			else:
				arr[pos1] = inputValue

			index += 2

		elif op == 4:
			# Output value in pos1
			# parameter mode compatible
			val1 = arr[arr[index+1]] if int(param) == 0 else arr[index+1]
			outputValue = val1

			index += 2
			return (arr, index, outputValue)

		elif op == 5:
			# jump if true
			# if val1 is non-zero, set index to val2
			# otherwise, advance index normally
			# param mode compatible
			val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
			val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
			if val1 != 0:
				index = val2
			else:
				index += 3

		elif op == 6:
			# jump if not true
			# if val1 is zero, set index to val2
			# otherwise, advance index normally
			# pmode compatible
			val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
			val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
			if val1 == 0:
				index = val2
			else:
				index += 3

		elif op == 7:
			# less than
			# if val1 < val2 then store ONE in pos3
			# else store 0 in pos3
			val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
			val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
			pos3 = arr[index + 3]
			arr[pos3] = 1 if val1 < val2 else 0

			index += 4

		elif op == 8:
			# equal to
			# if val1 == val2 then store ONE in pos3
			# else store 0 in pos3
			val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
			val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
			pos3 = arr[index + 3]
			arr[pos3] = 1 if val1 == val2 else 0

			index += 4

		else:
			print("Found a different opcode: " + str(op))
			print("Exiting...")
			sys.exit()

def part1():
	# This is an iterator that returns a possible permutations of 0-4, in tuple form.
	inputTwo = 0
	maxNum = -1
	maxTuple = (0,0,0,0,0)
	perms = itertools.permutations(range(5))
	for permTuple in perms:
		for number in permTuple: # This should run five times per tuple. Because each tuple is five long.
			inputs = [number, inputTwo]
			inputTwo = part1intcode(inputs)
		if inputTwo > maxNum:
			maxNum = inputTwo
			maxTuple = permTuple
		inputTwo = 0
	print(maxNum)
	print(maxTuple)

def part2():
	# To have each computers A-E continually running, the intcode program will store program and index in some global vars
	with open('input.txt') as f:
		amp = f.readlines()[0].split(',')
		for index, value in enumerate(amp):
			amp[index] = int(value) # Make each value an integer, not a string

	# This is an iterator that returns a possible permutations of 5-9, in tuple form.
	perms = itertools.permutations(range(5, 10))
	maxNum = -1
	maxTuple = (0,0,0,0,0)
	for permTuple in perms:
		# For each tuple
		# Run each amp, with phase if it is the first time
		# take the output, if it's not None, then pass it to the next 
		# Run the next amp with input being output of previous amp
		# When all 5 are done, print the last output from E

		ampAoutput = part2intcode((amp, 0, 0), permTuple[0]) # Run A for the first time
		ampBoutput = part2intcode((amp.copy(), 0, ampAoutput[2]), permTuple[1]) # Run B for the first time
		ampCoutput = part2intcode((amp.copy(), 0, ampBoutput[2]), permTuple[2]) # Run C for the first time
		ampDoutput = part2intcode((amp.copy(), 0, ampCoutput[2]), permTuple[3]) # Run D for the first time
		ampEoutput = part2intcode((amp.copy(), 0, ampDoutput[2]), permTuple[4]) # Run E for the first time
		# Now that phase has been passed in, continually run these until they all halt with opcode 99
		while True:
			if ampEoutput == None:
				print("E outputs None!")
				print("Wait, what?")
				break
			ampAoutput = part2intcode((ampAoutput[0], ampAoutput[1], ampEoutput[2]))
			if ampAoutput == None:
				print("A outputs None!")
				finalOutput = ampEoutput[2]
				if finalOutput > maxNum:
					maxNum = finalOutput
					maxTuple = permTuple
				break 
			ampBoutput = part2intcode((ampBoutput[0], ampBoutput[1], ampAoutput[2]))
			if ampBoutput == None:
				print("B outputs None!")
				finalOutput = ampEoutput[2]
				if finalOutput > maxNum:
					maxNum = finalOutput
					maxTuple = permTuple
				break
			ampCoutput = part2intcode((ampCoutput[0], ampCoutput[1], ampBoutput[2]))
			if ampCoutput == None:
				print("C outputs None!")
				finalOutput = ampEoutput[2]
				if finalOutput > maxNum:
					maxNum = finalOutput
					maxTuple = permTuple
				break
			ampDoutput = part2intcode((ampDoutput[0], ampDoutput[1], ampCoutput[2]))
			if ampDoutput == None:
				print("D outputs None!")
				finalOutput = ampEoutput[2]
				if finalOutput > maxNum:
					maxNum = finalOutput
					maxTuple = permTuple
				break
			ampEoutput = part2intcode((ampEoutput[0], ampEoutput[1], ampDoutput[2]))

	print(maxNum)
	print(maxTuple)

def main():
	#part1()
	part2()

main()