# Runs the passed in program
# program is a list of strings, where each string is a single command
# returns tuple (status, accumulator) where
# 	status == 'infinite loop' if the same line is about to be run twice.
# 	status == 'eop' if it reaches the end of the program
def runProgram(program):
	index = 0
	instructionSet = set()
	accumulator = 0
	while(True):
		if index in instructionSet:
			return ('infinite loop', accumulator)
		if index >= len(program):
			return ('eop', accumulator)
		instructionSet.add(index)

		command = program[index].split(' ')[0]
		argument = program[index].split(' ')[1]

		if command == 'nop':
			index += 1
		elif command == 'acc':
			accumulator += int(argument)
			index += 1
		elif command == 'jmp':
			index += int(argument)
		else:
			print("Bad command during program line parsing: " + command + ' from ' + program[index])
			quit()

def part1():
	program = []
	with open('input.txt') as f:
		for line in f:
			program.append(line.strip())

	print(runProgram(program))

def part2():
	program = []
	with open('input.txt') as f:
		for line in f:
			program.append(line.strip())

	# loop through every line. if it's nop or jmp, replace it with the other, and then run program and see if it runs successfully
	for index, line in enumerate(program):
		if line.split(' ')[0] == 'nop' or line.split(' ')[0] == 'jmp':
			newLine = 'jmp ' + line.split(' ')[1] if line.split(' ')[0] == 'nop' else 'nop ' + line.split(' ')[1]
			newProgram = program.copy()
			newProgram[index] = newLine
			result = runProgram(newProgram)
			if result[0] == 'eop':
				print('EOP - ' + str(result[1]))

def main():
	part1()
	part2()
main()