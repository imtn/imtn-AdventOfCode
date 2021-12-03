# This method takes in several values and returns adjusted values based on the input
#	action is a letter representing the action to take
# 	val is an integer representing the magnitude to perform the action
# 	facing is an integers representing the current direction we're facing
# 	xCor is the X Coordinate of the ship.
# 	yCor is the Y Coordinate of the ship.
# What each action does is listed below:
#	Action N means to move north by the given value.
#	Action S means to move south by the given value.
#	Action E means to move east by the given value.
#	Action W means to move west by the given value.
#	Action L means to turn left the given number of degrees.
#	Action R means to turn right the given number of degrees.
#	Action F means to move forward by the given value in the direction the ship is currently facing.
def oldMove(action, val, facing, xCor, yCor):
	if action == 'N':
		return (facing, xCor, yCor + val)
	elif action == 'S':
		return (facing, xCor, yCor - val)
	elif action == 'E':
		return (facing, xCor + val, yCor)
	elif action == 'W':
		return (facing, xCor - val, yCor)
	elif action == 'L':
		return ((facing - int(val/90))%4, xCor, yCor)
	elif action == 'R':
		return ((facing + int(val/90))%4, xCor, yCor)
	elif action == 'F':
		if facing == 0: # East
			return (facing, xCor + val, yCor)
		elif facing == 1: # South
			return (facing, xCor, yCor - val)
		elif facing == 2: # West
			return (facing, xCor - val, yCor)
		elif facing == 3: # North
			return (facing, xCor, yCor + val)
		else:
			print("Bad facing in move('F'):" + str(facing))
			quit()
	else:
		print("Bad action in move(): " + action)
		quit()


# This method takes in several values and returns adjusted values based on the input
#	action is a letter representing the action to take
# 	val is an integer representing the magnitude to perform the action
# 	sX and sY are the X and Y coordinates of the ship
# 	wX and wY are the X and Y coordinates of the waypoint
# What each action does is listed below:
#	Action N means to move the waypoint north by the given value.
#	Action S means to move the waypoint south by the given value.
#	Action E means to move the waypoint east by the given value.
#	Action W means to move the waypoint west by the given value.
#	Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
#	Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
#	Action F means to move forward to the waypoint a number of times equal to the given value.
def newMove(action, val, sX, sY, wX, wY):
	if action == 'N':
		return (sX, sY, wX, wY + val)
	elif action == 'S':
		return (sX, sY, wX, wY - val)
	elif action == 'E':
		return (sX, sY, wX + val, wY)
	elif action == 'W':
		return (sX, sY, wX - val, wY)
	elif action == 'L':
		num = int(val / 90)
		for _ in range(num):
			oldWX = wX
			oldWY = wY
			wX = oldWY * -1
			wY = oldWX
		return (sX, sY, wX, wY)
	elif action == 'R':
		num = int(val / 90)
		for _ in range(num):
			oldWX = wX
			oldWY = wY
			wX = oldWY
			wY = oldWX * -1
		return (sX, sY, wX, wY)
	elif action == 'F':
		sX += (wX * val)
		sY += (wY * val)
		return (sX, sY, wX, wY)
	else:
		print("Bad action in move(): " + action)
		quit()

def part1():
	# Facing direction represented by integers as follows:
	# 0 - East
	# 1 - South
	# 2 - West
	# 3 - North
	# Turn Right is Plus, Turn Left is Minus
	facing = 0
	xCor = 0
	yCor = 0

	with open('input.txt') as f:
		for line in f:
			action = line[0]
			val = int(line.strip()[1:])
			facing, xCor, yCor = oldMove(action, val, facing, xCor, yCor)
			# print('fXY: ' + str(facing) + ' ' + str(xCor) + ' ' + str(yCor))
			# print('aV: ' + action + ' ' + str(val))
			# input()

	print("Part 1 Manhattan distance:")
	print(str(abs(xCor) + abs(yCor)))


def part2():
	# sX and sY are the X and Y coordinates of the ship
	# wX and wY are the X and Y coordinates of the waypoint
	sX = 0
	sY = 0
	wX = 10
	wY = 1

	with open('input.txt') as f:
		for line in f:
			action = line[0]
			val = int(line.strip()[1:])
			sX, sY, wX, wY = newMove(action, val, sX, sY, wX, wY)
			# print('sXY: ' + str(sX) + ' ' + str(sY) + ' | wXY: ' + str(wX) + ' ' + str(wY))
			# print('aV: ' + action + ' ' + str(val))
			# input()

	print("Part 2 Manhattan distance:")
	print(str(abs(sX) + abs(sY)))

def main():
	part1()
	part2()
main()