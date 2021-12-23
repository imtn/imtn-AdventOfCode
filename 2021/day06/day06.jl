function passOneDay(fishAgeArray)
	newFishAgeArray = []
	for i in fishAgeArray
		if i == 0
			push!(newFishAgeArray, 6)
			push!(newFishAgeArray, 8)
		else
			push!(newFishAgeArray, i - 1)
		end
	end
	return newFishAgeArray
end

function newPassOneDay(fishDict)
	dictToReturn = Dict(i => 0 for i = 0:8)
	for i in 0:8
		if i == 0
			dictToReturn[6] = fishDict[i]
			dictToReturn[8] = fishDict[i]
		else
			dictToReturn[i-1] += fishDict[i]
		end
	end
	return dictToReturn
end

function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	fishArray = parse.(Int64, split(input[1], ","))

	for i in 1:80
		fishArray = passOneDay(fishArray)
	end

	println(length(fishArray))

end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	oldFishArray = sort(parse.(Int64, split(input[1], ",")))
	fishDict = Dict(i => 0 for i = 0:8)
	for i in oldFishArray
		fishDict[i] += 1
	end
	
	for i in 1:256
		fishDict = newPassOneDay(fishDict)
	end

	runningsum = 0
	for i in 0:8
		runningsum += fishDict[i]
	end
	@show runningsum
end

part2("input.txt")