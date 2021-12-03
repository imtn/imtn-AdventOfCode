# Returns the integer number of Adjacent Seats that are occupied
def countOccupiedAdjacentSeats(row, col, seats):
	count = 0
	for currRow in range(row-1, row+2):
		for currCol in range(col-1, col+2):
			if currRow in range(len(seats)) and currCol in range(len(seats[0])) and (currRow != row or currCol != col) and seats[currRow][currCol] == '#':
				count += 1
	return count

# Returns the integer number of Adjacent Seats that are occupied
def countOccupiedVisiblyAdjacentSeats(row, col, seats):
	count = 0
	
	# manually check each direction
	# northwest
	currRow = row - 1
	currCol = col - 1
	while currRow in range(len(seats)) and currCol in range(len(seats[0])):
		if seats[currRow][currCol] == '#':
			count += 1
			break
		elif seats[currRow][currCol] == 'L':
			break
		else:
			currRow -= 1
			currCol -= 1

	# north
	currRow = row - 1
	currCol = col
	while currRow in range(len(seats)) and currCol in range(len(seats[0])):
		if seats[currRow][currCol] == '#':
			count += 1
			break
		elif seats[currRow][currCol] == 'L':
			break
		else:
			currRow -= 1

	# northeast
	currRow = row - 1
	currCol = col + 1
	while currRow in range(len(seats)) and currCol in range(len(seats[0])):
		if seats[currRow][currCol] == '#':
			count += 1
			break
		elif seats[currRow][currCol] == 'L':
			break
		else:
			currRow -= 1
			currCol += 1

	# west
	currRow = row
	currCol = col - 1
	while currRow in range(len(seats)) and currCol in range(len(seats[0])):
		if seats[currRow][currCol] == '#':
			count += 1
			break
		elif seats[currRow][currCol] == 'L':
			break
		else:
			currCol -= 1

	# east
	currRow = row
	currCol = col + 1
	while currRow in range(len(seats)) and currCol in range(len(seats[0])):
		if seats[currRow][currCol] == '#':
			count += 1
			break
		elif seats[currRow][currCol] == 'L':
			break
		else:
			currCol += 1

	# southwest
	currRow = row + 1
	currCol = col - 1
	while currRow in range(len(seats)) and currCol in range(len(seats[0])):
		if seats[currRow][currCol] == '#':
			count += 1
			break
		elif seats[currRow][currCol] == 'L':
			break
		else:
			currRow += 1
			currCol -= 1

	# south
	currRow = row + 1
	currCol = col
	while currRow in range(len(seats)) and currCol in range(len(seats[0])):
		if seats[currRow][currCol] == '#':
			count += 1
			break
		elif seats[currRow][currCol] == 'L':
			break
		else:
			currRow += 1

	# southeast
	currRow = row + 1
	currCol = col + 1
	while currRow in range(len(seats)) and currCol in range(len(seats[0])):
		if seats[currRow][currCol] == '#':
			count += 1
			break
		elif seats[currRow][currCol] == 'L':
			break
		else:
			currRow += 1
			currCol += 1

	return count

# Processes the seats once according to the rules of the puzzle
# 	If seat is empty and there are no adjacent occupied seats, the seat becomes occupied
# 	If seat is occupied and four or more adjacent seats are occupied, the seat becomes occupied
# 	Seats otherwise and floors do not chance.
# Returns a tuple of (original seat list passed in, new processed seat list, seatsChanged)
def oldProcessOnce(seats):
	seatsChanged = 0
	previousSeats = [x[:] for x in seats]
	for rowI in range(len(previousSeats)):
		for colI in range(len(previousSeats[rowI])):
			adjOccCount = countOccupiedAdjacentSeats(rowI, colI, previousSeats)
			if previousSeats[rowI][colI] == 'L' and adjOccCount == 0:
				seats[rowI][colI] = '#'
				seatsChanged += 1
			elif previousSeats[rowI][colI] == '#' and adjOccCount >= 4:
				seats[rowI][colI] = 'L'
				seatsChanged += 1
			else:
				seats[rowI][colI] = previousSeats[rowI][colI]
	return (previousSeats, seats, seatsChanged)

# Processes the seats once according to the rules of the puzzle
# 	If seat is empty and there are no adjacent occupied seats, the seat becomes occupied
# 	If seat is occupied and four or more adjacent seats are occupied, the seat becomes occupied
# 	Seats otherwise and floors do not chance.
# Returns a tuple of (original seat list passed in, new processed seat list, seatsChanged)
def newProcessOnce(seats):
	seatsChanged = 0
	previousSeats = [x[:] for x in seats]
	for rowI in range(len(previousSeats)):
		for colI in range(len(previousSeats[rowI])):
			adjOccCount = countOccupiedVisiblyAdjacentSeats(rowI, colI, previousSeats)
			if previousSeats[rowI][colI] == 'L' and adjOccCount == 0:
				seats[rowI][colI] = '#'
				seatsChanged += 1
			elif previousSeats[rowI][colI] == '#' and adjOccCount >= 5:
				seats[rowI][colI] = 'L'
				seatsChanged += 1
			else:
				seats[rowI][colI] = previousSeats[rowI][colI]
	return (previousSeats, seats, seatsChanged)

def part1():
	# seats is a nested list of lists, where the outer list holds rows of seats, and the inner list holds a char that represents a seat or floor
	# to get a seat, do seats[row][col]
	seats = []
	with open('input.txt') as f:
		for line in f:
			seats.append([])
			for char in line.strip():
				seats[-1].append(char)

	while(True):
		previousSeats, seats, seatsChanged = oldProcessOnce(seats)
		if seatsChanged == 0:
			seatCount = 0
			for row in seats:
				for seat in row:
					if seat == '#':
						seatCount += 1
			print(seatCount)
			return
	# Be patient, part 1 takes up to a dozen seconds to run

def part2():
	# seats is a nested list of lists, where the outer list holds rows of seats, and the inner list holds a char that represents a seat or floor
	# to get a seat, do seats[row][col]
	seats = []
	with open('input.txt') as f:
		for line in f:
			seats.append([])
			for char in line.strip():
				seats[-1].append(char)

	while(True):
		previousSeats, seats, seatsChanged = newProcessOnce(seats)
		if seatsChanged == 0:
			seatCount = 0
			for row in seats:
				for seat in row:
					if seat == '#':
						seatCount += 1
			print(seatCount)
			return
	# Be patient, part 2 takes up to a dozen seconds to run

def main():
	# part1()
	part2()
main()