function has2SmallCaves(path::Array{String})
	sortedLowercase = sort!(filter(x->all(islowercase, x), path))
	returnThis = length(sortedLowercase) != length(Set{String}(sortedLowercase))
	return returnThis
end

function isVisitablePart2(cave::String, path::Array{String})
	# this assumes the cave variable has not been pushed to the end of the path yet.
	# cave is visitable if:
	# 	it is uppercase
	# 	it is "end"
	# 	it is lowercase and and not "start" and
	#		it has not been visited yet,
	# 		or no small cave has been visited twice so far
	if all(isuppercase, cave) || cave == "end"
		return true
	elseif all(islowercase, cave) && cave != "start" && (!in(cave, path) || !has2SmallCaves(path))
		return true
	else
		return false
	end
end

function calculatePaths(caveDict::Dict)
	# while path in queue
	#	pop path
	# 	get last cave in path
	#	add every possible adjacent cave as a new path (only caves with capital letters, or small letters not already in path)
	# 		if path ends in "end", add to set
	# 		else, add to queue

	pathSet = Set{Array{String}}() # Set of paths, where each path is an Array of strings that represent the order of caves

	pathQueue = [["start"]] # push to back, popfirst from front

	while(!isempty(pathQueue))
		currPath = popfirst!(pathQueue)
		lastCave = currPath[end]
		for nextCave in caveDict[lastCave]
			if nextCave == "end"
				newPath = push!(copy(currPath), nextCave)
				push!(pathSet, newPath)
			elseif all(isuppercase, nextCave) || !in(nextCave, currPath)
				newPath = push!(copy(currPath), nextCave)
				push!(pathQueue, newPath)
			end
		end
	end

	return pathSet
end

function calculatePaths2(caveDict::Dict)
	# while path in queue
	#	pop path
	# 	get last cave in path
	#	add every possible adjacent cave as a new path (only caves with capital letters, or small letters not already in path)
	# 		if path ends in "end", add to set
	# 		else, add to queue

	pathSet = Set{Array{String}}() # Set of paths, where each path is an Array of strings that represent the order of caves

	pathQueue = [["start"]] # push to back, popfirst from front

	while(!isempty(pathQueue))
		currPath = popfirst!(pathQueue)
		lastCave = currPath[end]
		for nextCave in caveDict[lastCave]
			if nextCave == "end"
				newPath = push!(copy(currPath), nextCave)
				push!(pathSet, newPath)
			elseif isVisitablePart2(nextCave, currPath)
				newPath = push!(copy(currPath), nextCave)
				push!(pathQueue, newPath)
			end
		end
	end

	return pathSet
end

function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	# Store paths in dictionary
	# Key is name of cave
	# value is set of all other caves it connects to

	caveDict = Dict{String, Set{String}}()

	for line in input
		splitLine = split(line, "-")

		if haskey(caveDict, splitLine[1])
			push!(caveDict[splitLine[1]], splitLine[2])
		else
			caveDict[splitLine[1]] = Set{String}([splitLine[2]])
		end

		if haskey(caveDict, splitLine[2])
			push!(caveDict[splitLine[2]], splitLine[1])
		else
			caveDict[splitLine[2]] = Set{String}([splitLine[1]])
		end
	end

	paths = calculatePaths(caveDict)
	println(length(paths))
end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	# Store paths in dictionary
	# Key is name of cave
	# value is set of all other caves it connects to

	caveDict = Dict{String, Set{String}}()

	for line in input
		splitLine = split(line, "-")

		if haskey(caveDict, splitLine[1])
			push!(caveDict[splitLine[1]], splitLine[2])
		else
			caveDict[splitLine[1]] = Set{String}([splitLine[2]])
		end

		if haskey(caveDict, splitLine[2])
			push!(caveDict[splitLine[2]], splitLine[1])
		else
			caveDict[splitLine[2]] = Set{String}([splitLine[1]])
		end
	end

	paths = calculatePaths2(caveDict)
	println(length(paths))
end

part2("input.txt")