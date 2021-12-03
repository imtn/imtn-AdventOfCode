def part1():
	line = ''
	with open('input.txt') as f:
		for l in f:
			# only one line in f
			line = l
	currentFloor = 0
	for letter in line:
		if letter == '(':
			currentFloor += 1
		elif letter == ')':
			currentFloor -= 1
		else:
			print("Bad input: " + letter)
			quit()
	print(currentFloor)

def part2():
	line = ''
	with open('input.txt') as f:
		for l in f:
			# only one line in f
			line = l
	currentFloor = 0
	for index, letter in enumerate(line):
		if letter == '(':
			currentFloor += 1
		elif letter == ')':
			currentFloor -= 1
		else:
			print("Bad input: " + letter)
			quit()

		if currentFloor == -1:
			print("Entered basement at position " + str(index+1))
			quit()

def main():
	part1()
	part2()
main()