# Color Shapes
# Author: Stepan Nazarov aka Susllike


# NOT AVAILABLE ANYMORE - TOO SLOW COMPARED TO OTHER METHODS
#import experimental_drawing as ed

import pygame
import pygame_gui
import math
from random import randint, choice
from sys import exit
from shape import Shape

#@profile # Performance testing via kernprof
def main():
	"""Putting everything into one function 
		for easier performance testing."""

	# All the stuff that can be changed!
  
	# Since the resizable version doesn't work, just toggle these
	screen_width = 1000
	screen_height = 600

	# How many shapes to add at once when you click on the add button
	num_to_add = 10
	num_to_remove = 1

	# The maximum distance for a line to still be drawn
	max_distance = 250 # CAN'T BE LOWER THAN 200
  
	# END of change-able stuff

	def maprange(dist):
		"""Determine the thickness of a connecting line 
		between two shapes based on distance."""
		
		if 0 <= dist < 50: return 5
		if 50 <= dist < 100: return 4
		if 100 <= dist < 150: return 3
		if 150 <= dist < 200: return 2
		if 200 <= dist <= max_distance: return 1

	def mix_colors(color_1, color_2):
		"""Mix the two color tuples for an average 
		color line between two figures. 
		Not used for gradient lines."""
		
		r1, g1, b1 = color_1
		r2, g2, b2 = color_2

		return (int((r1+r2)/2), int((g1+g2)/2), int((b1+b2)/2))

	def check_events():
		"""Event loop. Checks for any 
		window or button pressing actions."""
		global clean_the_playground

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
        # Quit
				pygame.quit()
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
          # Quit
					pygame.quit()
					exit()

			if event.type == pygame_gui.UI_BUTTON_PRESSED:
			    if event.ui_element == add_button:
			    	# Add shapes
			    	for _ in range(num_to_add):
				        figures.append(
						        	Shape(
						        			(
						        				0, 
						        				playground_rect.width,
						        				playground_rect.height,
						        				0
						        			)
						        		)
						        	)

			    elif event.ui_element == remove_button:
			    	# Remove random shape(s)
			        if figures:
			        	if len(figures) >= num_to_remove:
			        		for _ in range(num_to_remove):
				        		figures.remove(choice(figures))
				        else:
				        	figures.clear()

			    elif event.ui_element == clear_button:
			    	# Remove all shapes
			        figures.clear()
			        playground.fill((0, 0, 0))

			    elif event.ui_element == quit_button:
			    	# Quit
			    	pygame.quit()
			    	exit()

			manager.process_events(event)

	#@profile # Performance testing via kernprof
	def draw_the_line(surf, colors, start, end, width = 1):
		"""Gradient line drawing. Uses a series of lines with
		slowly changing colors instead of one connecting line to
		imitate one gradient-colored line as pygame doesn't have
		the functionality like this built-in.
		The current gradient code is shit, but there is a lot more work
		needed for the version that isn't shit."""

		# Define the starting and ending colors for the gradient - can be same
		color_1, color_2 = colors 

		# Calculate the difference between the starting and ending colors
		color_diff = [color_2[i] - color_1[i] for i in range(3)]

		# Set the number of steps for the gradient
		# 15 is almost perfect already; lower is worse but faster, higher is better but slower
		steps = 15

		# Calculate the increment for each color channel for each step
		color_inc = [color_diff[i] / steps for i in range(3)]

		cur_color = color_1
		cur_pos = start

		pos_diff = [end[i] - start[i] for i in range(2)]

		for _ in range(steps):
		# Draw a line from the current position to the next position
			pygame.draw.line(
				surf, 
				cur_color, 
				cur_pos, 
				(cur_pos[0] + pos_diff[0] / steps, cur_pos[1] + pos_diff[1] / steps),
				width
			)

		    # Update the current position
			cur_pos = (cur_pos[0] + pos_diff[0] / steps, cur_pos[1] + pos_diff[1] / steps)

			# This is ass at the moment. Rework in the future.
			cur_color = (
			   	int(min(255, max(0, cur_color[0] + color_inc[0]))), 
			   	int(min(255, max(0, cur_color[1] + color_inc[1]))), 
			   	int(min(255, max(0, cur_color[2] + color_inc[2])))
			)

	#@profile # Performance testing via kernprof
	def draw_lines():
		"""Determines the distances between every shape and
		whether to draw a connecting line between any given pair.
		Also updates the current connections of a shape with other shapes."""

		for i in range(len(figures)):
			for j in range(i):
				# Figure out the distance between two figures
				distance = math.dist(
								(figures[i].x_pos, figures[i].y_pos),
								(figures[j].x_pos, figures[j].y_pos)
							)

				if (distance <= max_distance and 
					figures[i].current_connections < figures[i].max_connections and
					figures[j].current_connections < figures[j].max_connections):
					draw_the_line(
						playground,
						[figures[i].color, figures[j].color],
						(figures[i].x_pos, figures[i].y_pos),
						(figures[j].x_pos, figures[j].y_pos),
						maprange(distance)
					)

					figures[i].current_connections += 1
					figures[j].current_connections += 1

	def draw_figures():
		"""Iterate over every existing shape, draw it on the screen,
		then check for screen collisions, rotate the points in space,
		reset existing connection count, and update the bounding box
		for the shape to 'bounce around in'."""

		for shape in figures:
			# Solid-colored shape
			if shape.filled:
				pygame.draw.polygon(
					playground, 
					shape.color, 
					shape.points,
					width = 0
				)

			# Black shape with colored border
			else:
				pygame.draw.polygon(
					playground, 
					(0, 0, 0), 
					shape.points,
					width = 0
				)
				pygame.draw.polygon(
					playground, 
					shape.color, 
					shape.points,
					width = 1
				)

			shape.check_collisions()
			shape.update_rotation_angle()
			shape.new_points()
			shape.reset_connections()
			shape.update_border((0, playground_rect.width,playground_rect.height, 0))

	# Initializing
	pygame.init()

	# Event manager
	manager = pygame_gui.UIManager((screen_width, screen_height))

	# Screen setup
	# RESIZABLE MODE ISN'T COMPLETE
	#screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

	# NON-RESIZABLE
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Color Shapes")
	window_icon = pygame.image.load("Images/icon.png")
	pygame.display.set_icon(window_icon)

	# Playground setup
	playground = pygame.Surface((screen_width - 230, screen_height - 20))
	playground_rect = playground.get_rect()

	# Menu setup
	MENU_WIDTH = 200
	menu_height = screen_height - 20
	menu = pygame.Surface((MENU_WIDTH, menu_height))
	#menu.fill((0, 0, 0))

	## Menu buttons
	# Add a shape
	add_button = pygame_gui.elements.UIButton(
	    relative_rect = pygame.Rect((screen_width - MENU_WIDTH - 5, 15), (190, 50)),
	    text = "Add a shape",
	    manager = manager,
	)

	# Add a random shape
	remove_button = pygame_gui.elements.UIButton(
	    relative_rect = pygame.Rect((screen_width - MENU_WIDTH - 5, 70), (190, 50)),
	    text = "Remove random",
	    manager = manager
	)

	# Remove all shapes
	clear_button = pygame_gui.elements.UIButton(
	    relative_rect = pygame.Rect((screen_width - MENU_WIDTH - 5, 125), (190, 50)),
	    text = "Clear screen",
	    manager = manager
	)

	# Exit the program
	quit_button = pygame_gui.elements.UIButton(
	    relative_rect = pygame.Rect((screen_width - MENU_WIDTH - 5, screen_height - 65), (190, 50)),
	    text = "Quit",
	    manager = manager
	)

	# Clock setup
	clock = pygame.time.Clock()
  
  # Shapes list
	figures = []

	# Main loop
	while True:
		new_screen_width = screen.get_width()
		new_screen_height = screen.get_height()

		# FOR RESIZABLE VERSION
		##if screen_width != new_screen_width or screen_height != new_screen_height:
		##	screen_width = new_screen_width
		##	screen_height = new_screen_height
		##	
		##	playground = pygame.Surface((screen_width - 230, screen_height - 20))
		##	playground_rect = playground.get_rect()
		##
		##	menu = pygame.Surface((MENU_WIDTH, screen_height - 20))

		time_delta = clock.tick(60) / 1000.

		# Event loop
		check_events()

		# UI update
		manager.update(time_delta)

		# Surface fills
		# Clean the background from slight OOB pixels from the shape collisions
		screen.fill((255, 255, 255))
		
		# Uncomment for cool patterns
		playground.fill((0, 0, 0))

		draw_lines() # Lines
		draw_figures() # Shapes - drawn after because layering
		
		# Screen updates
		screen.blit(playground, (10, 10))
		screen.blit(menu, (screen_width - menu.get_width() - 10, 10))
		manager.draw_ui(screen)
		pygame.display.update()

# Start the show
if __name__ == "__main__":
	main()
