with open("input.txt") as f:
	arr = []
	passArr = []
	failArr = []

	for line in f:
		arr.append(int(line))

	increasingCounter = 0

	for i in range(0, len(arr)-1):
		if arr[i] < arr[i+1]:
			increasingCounter = increasingCounter + 1
			passArr.append((arr[i], arr[i+1]))
		else:
			failArr.append((arr[i], arr[i+1]))

	# print(len(passArr))
	# print(len(failArr))

	for i in failArr:
		print(i)
	print(increasingCounter)
