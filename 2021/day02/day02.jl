function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	xCurr::Int64 = 0 # Horizontal Position
	yCurr::Int64 = 0 # Vertical Position

	for i in input
		instruction = split(i)
		if instruction[1] == "forward"
			xCurr += parse(Int64, instruction[2])
		elseif instruction[1] == "up"
			yCurr -= parse(Int64, instruction[2])
		elseif instruction[1] == "down"
			yCurr += parse(Int64, instruction[2])
		else
			println("Parsed weird instruction: $(instruction[1])")
			exit()
		end
	end

	println(xCurr * yCurr)
end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	xCurr::Int64 = 0 # Horizontal Position
	yCurr::Int64 = 0 # Vertical Position
	aim::Int64 = 0

	for i in input
		instruction = split(i)
		amount = parse(Int64, instruction[2])
		if instruction[1] == "forward"
			xCurr += amount
			yCurr += (aim * amount)
		elseif instruction[1] == "up"
			aim -= amount
		elseif instruction[1] == "down"
			aim += amount
		else
			println("Parsed weird instruction: $(instruction[1])")
			exit()
		end
	end

	println(xCurr * yCurr)
end

part2("input.txt")