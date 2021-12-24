function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	pointDict = Dict(')' => 3, ']' => 57, '}' => 1197, '>' => 25137)
	pairDict = Dict('(' => ')', '[' => ']', '{' => '}', '<' => '>')
	openCharSet = Set(['(', '[', '{', '<'])
	runningScore = 0

	for line in input
		charStack = [] # A Stack of Char

		# for each char
		# if char is opening char, push char to stack
		# else (char is closing char), check if it matches last item (pop) in stack.
		# 	if matches, move on to next char
		# 	if doesn't match, increase score
		for char in line
			if char in openCharSet
				push!(charStack, char)
			else
				if char == pairDict[pop!(charStack)]
					continue
				else
					runningScore += pointDict[char]
				end
			end
		end

		# NOTE we don't have to worry about this in part 1, but if we want to make sure the chunk is closed, we should check here that the charStack is empty.

	end
	println("Final score is $runningScore")
end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	pointDict = Dict(')' => 1, ']' => 2, '}' => 3, '>' => 4)
	pairDict = Dict('(' => ')', '[' => ']', '{' => '}', '<' => '>')
	openCharSet = Set(['(', '[', '{', '<'])
	scoreArray = []

	for line in input
		charStack = [] # A Stack of Char
		runningScore = 0

		# for each char
		# if char is opening char, push char to stack
		# else (char is closing char), check if it matches last item (pop) in stack.
		# 	if matches, move on to next char
		# 	if doesn't match, empty stack and move to next line (effectively skips this corrupted line)
		for char in line
			if char in openCharSet
				push!(charStack, char)
			else
				if char == pairDict[pop!(charStack)]
					continue
				else
					empty!(charStack)
					break
				end
			end
		end

		# If charStack has characters, let's close it and count score
		while !isempty(charStack)
			currChar = pop!(charStack)
			runningScore = (runningScore * 5) + pointDict[pairDict[currChar]]
		end

		if runningScore != 0
			push!(scoreArray, runningScore)
		end
	end
	
	middleScore = (sort!(scoreArray))[trunc(Int, (length(scoreArray) + 1) / 2)]
	println("Middle score is $middleScore")
end

part2("input.txt")