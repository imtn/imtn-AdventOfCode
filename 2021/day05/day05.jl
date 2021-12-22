function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	inputCoords = split.(input, " ")
	ventGrid = Dict{Tuple{Int64, Int64},Int64}() # This dictionary maps a coordinates (represented as (x, y) tuples) to an integer representing how many vents there are there.

	# populate ventGrid
	for line in inputCoords
		fromCoord = (parse(Int, split(line[1], ",")[1]), parse(Int, split(line[1], ",")[2]))
		toCoord = (parse(Int, split(line[3], ",")[1]), parse(Int, split(line[3], ",")[2]))

		if fromCoord[1] == toCoord[1]
			# println("1: Adding from $fromCoord to $toCoord")
			loopArray = fromCoord[2] <= toCoord[2] ? collect(fromCoord[2]:toCoord[2]) : collect(toCoord[2]:fromCoord[2])
			for i in loopArray
				ventGrid[(fromCoord[1], i)] = get(ventGrid, (fromCoord[1], i), 0) + 1
			end
		elseif fromCoord[2] == toCoord[2]
			# println("2: Adding from $fromCoord to $toCoord")
			loopArray = fromCoord[1] <= toCoord[1] ? collect(fromCoord[1]:toCoord[1]) : collect(toCoord[1]:fromCoord[1])
			for i in loopArray
				ventGrid[(i, fromCoord[2])] = get(ventGrid, (i, fromCoord[2]), 0) + 1
			end
		end
	end

	runningsum = 0
	for i in values(ventGrid)
		if i >= 2
			runningsum += 1
		end
	end
	println(runningsum)
end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	inputCoords = split.(input, " ")
	ventGrid = Dict{Tuple{Int64, Int64},Int64}() # This dictionary maps a coordinates (represented as (x, y) tuples) to an integer representing how many vents there are there.

	# populate ventGrid
	for line in inputCoords
		fromCoord = (parse(Int, split(line[1], ",")[1]), parse(Int, split(line[1], ",")[2]))
		toCoord = (parse(Int, split(line[3], ",")[1]), parse(Int, split(line[3], ",")[2]))

		if fromCoord[1] == toCoord[1]
			# println("1: Adding from $fromCoord to $toCoord")
			loopArray = fromCoord[2] <= toCoord[2] ? collect(fromCoord[2]:toCoord[2]) : collect(toCoord[2]:fromCoord[2])
			for i in loopArray
				ventGrid[(fromCoord[1], i)] = get(ventGrid, (fromCoord[1], i), 0) + 1
			end
		elseif fromCoord[2] == toCoord[2]
			# println("2: Adding from $fromCoord to $toCoord")
			loopArray = fromCoord[1] <= toCoord[1] ? collect(fromCoord[1]:toCoord[1]) : collect(toCoord[1]:fromCoord[1])
			for i in loopArray
				ventGrid[(i, fromCoord[2])] = get(ventGrid, (i, fromCoord[2]), 0) + 1
			end
		else
			# println("3: Adding from $fromCoord to $toCoord")

			# Process Diagonals
			xCoord, yCoord = fromCoord

			while ((xCoord, yCoord) != toCoord)
				ventGrid[(xCoord, yCoord)] = get(ventGrid, (xCoord, yCoord), 0) + 1
				xCoord = xCoord < toCoord[1] ? xCoord + 1 : xCoord - 1
				yCoord = yCoord < toCoord[2] ? yCoord + 1 : yCoord - 1
			end
			ventGrid[(xCoord, yCoord)] = get(ventGrid, (xCoord, yCoord), 0) + 1
		end
	end

	runningsum = 0
	for i in values(ventGrid)
		if i >= 2
			runningsum += 1
		end
	end
	println(runningsum)
end

part2("input.txt")