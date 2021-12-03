def findFuel(num):
	return num//3-2

def findFuelRecursive(num):
	if num//3-2 <= 0:
		return 0
	currentSum = num//3-2
	currentSum += findFuelRecursive(currentSum)
	return currentSum

def part1():
	sum = 0
	with open('input.txt') as f:
		for line in f:
			intline = int(line)
			# print(intline)
			sum += findFuel(intline)

	print("Sum is " + str(sum))

def part2():
	sum = 0
	with open('input.txt') as f:
		for line in f:
			intline = int(line)
			# print(intline)
			sum += findFuelRecursive(intline)

	print("Sum is " + str(sum))

def main():
	print(findFuelRecursive(1969))
	part1()
	part2()

main()