function passOneStep!(octoArray)
	# first, increase all energy levels by 1. if any have level equal 10, add to needToFlash queue
	# then, while the queue has octopi,
	# 	pop
	# 	add octopus to flashed
	#	increment flashCount
	# 	increment neighbors
	#		if any neighbors are 10 and not in flashed, then add them to queue
	# after queue is processed, set all octopi in flashed to 0 energy

	flashed = Set{Tuple}() # a set of (x, y) coordinate tuples for all the octopi in this step that have flashed
	needToFlash = [] # queue of (x, y) coordinate tuples that we need to process flashing. add with push!, remove with popfirst!
	flashCount = 0

	for row in 1:10, col in 1:10
		octoArray[row, col] += 1
		if octoArray[row, col] == 10
			push!(needToFlash, (row, col))
		end
	end

	while !isempty(needToFlash)
		cRow, cCol = popfirst!(needToFlash)
		push!(flashed, (cRow, cCol))
		flashCount += 1

		for x in cRow-1:cRow+1, y in cCol-1:cCol+1
			if 1 <= x <= length(octoArray[:, 1]) && 1 <= y <= length(octoArray[1, :])
				octoArray[x, y] += 1
				if octoArray[x, y] == 10 && !in((x, y), flashed)
					push!(needToFlash, (x, y))
				end
			end
		end
	end

	for octTup in flashed
		row, col = octTup
		octoArray[row, col] = 0
	end

	return flashCount
end

function passOneStepPartTwo!(octoArray)
	# first, increase all energy levels by 1. if any have level equal 10, add to needToFlash queue
	# then, while the queue has octopi,
	# 	pop
	# 	add octopus to flashed
	#	increment flashCount
	# 	increment neighbors
	#		if any neighbors are 10 and not in flashed, then add them to queue
	# after queue is processed, set all octopi in flashed to 0 energy
	# returns True if all octopi flashed, else False

	flashed = Set{Tuple}() # a set of (x, y) coordinate tuples for all the octopi in this step that have flashed
	needToFlash = [] # queue of (x, y) coordinate tuples that we need to process flashing. add with push!, remove with popfirst!
	flashCount = 0

	for row in 1:10, col in 1:10
		octoArray[row, col] += 1
		if octoArray[row, col] == 10
			push!(needToFlash, (row, col))
		end
	end

	while !isempty(needToFlash)
		cRow, cCol = popfirst!(needToFlash)
		push!(flashed, (cRow, cCol))
		flashCount += 1

		for x in cRow-1:cRow+1, y in cCol-1:cCol+1
			if 1 <= x <= length(octoArray[:, 1]) && 1 <= y <= length(octoArray[1, :])
				octoArray[x, y] += 1
				if octoArray[x, y] == 10 && !in((x, y), flashed)
					push!(needToFlash, (x, y))
				end
			end
		end
	end

	for octTup in flashed
		row, col = octTup
		octoArray[row, col] = 0
	end

	return length(flashed) == length(octoArray)
end

function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	octopuses = Array{Int64}(undef, 10, 10)
	for i in 1:10
		octopuses[i, :] = parse.(Int64, collect(input[i]))
	end
	
	flashCount = 0
	for i in 1:100
		flashCount += passOneStep!(octopuses)
	end
	println(flashCount)
end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	octopuses = Array{Int64}(undef, 10, 10)
	for i in 1:10
		octopuses[i, :] = parse.(Int64, collect(input[i]))
	end
	
	for i in 1:500
		if(passOneStepPartTwo!(octopuses))
			println("Passed on step $i !")
			break
		end
	end
end

part2("input.txt")