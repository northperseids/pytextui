"""
Example main.py.

"""

import pygame
import pytextui

pygame.init()
screen = pygame.display.set_mode((700,700))
pygame.display.set_caption('EXAMPLE')
clock = pygame.time.Clock()
pygame.font.init()
running = True
dt = 0

# USER VARS
font = pygame.font.Font(None, 40)
lincos = pygame.font.Font('./fonts/Lincos.ttf', 60)
english = pygame.font.Font('./fonts/Metropolis.otf', 30)
bg_color = '#234e82'

# FUNCTIONAL VARS
direction = None
key = None

textmodule = pytextui.TextModule(screen, font=pygame.Font(None, 30))

box = pytextui.ScrollSequenceBox(screen)
box.add_line('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at sem odio. Duis vel erat eu turpis porttitor ornare sed sit amet est. In a ante bibendum, vulputate velit sit amet, luctus mi. Cras suscipit tristique enim. Sed orci mi, hendrerit in tortor sit amet, lacinia commodo magna. Curabitur accumsan vehicula nulla, viverra posuere urna. Phasellus posuere purus quis libero venenatis, at ullamcorper mauris pharetra. Praesent ac pharetra felis. Integer euismod rutrum arcu eu malesuada. Donec sagittis arcu non dignissim posuere. Etiam bibendum lorem ipsum, ac accumsan nibh tristique sed. Curabitur ornare arcu in libero sodales, fermentum imperdiet orci tempor. ')
box.add_line('Nunc ornare pretium sem, vel vulputate eros pellentesque at. Maecenas et lectus efficitur, fringilla est id, suscipit justo. Quisque laoreet odio sagittis, consequat sapien at, pretium massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vestibulum ex lectus, bibendum sed quam non, condimentum tempor tortor. Nam non lacus orci. Mauris pharetra erat at dolor venenatis venenatis. Fusce ac mauris posuere, commodo ex nec, molestie sem. Sed id aliquam nibh, eu molestie nisi. Nunc non tellus quis nisi ultricies bibendum. ')
box.add_line('Hello world!')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key = event.key
        elif event.type == pygame.KEYUP:
            key = None
        elif event.type == pygame.MOUSEWHEEL:
            direction = event.y
    
    # clear screeen with background color
    screen.fill(bg_color)
    
    box.draw(key, direction)

    # update pygame display
    pygame.display.flip()

    # reset input vals to prevent continuous triggers without mouse input
    direction = 0
    key = None

    dt = clock.tick(30) / 1000

# exit game when done
pygame.quit()