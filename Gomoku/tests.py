import pygame as pg

pg.init()


text = ''

class InputBox:

    COLOR_INACTIVE = pg.Color('lightskyblue3')
    COLOR_ACTIVE = pg.Color('dodgerblue2')
    FONT = pg.font.Font(None, 32)

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = InputBox.COLOR_INACTIVE
        self.text = text
        self.txt_surface = InputBox.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
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
                    return self.text
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = InputBox.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)



def input_name():
    screen = pg.display.set_mode((640, 70))
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
            return text


        input_box.update()

        screen.fill((30, 30, 30))
        input_box.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    input_name()
    pg.quit()