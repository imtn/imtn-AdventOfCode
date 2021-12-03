def printCube(cube):
	for z in range(cube['zMin'], cube['zMax'] + 1):
		print('\n')
		print('z = ' + str(z))
		for y in range(cube['yMin'], cube['yMax'] + 1):
			for x in range(cube['xMin'], cube['xMax'] + 1):
				if (x,y,z) not in cube:
					print('.', end = '')
				else:
					print(cube[(x,y,z)], end = '')
			print('\n')

# Returns a count of how many active neighbors the passed in (x,y,z) coordinate has
def countActiveNeighbors(cube, x, y, z):
	count = 0
	for zz in range(z - 1, z + 2):
		for yy in range(y - 1, y + 2):
			for xx in range(x - 1, x + 2):
				if (xx, yy, zz) in cube and (xx,yy,zz) != (x,y,z):
					count += 1
	return count

# Returns a count of how many active neighbors the passed in (x,y,z,w) coordinate has
def newCountActiveNeighbors(cube, x, y, z, w):
	count = 0
	for ww in range(w - 1, w + 2):
		for zz in range(z - 1, z + 2):
			for yy in range(y - 1, y + 2):
				for xx in range(x - 1, x + 2):
					if (xx, yy, zz, ww) in cube and (xx,yy,zz,ww) != (x,y,z,w):
						count += 1

	return count


# processes the cube according to the rules in day 17
# If cube is active and 2 or 3 neighbors are active, cube stays active, otherwise becomes inactive
# If cube is inactive and 3 neighbors are active, cube becomes active, otherwise stays inactive
# Returns a new cube
def processOnce(cube):
	newCube = dict()
	newCube['xMin'] = None
	newCube['xMax'] = None
	newCube['yMin'] = None
	newCube['yMax'] = None
	newCube['zMin'] = None
	newCube['zMax'] = None

	for z in range(cube['zMin'] - 1, cube['zMax'] + 2):
		for y in range(cube['yMin'] - 1, cube['yMax'] + 2):
			for x in range(cube['xMin'] - 1, cube['xMax'] + 2):
				nCount = countActiveNeighbors(cube, x, y, z)
				# print("Coordinates (" + str(x) + ',' + str(y) + ',' + str(z) + ') | nCount == ' + str(nCount))
				if (x,y,z) in cube:
					if nCount == 2 or nCount == 3:
						newCube[(x,y,z)] = '#'

						newCube['xMin'] = x if newCube['xMin'] == None or x < newCube['xMin'] else newCube['xMin']
						newCube['xMax'] = x if newCube['xMax'] == None or x > newCube['xMax'] else newCube['xMax']
						newCube['yMin'] = y if newCube['yMin'] == None or y < newCube['yMin'] else newCube['yMin']
						newCube['yMax'] = y if newCube['yMax'] == None or y > newCube['yMax'] else newCube['yMax']
						newCube['zMin'] = z if newCube['zMin'] == None or z < newCube['zMin'] else newCube['zMin']
						newCube['zMax'] = z if newCube['zMax'] == None or z > newCube['zMax'] else newCube['zMax']

				elif (x,y,z) not in cube:
					if nCount == 3:
						newCube[(x,y,z)] = '#'

						newCube['xMin'] = x if newCube['xMin'] == None or x < newCube['xMin'] else newCube['xMin']
						newCube['xMax'] = x if newCube['xMax'] == None or x > newCube['xMax'] else newCube['xMax']
						newCube['yMin'] = y if newCube['yMin'] == None or y < newCube['yMin'] else newCube['yMin']
						newCube['yMax'] = y if newCube['yMax'] == None or y > newCube['yMax'] else newCube['yMax']
						newCube['zMin'] = z if newCube['zMin'] == None or z < newCube['zMin'] else newCube['zMin']
						newCube['zMax'] = z if newCube['zMax'] == None or z > newCube['zMax'] else newCube['zMax']

				else:
					print("Weird logic when processing cube")
					quit()
	return newCube

