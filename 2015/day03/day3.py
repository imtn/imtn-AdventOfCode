def part1():
	directions = ''
	with open('input.txt') as f:
		for line in f:
			directions = line.strip()

	x = 0
	y = 0
	visitedHouseSet = set() # set of tuples which represent x y coords of houses visited
	visitedHouseSet.add((0,0))
	for d in directions:
		if d == '^':
			y += 1
		elif d == 'v':
			y -= 1
		elif d == '<':
			x -= 1
		elif d == '>':
			x += 1
		else:
			print("Weird d: " + str(d))
			quit()
		visitedHouseSet.add((x,y))
	print(len(visitedHouseSet))

def part2():
	directions = ''
	with open('input.txt') as f:
		for line in f:
			directions = line.strip()

	x = 0
	y = 0
	visitedHouseSet = set() # set of tuples which represent x y coords of houses visited
	visitedHouseSet.add((0,0))

	for d in directions[::2]:
		if d == '^':
			y += 1
		elif d == 'v':
			y -= 1
		elif d == '<':
			x -= 1
		elif d == '>':
			x += 1
		else:
			print("Weird d: " + str(d))
			quit()
		visitedHouseSet.add((x,y))

	x = 0
	y = 0
	for d in directions[1::2]:
		if d == '^':
			y += 1
		elif d == 'v':
			y -= 1
		elif d == '<':
			x -= 1
		elif d == '>':
			x += 1
		else:
			print("Weird d: " + str(d))
			quit()
		visitedHouseSet.add((x,y))

	print(len(visitedHouseSet))

def main():
	part1()
	part2()
main()