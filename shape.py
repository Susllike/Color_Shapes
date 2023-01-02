import math
from random import randint

class Shape:
	"""Class for managing the geometric 
  shapes in the playground Surface."""
  
	def __init__(self, border):
    
    # Bounding box
		self.top, self.right, self.bottom, self.left = border

		self.radius = randint(10, 30) # Size
		self.sides = randint(3, 10) # Num of sides
		
		self.rot_angle = randint(0, 359) # Initial rotation angle
		self.cw_or_ccw = 1 if randint(0, 1) else -1 # Which way to rotate

		self.x_pos = randint(self.left + self.radius, self.right - self.radius)
		self.x_v = randint(1, 2) if randint(0, 1) else -randint(1, 2) # x velocity
    
		self.y_pos = randint(self.top + self.radius, self.bottom - self.radius)
		self.y_v = randint(1, 2) if randint(0, 1) else -randint(1, 2) # y velocity
    
		self.color = (randint(0, 255), randint(0, 255), randint(0, 255)) # Shape color

		self.new_points() # Calculate the points' positions of the shape

		self.filled = randint(0, 1) # 1 - Flat colored, 0 - black with color border

		self.current_connections = 0
    # Can only connect to as many shapes as how many sides you have
		self.max_connections = self.sides

	def check_collisions(self):
    """Check the collisions with the bounding box and act accordingly."""
    
		self.x_pos += self.x_v
		if (self.x_pos > (self.right - self.radius)):
			self.x_pos = self.right - self.radius
			self.x_v = -self.x_v
			self.cw_or_ccw = 1 if randint(0, 1) else -1
			self.x_v = randint(1, 2) if randint(0, 1) else -randint(1, 2)

		if self.x_pos < (self.left + self.radius):
			self.x_pos = self.left + self.radius
			self.x_v = -self.x_v
			self.cw_or_ccw = 1 if randint(0, 1) else -1
			self.x_v = randint(1, 2) if randint(0, 1) else -randint(1, 2)

		self.y_pos += self.y_v
		if (self.y_pos > (self.bottom - self.radius)):
			self.y_pos = self.bottom - self.radius
			self.y_v = -self.y_v
			self.cw_or_ccw = 1 if randint(0, 1) else -1
			self.y_v = randint(1, 2) if randint(0, 1) else -randint(1, 2)
		
		if self.y_pos < (self.top + self.radius):
			self.y_pos = self.top + self.radius
			self.y_v = -self.y_v
			self.cw_or_ccw = 1 if randint(0, 1) else -1
			self.y_v = randint(1, 2) if randint(0, 1) else -randint(1, 2)

	def update_rotation_angle(self):
    """Rotate in space."""
		self.rot_angle = self.rot_angle % 360 + 1 * self.cw_or_ccw

	def new_points(self):
    """Generate the points' positions"""
    
		self.angles = [
					(360/self.sides)*i + self.rot_angle 
					for i in range(self.sides)
				]

		self.points = [
		            (
		                int(self.radius * math.cos(math.radians(angle)) 
		                	+ self.x_pos), 
		                int(self.radius * math.sin(math.radians(angle)) 
		                	+ self.y_pos)
		            )
		            
		            for angle in self.angles
		        ]

	def reset_connections(self):
		self.current_connections = 0

  # Strictly for the resizable version of the window
	def update_border(self, new_border):
    """Update the bounding box for collisions."""
		self.top, self.right, self.bottom, self.left = new_border
		self.check_collisions() # Check if outside the box
