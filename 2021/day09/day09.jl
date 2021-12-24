function isPointInBasinArr(point, basinsArr)
	for basin in basinsArr
		if point in basin
			return true
		end
	end
	return false
end

function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	width = length(input[1])
	height = length(input)

	floor = Array{Int64}(undef, length(input), length(input[1]))

	for i in 1:length(input)
		floor[i, :] = parse.(Int64, collect(input[i]))
	end
	
	lowPointSum = 0
	#loop through each point and determine if it's a low point or not.
	for row in 1:height, col in 1:width
		currFloor = floor[row, col]
		# north
		if currFloor >= get(floor, (row-1, col), 10)
			continue
		end
		# south
		if currFloor >= get(floor, (row+1, col), 10)
			continue
		end
		# east
		if currFloor >= get(floor, (row, col+1), 10)
			continue
		end
		# west
		if currFloor >= get(floor, (row, col-1), 10)
			continue
		end

		# confirmed low point, calculate score
		lowPointSum += currFloor + 1
	end
	println("Sum of risk levels is $lowPointSum")
end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	width = length(input[1])
	height = length(input)

	floor = Array{Int64}(undef, length(input), length(input[1]))

	for i in 1:length(input)
		floor[i, :] = parse.(Int64, collect(input[i]))
	end

	lpSet = Set{Tuple}() # A set of (x, y) tuples representing the low points we find.
	
	#loop through each point and determine if it's a low point or not.
	for row in 1:height, col in 1:width
		currFloor = floor[row, col]
		# north
		if currFloor >= get(floor, (row-1, col), 10)
			continue
		end
		# south
		if currFloor >= get(floor, (row+1, col), 10)
			continue
		end
		# east
		if currFloor >= get(floor, (row, col+1), 10)
			continue
		end
		# west
		if currFloor >= get(floor, (row, col-1), 10)
			continue
		end

		# confirmed low point
		push!(lpSet, (row, col))
	end

	# Basin is set of coordinates represented by tuples?
	# Find basin starting with low point. Use a queue to add neighbors unless it's a one
	# When starting a new basin, check if low point is already in another basin

	basinsArr = Set{Tuple}[] # An array of all basins. Each basin is a set of (x, y) tuple coordinates that represent the points in that basin

	# for each low point, if it's not already in an existing basin, build a basin for it by creating its basin set and adding it to basin array.
	for lowPoint in lpSet
		if !isPointInBasinArr(lowPoint, basinsArr)

			basin = Set{Tuple}()
			pointQueue = Tuple[(lowPoint)]

			#=
			while queue has points,
			add the point to the basin
			then add all neighbors that are not 9, are inbounds, and not already in the basin to the queue

			Queue: push to back, pop from front
			=#
			while !isempty(pointQueue)
				thisPoint = popfirst!(pointQueue)
				
				push!(basin, thisPoint)

				north = (thisPoint[1] - 1, thisPoint[2])
				if north[1] >= 1 && !in(north, basin) && floor[north[1], north[2]] != 9
					push!(pointQueue, north)
				end

				south = (thisPoint[1] + 1, thisPoint[2])
				if south[1] <= height && !in(south, basin) && floor[south[1], south[2]] != 9
					push!(pointQueue, south)
				end

				east = (thisPoint[1], thisPoint[2] + 1)
				if east[2] <= width && !in(east, basin) && floor[east[1], east[2]] != 9
					push!(pointQueue, east)
				end

				west = (thisPoint[1], thisPoint[2] - 1)
				if west[2] >= 1 && !in(west, basin) && floor[west[1], west[2]] != 9
					push!(pointQueue, west)
				end
			end

			push!(basinsArr, basin)
		end
	end

	# basinsArr created, now sort it
	# and find the product of the sizes of the 3 largest basins
	sort!(basinsArr, by = x->length(x))

	product = length(basinsArr[end]) * length(basinsArr[end - 1]) * length(basinsArr[end - 2])
	println("Product is $product")
end

part2("input.txt")