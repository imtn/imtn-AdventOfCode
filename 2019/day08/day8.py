from PIL import Image
import sys

def getPixelValue(image, x, y):
	index = (y * 25) + x # index in image, which where layer stores pixels in 1d array
	for layer in image:
		if layer[index] == 0:
			return 0
		if layer[index] == 1:
			return 1
	print("Did not find color for pixel " + str((x, y)) + " in image.")
	sys.exit()
	return


def part1():
	width = 25
	height = 6
	size = width * height

	fewest0digits = sys.maxsize
	num1digits = 0
	num2digits = 0
	image = [[]]
	imageIndex = 0
	layerIndex = 0
	curr0 = 0
	curr1 = 0
	curr2 = 0
	with open('input.txt') as f:
		message = f.readline().strip()
		
		# Image is stored in a list of lists
		# Where the index in the outer list is the layer
		# and the inner list is the actual data
		# so the image is a list of layers
		# and a layer is a list of pixels
		# Loop through input, fill all layers, and after filling each layer,
		# Check if it has fewer 0 digits, and fill in vars if so.

		for pixel in message:
			if layerIndex == size:
				print("Filled layer")
				layerIndex = 0
				imageIndex += 1
				image.append([])

				print("Zero is")
				print(curr0)
				print(curr0 + curr1 + curr2)

				if curr0 < fewest0digits:
					print("Entered")
					fewest0digits = curr0
					num1digits = curr1
					num2digits = curr2
				curr0 = 0
				curr1 = 0
				curr2 = 0
				
			pixel = int(pixel)
			image[imageIndex].append(pixel)

			layerIndex += 1

			if pixel == 0:
				curr0 += 1
			elif pixel == 1:
				curr1 += 1
			elif pixel == 2:
				curr2 += 2
			else:
				print("Found something else")
				print(pixel)
				sys.exit(0)

		print(fewest0digits)
		print(num1digits)
		print(num2digits)
		print(num1digits*num2digits)
		for layer in image:
			print("Layer is:")
			print(layer)
			print(layer.count(0))
			print(layer.count(1)*layer.count(2))

def part2():
	width = 25
	height = 6
	size = width * height

	image = [[]]
	imageIndex = 0
	layerIndex = 0
	with open('input.txt') as f:
		message = f.readline().strip()
		
		# Image is stored in a list of lists
		# Where the index in the outer list is the layer
		# and the inner list is the actual data
		# so the image is a list of layers
		# and a layer is a list of pixels

		for pixel in message:
			if layerIndex == size:
				layerIndex = 0
				imageIndex += 1
				image.append([])
				
			pixel = int(pixel)
			image[imageIndex].append(pixel)

			layerIndex += 1

	#loop through each pixel in imageFile
	#get its value from image
	#save file

	imageFile = Image.new("1", (width, height))
	for x in range(width):
		for y in range(height):
			value = getPixelValue(image, x, y) # Does this work with ones and zeroes?
			imageFile.putpixel((x, y), value)
	imageFile.save("image.png")


def main():
	# part1()
	part2()

main()