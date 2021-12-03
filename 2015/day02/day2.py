def calcSurfaceAreaPlusSmallestSide(length, width, height):
	side1 = length*width
	side2 = width*height
	side3 = height*length

	return 2*side1 + 2*side2 + 2*side3 + min(side1, side2, side3)

def part1():
	surfaceAreaSum = 0
	with open('input.txt') as f:
		for line in f:
			lineSplit = line.strip().split('x')
			surfaceAreaSum += calcSurfaceAreaPlusSmallestSide(int(lineSplit[0]), int(lineSplit[1]), int(lineSplit[2]))
	print(surfaceAreaSum)

def part2():
	ribbonLength = 0
	with open('input.txt') as f:
		for line in f:
			lineSplit = line.strip().split('x')
			length = int(lineSplit[0])
			width = int(lineSplit[1])
			height = int(lineSplit[2])
			sortedSideLengths = sorted([length, width, height])
			ribbonLength += 2*sortedSideLengths[0] + 2*sortedSideLengths[1] + length * width * height


	print(ribbonLength)

def main():
	part1()
	part2()
main()