import pygame
import textwrap
import json

pygame.font.init()

class TextModule():
    """
    Base module for text boxes.\n
    Has methods to set values for things like max characters per line, max lines per screen, and default font/colors.
    """
    def __init__(self, surface:pygame.Surface):
        super().__init__()
        self.surface = surface

        # defaults; can be changed with set functions
        self.max_chars = 40        
        self.max_lines = 10
        self.bg_color = (0,0,0,200)
        self.border_color = 'White'
        self.font_color = 'White'
        self.arrowup = None
        self.arrowdown = None
        self.font = pygame.Font(None, 30)

        # calculated values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.outer_x = self.width * 0.057 # 40
        self.outer_y = self.height * 0.043 # 30
        self.inner_x = self.outer_x + 10 # 50
        self.inner_y = self.outer_y + 10 # 40

        # other vals
        self.scroll_i = 0
        self.sequence_index = 0
        self.key = pygame.K_SPACE

    def clear_box(self):
        """
        Clears the screen of any text boxes by blitting a blank surface.
        """
        clear_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        clear_surface.fill(pygame.Color(0,0,0,0))
        self.surface.blit(clear_surface, (self.outer_x, self.outer_y))

    def set_sequence_key(self, key):
        """
        Sets the key to trigger sequential text box changes. (Space bar by default.)
        """
        self.key = key

    def set_font(self, font:pygame.Font):
        self.font = font

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

    def set_arrows(self, arrowup:pygame.Surface, arrowdown:pygame.Surface):
        """
        Optionally sets two surfaces/images to display as arrow-up and arrow-down indicators.\n
        (Cannot be clicked to scroll - YET.)
        """
        self.arrowup = arrowup
        self.arrowdown = arrowdown

    def get_wrap_arr(self, text:str):
        """
        INTERNAL FUNCTION
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

    def get_sequence_array(self, dialogue_file:str):
        """
        INTERNAL FUNCTION
        """
        arr = []
        with open(dialogue_file, 'r') as file:
            content = json.load(file)
            for line in content:
                arr.append(line['text'])
        return arr
    
class TextBox(TextModule):
    """
    Plain text box.\n
    Use set_text() to add text. Optionally, use set_font() to set a specific font; otherwise, global font will be used.
    """
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        self.text = ''
        self.sub_font = self.font

    def set_text(self, text):
        self.text = text

    def set_font(self, font:pygame.Font):
        self.sub_font = font

    def draw(self):
        """
        Draws a text box with given text and font.
        """
        bg = pygame.Surface((self.width * 0.9,self.height * 0.9), pygame.SRCALPHA)
        border = pygame.Rect(self.outer_x - 1, self.outer_y - 1, self.width * 0.9 + 2, self.height * 0.9 + 2)
        pygame.draw.rect(self.surface, self.border_color, border, 1)
        bg.fill(self.bg_color)
        self.surface.blit(bg, (self.outer_x,self.outer_y))

        lines = self.get_wrap_arr(self.text)
        y_offset = 0
        for line in lines:
            txt = self.sub_font.render(line, True, self.font_color)
            self.surface.blit(txt, (self.inner_x, self.inner_y + y_offset))
            y_offset = y_offset + txt.get_height()

class SequenceBox(TextModule):
    """
    Box that cycles through lines in an array.\n
    Has to be created OUTSIDE the event loop for the sequence to work properly.\n
    Use add_line() to add a new text line. Optionally, use set_font() to set a specific font; otherwise, global font will be used.\n
    JSON format: [{"text":"line"}]
    """
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        self.sub_font = self.font
        self.sequence = []

    def set_font(self, font:pygame.Font):
        self.sub_font = font

    def add_line(self, text):
        self.sequence.append(text)

    def draw(self, key):
        lines = self.sequence
        if key == pygame.K_SPACE:
            self.sequence_index = self.sequence_index + 1
        if self.sequence_index < len(lines):
            box = TextBox(self.surface)
            box.set_text(lines[self.sequence_index])
            box.set_font(self.sub_font)
            box.draw()
        else:
            pass

class SequenceJsonBox(TextModule):
    """
    Box that cycles through lines given in a JSON file.\n
    Has to be created OUTSIDE the event loop for the sequence to work properly.\n
    Use set_sequence() to point to the JSON file. Optionally, use set_font() to set a specific font; otherwise, global font will be used.\n
    JSON format: [{"text":"line"}]
    """
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        self.sub_font = self.font
        self.sequence = []

    def set_font(self, font:pygame.Font):
        self.sub_font = font

    def set_sequence(self, sequence_file):
        with open(sequence_file, 'r') as file:
            content = json.load(file)
            for line in content:
                self.sequence.append(line)

    def draw(self, key):
        lines = self.sequence
        if key == pygame.K_SPACE:
            self.sequence_index = self.sequence_index + 1
        if self.sequence_index < len(lines):
            box = TextBox(self.surface)
            box.set_text(lines[self.sequence_index]['text'])
            box.set_font(self.sub_font)
            box.draw()
        else:
            pass

class ScrollBox(TextModule):
    """
    Plain scrollable box.\n
    Use set_text() to add text. Optionally, use set_font() to set a specific font; otherwise, global font will be used.
    """
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        self.text = ''
        self.sub_font = self.font

    def set_text(self, text):
        self.text = text

    def set_font(self, font:pygame.Font):
        self.sub_font = font

    def draw(self, direction):
        """
        Needs to be given a mousewheel direction generated from the event loop.
        """
        self.arr = self.get_wrap_arr(self.text)

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
                txt = self.sub_font.render(line, True, self.font_color)
                self.surface.blit(txt, (self.inner_x, self.inner_y + y_offset))
                y_offset = y_offset + txt.get_height()
        elif len(self.arr) < self.max_lines:
            for line in self.arr:
                txt = self.sub_font.render(line, True, self.font_color)
                self.surface.blit(txt, (self.inner_x, self.inner_y + y_offset))
                y_offset = y_offset + txt.get_height()

        # finally, throw everything on screen
        if len(self.arr) > self.max_lines and self.arrowup is not None:
            self.surface.blit(self.arrowup, (self.width * 0.85,self.outer_y))
            self.surface.blit(self.arrowdown, (self.width * 0.85,self.height * 0.85))

class ScrollSequenceBox(TextModule):
    """
    Box that cycles through scrollable lines of text in an array.\n
    Has to be created OUTSIDE the event loop for the sequence to work properly.\n
    Use add_line to add text. Optionally, use set_font() to set a specific font; otherwise, global font will be used.\n
    JSON format: [{"text":"line"}]
    """
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        self.sub_font = self.font
        self.sequence = []

    def set_font(self, font:pygame.Font):
        self.sub_font = font

    def add_line(self, text:str):
        self.sequence.append(text)

    def draw(self, key, direction:int):

        total_array = []

        for entry in self.sequence:
            lines = self.get_wrap_arr(entry)
            total_array.append(lines)

        if key == self.key:
            self.sequence_index = self.sequence_index + 1
            self.scroll_i = 0
        
        self.sub_arr = total_array[self.sequence_index]

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

        if self.scroll_i > len(self.sub_arr) - self.max_lines:
            self.scroll_i = len(self.sub_arr) - self.max_lines
        if self.scroll_i < 0:
            self.scroll_i = 0

        # display current text lines
        y_offset = 0
        if len(self.sub_arr) > self.max_lines:
            cut_arr = self.sub_arr[self.scroll_i:self.scroll_i+self.max_lines]
            for line in cut_arr:
                txt = self.sub_font.render(line, True, self.font_color)
                self.surface.blit(txt, (self.inner_x, self.inner_y + y_offset))
                y_offset = y_offset + txt.get_height()
        elif len(self.sub_arr) < self.max_lines:
            for line in self.sub_arr:
                txt = self.sub_font.render(line, True, self.font_color)
                self.surface.blit(txt, (self.inner_x, self.inner_y + y_offset))
                y_offset = y_offset + txt.get_height()

        # finally, throw everything on screen
        if len(self.sub_arr) > self.max_lines and self.arrowup is not None:
            self.surface.blit(self.arrowup, (self.width * 0.85,self.outer_y))
            self.surface.blit(self.arrowdown, (self.width * 0.85,self.height * 0.85))

class ScrollSequenceJsonBox(TextModule):
    """
    Box that cycles through scrollable lines of text given in a JSON file.\n
    Has to be created OUTSIDE the event loop for the sequence to work properly.\n
    Use set_sequence() to point to a JSON file. Optionally, use set_font() to set a specific font; otherwise, global font will be used.\n
    JSON format: [{"text":"line"}]
    """
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        self.sub_font = self.font
        self.sequence = []

    def set_font(self, font:pygame.Font):
        self.sub_font = font

    def set_sequence(self, sequence_file):
        with open(sequence_file, 'r') as file:
            content = json.load(file)
            for line in content:
                self.sequence.append(line)

    def draw(self, key, direction:int):

        total_array = []

        for entry in self.sequence:
            lines = self.get_wrap_arr(entry['text'])
            total_array.append(lines)

        if key == self.key:
            self.sequence_index = self.sequence_index + 1
            self.scroll_i = 0
        if self.sequence_index < len(lines):
            self.arr = total_array[self.sequence_index]

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
                txt = self.sub_font.render(line, True, self.font_color)
                self.surface.blit(txt, (self.inner_x, self.inner_y + y_offset))
                y_offset = y_offset + txt.get_height()
        elif len(self.arr) < self.max_lines:
            for line in self.arr:
                txt = self.sub_font.render(line, True, self.font_color)
                self.surface.blit(txt, (self.inner_x, self.inner_y + y_offset))
                y_offset = y_offset + txt.get_height()

        # finally, throw everything on screen
        if len(self.arr) > self.max_lines and self.arrowup is not None:
            self.surface.blit(self.arrowup, (self.width * 0.85,self.outer_y))
            self.surface.blit(self.arrowdown, (self.width * 0.85,self.height * 0.85))

class MultifontBox(TextModule):
    """
    Plain text box that allows multiple fonts.\n
    Use add_text_line() to add text.
    """
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        self.lines = []
        self.index = 0

    def add_text_line(self, text:str, font:pygame.Font):
        self.lines.append([text, font])

    def draw(self):
        bg = pygame.Surface((self.width * 0.9,self.height * 0.9), pygame.SRCALPHA)
        border = pygame.Rect(self.outer_x - 1, self.outer_y - 1, self.width * 0.9 + 2, self.height * 0.9 + 2)
        pygame.draw.rect(self.surface, self.border_color, border, 1)
        bg.fill(self.bg_color)
        self.surface.blit(bg, (self.outer_x,self.outer_y))

        y_offset = 0
        for line in self.lines:
            text = line[0]
            font = line[1]
            txt = font.render(text, True, self.font_color)
            self.surface.blit(txt, (self.inner_x, self.inner_y + y_offset))
            y_offset = y_offset + txt.get_height()