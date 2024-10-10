"""
Example main.py.

The asyncio stuff is important for pygbag.

The textbox class CAN handle \n characters - pygame as-is typically cannot, although pygame-ce *might* be able to.
"""

import asyncio
import pygame
from pycompass import TextModule

pygame.init()
screen = pygame.display.set_mode((700,700))
pygame.display.set_caption('LANG')
clock = pygame.time.Clock()
pygame.font.init()
running = True
dt = 0

# USER VARS
max_chars = 40
max_lines = 10
textbox_bg_color = (0,0,0,200)
border_color = 'White'
font_color = 'White'
font = pygame.font.Font(None, 40)
bg_color = '#234e82'

# FUNCTIONAL VARS
mouse_dir = None
key = None

ui = TextModule(screen)

#async def main():
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            # will need to implement mouse clicks here
            pass
        elif event.type == pygame.KEYDOWN:
            key = event.key
        elif event.type == pygame.KEYUP:
            key = None
        elif event.type == pygame.MOUSEWHEEL:
            mouse_dir = event.y
    
    # clear screeen with background color
    screen.fill(bg_color)
    
    #ui.draw_text_box("Hello world!\nHello world!\n\nHi there!", font)
    #ui.draw_scroll_box("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\nSed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?", font, mouse_dir)
    #ui.draw_sequence_box('./dialogue_example.json', font, key)
    ui.draw_scroll_sequence_box('./dialogue_example_scroll.json', font, key, mouse_dir)

    # update pygame display
    pygame.display.flip()

    # reset input vals to prevent continuous triggers without mouse input
    mouse_dir = 0
    key = None

    dt = clock.tick(30) / 1000
#    await asyncio.sleep(0)

# exit game when done
pygame.quit()

#asyncio.run(main())