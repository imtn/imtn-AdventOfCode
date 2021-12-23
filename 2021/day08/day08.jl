function calculateValue(line::String)
	#=
	  aaaa
	 b    c
	 b    c
	  dddd
	 e    f
	 e    f
	  gggg

	Numbers and how many segments they have:
	0: 6
	1: 2
	2: 5
	3: 5
	4: 4
	5: 5
	6: 6
	7: 3
	8: 7
	9: 6

	How to find each of a-g:
	- by default, we know 1, 4, 7, 8 because they have unique number of segments
	a: 7 - 1
	c/6: 1 - 6. All 6-segments have 1 except for 6, which only has f.
	f: 1 - c.
	9: 4 - 9 = empty set. Since we know 6, the other two 6-segments must be 0 and 9. 9 is the only one that fulfills this condition.
	0: the 6-segment that's not 6 or 9.
	d: 8 - 0.
	b: the segment in 4 that's not c, d, or f.
	g: 9 - abcdf
	e: last letter
	build 2, 3, 5
	=#

	input = split(split(line, " |")[1], " ") # array of strings
	output = split(split(line, "| ")[2], " ") # array of strings
	inputArr = broadcast(x->Set(collect(x)), input) # a vector of sets of characters
	outputArr = broadcast(x->Set(collect(x)), output) # same as above
	numberDict = Dict{Int, Set{Char}}() # maps the number to a set of characters from its line-specific string representation
	segmentDict = Dict{Char, Char}() # maps the real segment letter to its line-specific segment letter

	numberDict[1] = first(filter(x->length(x) == 2, inputArr))
	numberDict[4] = first(filter(x->length(x) == 4, inputArr))
	numberDict[7] = first(filter(x->length(x) == 3, inputArr))
	numberDict[8] = first(filter(x->length(x) == 7, inputArr))
	segmentDict['a'] = first(setdiff(numberDict[7], numberDict[1]))
	numberDict[6] = first(filter(x->length(x) == 6 && !isempty(setdiff(numberDict[1], x)), inputArr))
	segmentDict['c'] = first(setdiff(numberDict[1], numberDict[6]))
	segmentDict['f'] = first(setdiff(numberDict[1], Set(segmentDict['c'])))
	numberDict[9] = first(filter(x->length(x) == 6 && x != numberDict[6] && isempty(setdiff(numberDict[4], x)), inputArr))
	numberDict[0] = first(filter(x->length(x) == 6 && x != numberDict[6] && x != numberDict[9], inputArr))
	segmentDict['d'] = first(setdiff(numberDict[8], numberDict[0]))
	segmentDict['b'] = first(setdiff(numberDict[4], Set([segmentDict['c'], segmentDict['d'], segmentDict['f']])))
	segmentDict['g'] = first(setdiff(numberDict[9], Set([segmentDict['a'], segmentDict['b'], segmentDict['c'], segmentDict['d'], segmentDict['f']])))
	segmentDict['e'] = first(setdiff(numberDict[8], Set([segmentDict['a'], segmentDict['b'], segmentDict['c'], segmentDict['d'], segmentDict['f'], segmentDict['g']])))
	numberDict[2] = Set([segmentDict['a'], segmentDict['c'], segmentDict['d'], segmentDict['e'], segmentDict['g']])
	numberDict[3] = Set([segmentDict['a'], segmentDict['c'], segmentDict['d'], segmentDict['f'], segmentDict['g']])
	numberDict[5] = Set([segmentDict['a'], segmentDict['b'], segmentDict['d'], segmentDict['f'], segmentDict['g']])

	valueStr = ""
	for i in outputArr
		valueStr *= string(first(filter(x->numberDict[x] == i, keys(numberDict))))
	end
	return parse(Int, valueStr)
end

function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	# count how many times digits 1, 4, 7, or 8 appear
	# they use 2, 4, 3, and 7 segments, respectively

	outputValues = broadcast(x->split(x, "|")[2], input)
	
	runningSum = 0
	for outputLine in outputValues
		outputLineArray = split(outputLine, " ")
		for outputWord in outputLineArray
			if length(outputWord) in Set{Int}([2, 3, 4, 7])
				runningSum += 1
			end
		end
	end

	println(runningSum)
end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	runningSum = 0
	for line in input
		runningSum += calculateValue(line)
	end
	@show runningSum
end

part2("input.txt")