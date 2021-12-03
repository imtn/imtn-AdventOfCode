# modifies the lights dict according to the instruction
# lights is a dictionary maaping (x,y) coordinates to a boolean
# instruction is a string representing the instruction
# We don't return anything because we edit the lights dict in-place
def modifyLights(lights, instruction):
	iSplit = instruction.split(' ')
	iEnd = iSplit[-1].split(',')
	iStart = iSplit[-3].split(',')
	iCommand = iSplit[-4]

	x1 = int(iStart[0])
	y1 = int(iStart[1])
	x2 = int(iEnd[0])
	y2 = int(iEnd[1])
	
	if iCommand == 'on':
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				lights[(x,y)] = True
	elif iCommand == 'off':
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				lights[(x,y)] = False
	elif iCommand == 'toggle':
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				lights[(x,y)] = True if lights[(x,y)] == False else False
	else:
		print("Bad iCommand: " + iCommand)
		quit()

# modifies the lights dict according to the instruction
# lights is a dictionary maaping (x,y) coordinates to an integer
# instruction is a string representing the instruction
# We don't return anything because we edit the lights dict in-place
def newModifyLights(lights, instruction):
	iSplit = instruction.split(' ')
	iEnd = iSplit[-1].split(',')
	iStart = iSplit[-3].split(',')
	iCommand = iSplit[-4]

	x1 = int(iStart[0])
	y1 = int(iStart[1])
	x2 = int(iEnd[0])
	y2 = int(iEnd[1])
	
	if iCommand == 'on':
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				lights[(x,y)] += 1
	elif iCommand == 'off':
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				lights[(x,y)] = max(0, lights[(x,y)] - 1)
	elif iCommand == 'toggle':
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				lights[(x,y)] += 2
	else:
		print("Bad iCommand: " + iCommand)
		quit()

def part1():
	lights = dict() # lights is a dictionary mapping from a tuple (x, y) coords to a boolean about whether or not the light is on
	for x in range(1000):
		for y in range(1000):
			lights[(x,y)] = False

	with open('input.txt') as f:
		for line in f:
			modifyLights(lights, line.strip())

	litCount = 0
	for val in lights.values():
		if val:
			litCount += 1
	print(litCount)

def part2():
	lights = dict() # lights is a dictionary mapping from a tuple (x, y) coords to an integer representing the brightness
	for x in range(1000):
		for y in range(1000):
			lights[(x,y)] = 0

	with open('input.txt') as f:
		for line in f:
			newModifyLights(lights, line.strip())

	bCount = 0
	for val in lights.values():
		bCount += val
	print(bCount)

part1()
part2()