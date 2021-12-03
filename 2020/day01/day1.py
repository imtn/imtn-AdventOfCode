def part1():
	intArr = []
	intProd = 0
	with open("input.txt") as f:
		for line in f:
			intArr.append(int(line))

	for index1, value1 in enumerate(intArr):
		if index1 + 1 > len(intArr):
			continue
		for value2 in intArr[index1 + 1:]:
			if value1 + value2 == 2020:
					intProd = value1 * value2
	print(intProd) 

def part2():
	intArr = []
	intProd = 0
	with open("input.txt") as f:
		for line in f:
			intArr.append(int(line))

	for index1, value1 in enumerate(intArr):
		if index1 + 1 > len(intArr):
			continue
		for index2, value2 in enumerate(intArr[index1 + 1:]):
			if index2 + 1 > len(intArr):
				continue
			for value3 in intArr[index2 + 2:]:
				if value1 + value2 + value3 == 2020:
					intProd = value1 * value2 * value3
	print(intProd)

def main():
	part1()
	part2()
main()