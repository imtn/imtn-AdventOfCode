function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)
	input = parse.(Int64, input)

	increasingCounter::Int64 = 0
	for i in 2:length(input)
		if input[i - 1] < input[i]
			increasingCounter += 1
		end
	end

	println(increasingCounter)
end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)
	input = parse.(Int64, input)

	increasingCounter::Int64 = 0
	previous3::Int64 = input[1] + input[2] + input[3]
	current3::Int64 = 0

	for i in 2:length(input)-2
		current3 = input[i] + input[i+1] + input[i+2]
		if current3 > previous3
			increasingCounter += 1
		end
		previous3 = current3
	end

	println(increasingCounter)
end

part2("input.txt")