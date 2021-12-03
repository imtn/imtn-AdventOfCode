import sys

def getInput():
	userInput = input("getInput() >>> ")
	return userInput

def getOutput(output):
	print(output)

def part1():
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
				return

			elif op == 1:
				#Take val1 at pos1, add it to val2 at pos2, and store it in pos3
				#parameter mode compatible
				val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
				val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
				pos3 = arr[index + 3]
				arr[pos3] = val1 + val2

				index += 4

			elif op == 2:
				#Take val1 at pos1, multiply it to val2 at pos2, and store it in pos3
				#parameter mode compatible
				val1 = arr[arr[index + 1]] if param[2] == "0" else arr[index + 1]
				val2 = arr[arr[index + 2]] if param[1] == "0" else arr[index + 2]
				pos3 = arr[index + 3]
				arr[pos3] = val1 * val2

				index += 4

			elif op == 3:
				# Get input and store in pos1
				pos1 = arr[index + 1]
				arr[pos1] = int(getInput())

				index += 2

			elif op == 4:
				# Output value in pos1
				#parameter mode compatible
				val1 = arr[arr[index+1]] if int(param) == 0 else arr[index+1]
				getOutput(val1)

				index += 2

			else:
				print("Found a different opcode: " + str(op))
				print("Exiting...")
				sys.exit()

def part2():
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
				arr[pos1] = int(getInput())

				index += 2

			elif op == 4:
				# Output value in pos1
				# parameter mode compatible
				val1 = arr[arr[index+1]] if int(param) == 0 else arr[index+1]
				getOutput(val1)

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


def main():
	#part1()
	part2()

main()