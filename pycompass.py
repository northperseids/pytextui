import pygame
import textwrap
import json

class TextModule():
    """
    Module for text, scroll, and dialogue boxes. Must be initialized OUTSIDE of the event loop to function properly.\n
    (Default text values: max_chars = 40, max_lines = 10, key trigger = Spacebar. Change these with "set_[property]" functions.)
    """
    def __init__(self, surface:pygame.Surface):
        self.surface = surface

        # defaults; can be changed with set functions
        self.max_chars = 40        
        self.max_lines = 10
        self.bg_color = (0,0,0,200)
        self.border_color = 'White'
        self.font_color = 'White'
        self.arrowup = None
        self.arrowdown = None

        # calculated values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.outer_x = self.width * 0.057 # 40
        self.outer_y = self.height * 0.043 # 30
        self.inner_x = self.outer_x + 10 # 50
        self.inner_y = self.outer_y + 10 # 40

        # other vals
        self.scroll_i = 0
        self.dialogue_i = 0
        self.key = pygame.K_SPACE

    def clear_box(self):
        """
        Clears the screen of any text boxes by blitting a blank surface.
        """
        clear_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        clear_surface.fill(pygame.Color(0,0,0,0))
        self.surface.blit(clear_surface, (self.outer_x, self.outer_y))

    def draw_text_box(self, text:str, font:pygame.font.Font):
        """
        Draws a text box with given text and font.
        """
        bg = pygame.Surface((self.width * 0.9,self.height * 0.9), pygame.SRCALPHA)
        border = pygame.Rect(self.outer_x - 1, self.outer_y - 1, self.width * 0.9 + 2, self.height * 0.9 + 2)
        pygame.draw.rect(self.surface, self.border_color, border, 1)
        bg.fill(self.bg_color)
        self.surface.blit(bg, (self.outer_x,self.outer_y))

        lines = self.__get_wrap_arr(text)
        y_offset = 0
        for line in lines:
            txt = font.render(line, True, self.font_color)
            self.surface.blit(txt, (self.inner_x, self.inner_y + y_offset))
            y_offset = y_offset + txt.get_height()

    def draw_scroll_box(self, text:str, font:pygame.font.Font, direction:int):
        """
        Draws a scroll-enabled box with given text.\n
        Needs to be given a mousewheel direction generated from the event loop.
        """
        self.arr = self.__get_wrap_arr(text)
        self.font = font

        # background and border
        bg = pygame.Surface((self.width * 0.9,self.height * 0.9), pygame.SRCALPHA)
        border = pygame.Rect(self.outer_x - 1, self.outer_y - 1, self.width * 0.9 + 2, self.height * 0.9 + 2)
        pygame.draw.rect(self.surface, self.border_color, border, 1)
        bg.fill(self.bg_color)
        self.surface.blit(bg, (self.outer_x,self.outer_y))

        # keep scroll ranges within limits
        if direction == -1:
            self.scroll_i = self.scroll_i + 1
        elif direction == 1:
            self.scroll_i = self.scroll_i - 1

        if self.scroll_i > len(self.arr) - self.max_lines:
            self.scroll_i = len(self.arr) - self.max_lines
        if self.scroll_i < 0:
            self.scroll_i = 0

        # display current text lines
        y_offset = 0
        if len(self.arr) > self.max_lines:
            cut_arr = self.arr[self.scroll_i:self.scroll_i+self.max_lines]
            for line in cut_arr:
                txt = self.font.render(line, True, self.font_color)
                self.surface.blit(txt, (self.inner_x, self.inner_y + y_offset))
                y_offset = y_offset + txt.get_height()
        elif len(self.arr) < self.max_lines:
            for line in self.arr:
                txt = self.font.render(line, True, self.font_color)
                self.surface.blit(txt, (self.inner_x, self.inner_y + y_offset))
                y_offset = y_offset + txt.get_height()

        # finally, throw everything on screen
        if len(self.arr) > self.max_lines and self.arrowup is not None:
            self.surface.blit(self.arrowup, (self.width * 0.85,self.outer_y))
            self.surface.blit(self.arrowdown, (self.width * 0.85,self.height * 0.85))
    
    def draw_sequence_box(self, dialogue_file, font, key):
        """
        Draw a box that cycles through lines provided in a JSON file.\n
        JSON format:\n
        [{"text":"line"}]
        """
        lines = self.__get_dialogue_array(dialogue_file)
        if key == pygame.K_SPACE:
            self.dialogue_i += 1
            self.scroll_i = 0
        if self.dialogue_i < len(lines):
            self.draw_text_box(lines[self.dialogue_i], font)
        else:
            pass

    def draw_scroll_sequence_box(self, dialogue_file:str, font:pygame.font.Font, key, direction:int):
        """
        Draw a scroll box that cycles through lines provided in a JSON file.\n
        JSON format:\n
        [{"text":"line"}]
        """
        lines = self.__get_dialogue_array(dialogue_file)
        if key == self.key:
            self.dialogue_i += 1
            self.scroll_i = 0
        if self.dialogue_i < len(lines):
            self.draw_scroll_box(lines[self.dialogue_i], font, direction)
        else:
            pass

    def set_dialogue_key(self, key):
        """
        Sets the key to trigger dialogue changes. (Space bar by default.)
        """
        self.key = key

    def set_bg_color(self, color):
        self.bg_color = color

    def set_max_chars(self, max_chars:int):
        self.max_chars = max_chars

    def set_max_lines(self, max_lines:int):
        self.max_lines = max_lines

    def set_border_color(self, color):
        self.border_color = color

    def set_font_color(self, color):
        self.font_color = color

    def set_arrow_images(self, arrowup:pygame.Surface, arrowdown:pygame.Surface):
        """
        Optionally sets two images to display as arrow-up and arrow-down indicators.\n
        (Cannot be clicked to scroll - YET.)
        """
        self.arrowup = arrowup
        self.arrowdown = arrowdown

    def __get_wrap_arr(self, text:str):
        """
        Generates an array of lines of text in which each line fits the specified character width declared in the text box module's init.
        """
        lines = []
        for line in text.splitlines():
            if line == '':
                lines.append(' ')
            if line:
                if len(line) <= self.max_chars:
                    lines.append(f'{line}')
                else:
                    lines.extend(textwrap.wrap(line, self.max_chars, replace_whitespace=False))
        return lines

    def __get_dialogue_array(self, dialogue_file:str):
        """
        Best for this to be placed outside the event loop as well to minimize the amount of times the file is accessed.
        """
        arr = []
        with open(dialogue_file, 'r') as file:
            content = json.load(file)
            for line in content:
                arr.append(line['text'])
        return arr