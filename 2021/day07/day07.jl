function findFuelCost(crabArray, hPos)
	fuelCost = 0
	for i in crabArray
		fuelCost += abs(i - hPos)
	end
	return fuelCost
end

function findNewFuelCost(crabArray, hPos)
	fuelCost = 0
	for i in crabArray
		distance = abs(i - hPos)
		fuelCost += (distance * (distance + 1))/2
	end
	return fuelCost
end

function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	crabArray = sort(parse.(Int64, split(input[1], ",")))
	minPosition = (-1, 999999999999) # Tuple (hPos, fuelCost)

	# probably just brute force
	for i in crabArray[1]:crabArray[end]
		fuelCost = findFuelCost(crabArray, i)
		if fuelCost < minPosition[2]
			minPosition = (i, fuelCost)
		end
	end

	@show minPosition
end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	crabArray = sort(parse.(Int64, split(input[1], ",")))
	minPosition = (-1, 999999999999) # Tuple (hPos, fuelCost)

	# probably just brute force
	for i in crabArray[1]:crabArray[end]
		fuelCost = findNewFuelCost(crabArray, i)
		if fuelCost < minPosition[2]
			minPosition = (i, fuelCost)
		end
	end

	@show minPosition
	println(trunc(Int, minPosition[2]))
end

part2("input.txt")