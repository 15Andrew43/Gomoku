import pygame as pg

pg.init()



class InputBox:

    COLOR_INACTIVE = pg.Color('lightskyblue3')
    COLOR_ACTIVE = pg.Color('dodgerblue2')
    FONT = pg.font.Font(None, 32)

    def __init__(self, name, x, y, w, h, text=''):
        self.name = name
        self.input_rect = pg.Rect(x, y, w, h)
        self.active_rect = pg.Rect(x + w + 20, y, 70, 30)
        self.color = InputBox.COLOR_INACTIVE
        self.text = text
        self.txt_surface = InputBox.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.active_rect.collidepoint(event.pos):
                print(self.text)
                text = self.text
                self.text = ''
                self.txt_surface = InputBox.FONT.render(self.text, True, self.color)
                return text

            # If the user clicked on the input_box rect.
            if self.input_rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    text = self.text
                    self.text = ''
                    self.txt_surface = InputBox.FONT.render(self.text, True, self.color)
                    return text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = InputBox.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.input_rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.input_rect.x+5, self.input_rect.y+5))
        screen.blit(InputBox.FONT.render(self.name, True, self.color), (self.active_rect.x+5, self.active_rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.input_rect, 2)
        pg.draw.rect(screen, self.color, self.active_rect, 2)
        # pg.draw.rect(screen, self.color, ())




def input_name():
    screen1 = pg.display.set_mode((400, 70))
    clock = pg.time.Clock()
    input_box = InputBox(20, 20, 140, 30)
    # input_box2 = InputBox(100, 300, 140, 32)
    # input_boxes = [input_box1, input_box2]
    # input_boxes = [input_box1]
    done = False

    global text

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            text = input_box.handle_event(event)

        if text:
            pg.quit()
            return text

        input_box.update()

        screen1.fill((30, 30, 30))
        input_box.draw(screen1)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    input_name()
    # pg.quit()