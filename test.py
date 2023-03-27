class g():
	def __init__(self, x):
		self.x = x
	def change_x(self, y):
		self.x = y
class a():
	def __init__(self, g):
		self.gg = g
G = g(1)
A = a(G)
G.change_x(2)
print(A.gg.x)