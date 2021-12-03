class testClass:
	def __init__(self, x, y):
		self.x = x
		self.y = y


def main():
	test = testClass(5,3)
	print(test.x)
	print(test.y)
	test.x = 2
	print(test)
	print(test.x)

main()