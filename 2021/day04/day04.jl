# A board is a 5x5 array. An array of boards is an array of 5x5 arrays.
function parseBoards(strArray)
	boardArray = []
	currBoard = Array{Int64}(undef, 5, 5)

	cBIndex = 1 # currBoard Index

	for strRow in strArray
		if isempty(strRow) # reached newline row, save current board and start new one
			push!(boardArray, currBoard)
			currBoard = Array{Int64}(undef, 5, 5)
			cBIndex = 1
		else # row has numbers, save it to currBoard
			currBoard[cBIndex, :] = parse.(Int, filter(x->!isempty(x), split(strRow, " ")))
			cBIndex += 1
		end
	end
	push!(boardArray, currBoard) # save the final board

	return boardArray
end

# considers all bingo numbers at once and looks for the first bingo board in array that has 5 in row horizontally or vertically
# return winning board array, or -1 if no winners
function has5inRow(bingoBoardArr, bingoNumArr)
	# loop over each board. for each board
	# build set of coordinates of marked squares
	# check if set contains 5 with same x or same y

	markedTupleSet = Set{Tuple}()

	for board in bingoBoardArr
		# build set of coords of marked squares
		for num in bingoNumArr
			coords = findfirst(isequal(num), board)
			if !isnothing(coords)
				push!(markedTupleSet, Tuple(findfirst(isequal(num), board)))
			end
		end

		# check row and columns, 1-5
		for i in 1:5
			if length(filter(t->t[1] == i, markedTupleSet)) == 5
				# Bingo!
				# println("Bingo!")
				# println(filter(t->t[1] == i, markedTupleSet))
				# println(board)
				# println(bingoNumArr)
				return board
			elseif length(filter(t->t[2] == i, markedTupleSet)) == 5
				# Bingo!
				# println("Bingo!")
				# println(filter(t->t[2] == i, markedTupleSet))
				# println(board)
				# println(bingoNumArr)
				return board
			end
		end

		markedTupleSet = Set{Tuple}()
	end

	return -1
end

function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	bingoNumArr = parse.(Int, split(input[1], ","))

	# parse boards
	boards = parseBoards(input[3:end])
	winningBoard = -1
	winningBingoNumIndex = 5

	# start with the first 5 bingo numbers and check if they trigger 5 in row. Then continue adding numbers until find first 5 in row
	for i in 5:length(bingoNumArr)
		winningBoard = has5inRow(boards, bingoNumArr[1:i])
		if winningBoard != -1
			winningBingoNumIndex = i
			break
		end
	end

	if winningBoard == -1
		print("winningBoard is still -1")
		quit()
	end

	winningNumArray = bingoNumArr[1:winningBingoNumIndex]

	sumOfUnmarked = sum(filter(x->!in(x, winningNumArray), winningBoard))

	println(sumOfUnmarked * winningNumArray[end])
end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	bingoNumArr = parse.(Int, split(input[1], ","))

	# parse boards
	boards = parseBoards(input[3:end])
	winningBoard = -1
	bingoNumIndex = 5

	# start with first 5 bingo numbers, gradually expand. Remove boards that win until one remains.
	for i in 5:length(bingoNumArr)
		winningBoard = has5inRow(boards, bingoNumArr[1:i])
		while winningBoard != -1
			deleteat!(boards, findfirst(isequal(winningBoard), boards))
			winningBoard = has5inRow(boards, bingoNumArr[1:i])
			if length(boards) == 1
				bingoNumIndex = i
				break;
			end
		end
		if length(boards) == 1
			break;
		end
	end

	if length(boards) != 1
		println("Not 1 board left after removing board.")
		println(boards)
		exit()
	end

	# Find what numbers the last one needs to win, and calculate score.
	# Progressively add bingo numbers until it doesn't return -1
	# Then calculate score
	boardWins = -1
	while (boardWins == -1)
		boardWins = has5inRow(boards, bingoNumArr[1:bingoNumIndex])
		bingoNumIndex += 1
	end
	bingoNumIndex -= 1
	lastBoard = boards[1]
	sumOfUnmarked = sum(filter(x->!in(x, bingoNumArr[1:bingoNumIndex]), lastBoard))

	println(sumOfUnmarked)
	println(sumOfUnmarked * bingoNumArr[bingoNumIndex])
end

part2("input.txt")