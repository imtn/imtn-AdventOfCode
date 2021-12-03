def part1():
	tiles = dict() # tiles is a dictionary mapping an integer (tile number) to a list of strings, which represents a tile
	tileNum = -1

	with open('input.txt') as f:
		for line in f:
			if line[0] == 'T':
				tileNum = int(line.strip().split(' ')[1][:4])
				tiles[tileNum] = []
			elif line[0] == '.' or line[0] == '#':
				tiles[tileNum].append(line.strip())

	print(tiles)


def part2():
	pass

def main():
	part1()
	part2()
main()