# processes the (hyper-)cube according to the rules in day 17
# If cube is active and 2 or 3 neighbors are active, cube stays active, otherwise becomes inactive
# If cube is inactive and 3 neighbors are active, cube becomes active, otherwise stays inactive
# Returns a new cube
def newProcessOnce(cube):
	newCube = dict()
	newCube['xMin'] = None
	newCube['xMax'] = None
	newCube['yMin'] = None
	newCube['yMax'] = None
	newCube['zMin'] = None
	newCube['zMax'] = None
	newCube['wMin'] = None
	newCube['wMax'] = None

	for w in range(cube['wMin'] - 1, cube['wMax'] + 2):
		for z in range(cube['zMin'] - 1, cube['zMax'] + 2):
			for y in range(cube['yMin'] - 1, cube['yMax'] + 2):
				for x in range(cube['xMin'] - 1, cube['xMax'] + 2):
					nCount = newCountActiveNeighbors(cube, x, y, z, w)
					# print("Coordinates (" + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(w) + ') | nCount == ' + str(nCount))
					if (x,y,z,w) in cube:
						if nCount == 2 or nCount == 3:
							newCube[(x,y,z,w)] = '#'

							newCube['xMin'] = x if newCube['xMin'] == None or x < newCube['xMin'] else newCube['xMin']
							newCube['xMax'] = x if newCube['xMax'] == None or x > newCube['xMax'] else newCube['xMax']
							newCube['yMin'] = y if newCube['yMin'] == None or y < newCube['yMin'] else newCube['yMin']
							newCube['yMax'] = y if newCube['yMax'] == None or y > newCube['yMax'] else newCube['yMax']
							newCube['zMin'] = z if newCube['zMin'] == None or z < newCube['zMin'] else newCube['zMin']
							newCube['zMax'] = z if newCube['zMax'] == None or z > newCube['zMax'] else newCube['zMax']
							newCube['wMin'] = w if newCube['wMin'] == None or w < newCube['wMin'] else newCube['wMin']
							newCube['wMax'] = w if newCube['wMax'] == None or w > newCube['wMax'] else newCube['wMax']

					elif (x,y,z,w) not in cube:
						if nCount == 3:
							newCube[(x,y,z,w)] = '#'

							newCube['xMin'] = x if newCube['xMin'] == None or x < newCube['xMin'] else newCube['xMin']
							newCube['xMax'] = x if newCube['xMax'] == None or x > newCube['xMax'] else newCube['xMax']
							newCube['yMin'] = y if newCube['yMin'] == None or y < newCube['yMin'] else newCube['yMin']
							newCube['yMax'] = y if newCube['yMax'] == None or y > newCube['yMax'] else newCube['yMax']
							newCube['zMin'] = z if newCube['zMin'] == None or z < newCube['zMin'] else newCube['zMin']
							newCube['zMax'] = z if newCube['zMax'] == None or z > newCube['zMax'] else newCube['zMax']
							newCube['wMin'] = w if newCube['wMin'] == None or w < newCube['wMin'] else newCube['wMin']
							newCube['wMax'] = w if newCube['wMax'] == None or w > newCube['wMax'] else newCube['wMax']

					else:
						print("Weird logic when processing hypercube")
						quit()
	return newCube

def part1():
	# inputSquare is the input, it is a list of lines of # and .
	# top left unit is (0,0,0)
	inputSquare = []
	# cube is a dictionary mapping (x,y,z) tuple to active cubes (#). Inactive cubes (.) are not recorded.
	cube = dict()
	with open('input.txt') as f:
		for line in f:
			inputSquare.append(line.strip())

	# populate cube with inputSquare
	for iLine, line in enumerate(inputSquare): # y coordinate
		for iChar, char in enumerate(line): # x coordinate
			if char == '#':
				cube[(iChar,iLine,0)] = char
	cube['xMin'] = 0
	cube['xMax'] = len(inputSquare[0]) - 1
	cube['yMin'] = 0
	cube['yMax'] = len(inputSquare) - 1
	cube['zMin'] = 0
	cube['zMax'] = 0

	cube = processOnce(cube)
	cube = processOnce(cube)
	cube = processOnce(cube)
	cube = processOnce(cube)
	cube = processOnce(cube)
	cube = processOnce(cube)
	print(len(cube) - 6)
	# printCube(cube)

def part2():
	# inputSquare is the input, it is a list of lines of # and .
	# top left unit is (0,0,0,0)
	inputSquare = []
	# cube is a dictionary mapping (x,y,z,w) tuple to active cubes (#). Inactive cubes (.) are not recorded.
	cube = dict()
	with open('input.txt') as f:
		for line in f:
			inputSquare.append(line.strip())

	# populate cube with inputSquare
	for iLine, line in enumerate(inputSquare): # y coordinate
		for iChar, char in enumerate(line): # x coordinate
			if char == '#':
				cube[(iChar,iLine,0,0)] = char
	cube['xMin'] = 0
	cube['xMax'] = len(inputSquare[0]) - 1
	cube['yMin'] = 0
	cube['yMax'] = len(inputSquare) - 1
	cube['zMin'] = 0
	cube['zMax'] = 0
	cube['wMin'] = 0
	cube['wMax'] = 0

	cube = newProcessOnce(cube)
	cube = newProcessOnce(cube)
	cube = newProcessOnce(cube)
	cube = newProcessOnce(cube)
	cube = newProcessOnce(cube)
	cube = newProcessOnce(cube)
	print(len(cube) - 8)
	# printCube(cube)

def main():
	part1()
	part2()
main()