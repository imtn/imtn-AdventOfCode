def part1():
	grid = []
	numOfTrees = 0
	xPos = 0
	with open('input.txt') as f:
		for line in f:
			grid.append(line)
	gridWidth = len(grid[0].strip())

	for line in grid:
		if line[xPos % gridWidth] == '#':
			numOfTrees += 1
		xPos += 3

	print(numOfTrees)

def part2():
	# Check these slopes:
	# 0 - Right 1, down 1.
	# 1 - Right 3, down 1. (This is the slope you already checked.)
	# 2 - Right 5, down 1.
	# 3 - Right 7, down 1.
	# 4 - Right 1, down 2.

	grid = []
	numOfTrees = [0,0,0,0,0] # the above slopes, one by one
	xPos = [0,0,0,0,0] # XPos for each of the above
	yPos = 0
	with open('input.txt') as f:
		for line in f:
			grid.append(line)
	gridWidth = len(grid[0].strip())

	for line in grid:
		if line[xPos[0] % gridWidth] == '#':
			numOfTrees[0] += 1
		xPos[0] += 1
		if line[xPos[1] % gridWidth] == '#':
			numOfTrees[1] += 1
		xPos[1] += 3
		if line[xPos[2] % gridWidth] == '#':
			numOfTrees[2] += 1
		xPos[2] += 5
		if line[xPos[3] % gridWidth] == '#':
			numOfTrees[3] += 1
		xPos[3] += 7
		if yPos % 2 == 0: 
			if line[xPos[4] % gridWidth] == '#':
				numOfTrees[4] += 1
			xPos[4] += 1
		yPos += 1
		# print(xPos)
		# print(yPos)

	print(numOfTrees)
	product = 1
	for num in numOfTrees:
		product *= num
	print(product)

def main():
	part1()
	part2()
main()