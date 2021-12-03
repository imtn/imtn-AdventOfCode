import sys

goal = 19690720

def printArray(arr):
	for i in arr:
		print(i)

def part1():
	with open('input1202.txt') as f:
		arr = f.readlines()[0].split(',')
		for index, value in enumerate(arr):
			arr[index] = int(value) # Make each value an integer, not a string

		# Run the opcode program, stop on 99
		index = 0
		while True:
			op = arr[index]
			if op == 99:
				print("Finished processing.")
				print("Value at position 0 is " + str(arr[0]))
				return
			elif op == 1:
				#Take val1 at pos1, add it to val2 at pos2, and store it in pos3
				pos1 = arr[index + 1]
				pos2 = arr[index + 2]
				pos3 = arr[index + 3]
				arr[pos3] = arr[pos1] + arr[pos2]
			elif op == 2:
				#Take val1 at pos1, multiply it to val2 at pos2, and store it in pos3
				pos1 = arr[index + 1]
				pos2 = arr[index + 2]
				pos3 = arr[index + 3]
				arr[pos3] = arr[pos1] * arr[pos2]
			else:
				print("Found a different opcode: " + str(op))
				print("Exiting...")
				sys.exit()
			#Increment index
			index += 4

def runProgram(num1, num2):
	with open('input.txt') as f:
		arr = f.readlines()[0].split(',')
		for index, value in enumerate(arr):
			arr[index] = int(value) # Make each value an integer, not a string
		arr[1] = num1
		arr[2] = num2
		# Run the opcode program, stop on 99
		index = 0
		while True:
			op = arr[index]
			if op == 99:
				print("Finished processing.")
				print("Value at position 0 is " + str(arr[0]))
				return arr[0] #Returns the value at position 0
			elif op == 1:
				#Take val1 at pos1, add it to val2 at pos2, and store it in pos3
				pos1 = arr[index + 1]
				pos2 = arr[index + 2]
				pos3 = arr[index + 3]
				arr[pos3] = arr[pos1] + arr[pos2]
			elif op == 2:
				#Take val1 at pos1, multiply it to val2 at pos2, and store it in pos3
				pos1 = arr[index + 1]
				pos2 = arr[index + 2]
				pos3 = arr[index + 3]
				arr[pos3] = arr[pos1] * arr[pos2]
			else:
				print("Found a different opcode: " + str(op))
				print("Exiting...")
				sys.exit()
			#Increment index
			index += 4

def part2():
	for num1 in range(100):
		for num2 in range(100):
			result = runProgram(num1, num2)
			if result == goal:
				print( "(" + str(num1) + "," + str(num2) + ")")
				return

def main():
	part1()
	part2()

main()