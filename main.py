import pygame as pg

JUMPSET = set(" .,:;()[]{}")

BINDING_EMACS = {
    "BACKSPACE": lambda e: e.key == pg.K_BACKSPACE,
    "DELETE_CHAR": lambda e: e.mod == pg.KMOD_LCTRL and e.key == pg.K_d,
    "DELETE_WORD": lambda e: e.mod == pg.KMOD_LALT and e.key == pg.K_d,
    "DELETE_FORWARD": lambda e: e.mod == pg.KMOD_LCTRL and e.key == pg.K_k,
    "LEFT_CHAR": lambda e: e.mod == pg.KMOD_LCTRL and e.key == pg.K_b,
    "RIGHT_CHAR": lambda e: e.mod == pg.KMOD_LCTRL and e.key == pg.K_f,
    "LEFT_WORD": lambda e: e.mod == pg.KMOD_LALT and e.key == pg.K_b,
    "RIGHT_WORD": lambda e: e.mod == pg.KMOD_LALT and e.key == pg.K_f,
    "START": lambda e: e.mod == pg.KMOD_LCTRL and e.key == pg.K_a,
    "END": lambda e: e.mod == pg.KMOD_LCTRL and e.key == pg.K_e
}


class Editor:

    def __init__(self, font, binding):

        self.buffer = ""
        self.cursor = 0
        self.w, self.h = 0, 0
        self.surface = pg.Surface((0, 0), pg.SRCALPHA)
        self.font = font
        self.binding = binding
        self.tick = 0

    def listen(self, event):

        if event.type == pg.KEYDOWN:

            self.tick = 0

            if self.binding["BACKSPACE"](event):
                self.buffer = self.buffer[:self.cursor-1] + self.buffer[self.cursor:]
                self.cursor -= 1

            elif self.binding["DELETE_CHAR"](event):
                self.buffer = self.buffer[:self.cursor] + self.buffer[self.cursor+1:]

            elif self.binding["DELETE_WORD"](event):
                if self.cursor < len(self.buffer):
                    i = self.cursor + 1
                    while i < len(self.buffer) - 1:
                        if (self.buffer[i] not in JUMPSET and
                            self.buffer[i+1] in JUMPSET):
                            break
                        i += 1
                    self.buffer = self.buffer[:self.cursor] + self.buffer[i+1:]

            elif self.binding["DELETE_FORWARD"](event):
                self.buffer = self.buffer[:self.cursor]

            elif self.binding["LEFT_CHAR"](event):
                if 0 < self.cursor:
                    self.cursor -= 1

            elif self.binding["RIGHT_CHAR"](event):
                if self.cursor < len(self.buffer):
                    self.cursor += 1

            elif self.binding["LEFT_WORD"](event):
                if self.cursor > 0:
                    i = self.cursor - 1
                    while i > 0:
                        if (self.buffer[i] not in JUMPSET and
                            self.buffer[i-1] in JUMPSET):
                            break
                        i -= 1
                    self.cursor = i

            elif self.binding["RIGHT_WORD"](event):
                if self.cursor < len(self.buffer):
                    i = self.cursor + 1
                    while i < len(self.buffer) - 1:
                        if (self.buffer[i] not in JUMPSET and
                            self.buffer[i+1] in JUMPSET):
                            break
                        i += 1
                    self.cursor = i + 1

            elif self.binding["START"](event):
                self.cursor = 0

            elif self.binding["END"](event):
                self.cursor = len(self.buffer)

            elif event.mod == pg.KMOD_LSHIFT and event.key == pg.K_9:
                self.buffer = self.buffer[:self.cursor] + "(" + self.buffer[self.cursor:]
                self.cursor += 1
                self.buffer = self.buffer[:self.cursor] + ")" + self.buffer[self.cursor:]

            elif event.mod == pg.KMOD_LSHIFT and event.key == pg.K_LEFTBRACKET:
                self.buffer = self.buffer[:self.cursor] + "{" + self.buffer[self.cursor:]
                self.cursor += 1
                self.buffer = self.buffer[:self.cursor] + "}" + self.buffer[self.cursor:]

            elif event.key == pg.K_LEFTBRACKET:
                self.buffer = self.buffer[:self.cursor] + "[" + self.buffer[self.cursor:]
                self.cursor += 1
                self.buffer = self.buffer[:self.cursor] + "]" + self.buffer[self.cursor:]

            elif event.unicode:
                self.buffer = self.buffer[:self.cursor] + event.unicode + self.buffer[self.cursor:]
                self.cursor += 1

    def render(self, screen, pos, scale, color_text, color_highlight):
        self.surface = self.font.render(self.buffer, True, color_text)
        self.w, self.h = self.surface.get_size()
        screen.blit(pg.transform.smoothscale_by(self.surface, scale), pos)
        self.render_cursor(screen, pos, scale, color_highlight)

    def render_cursor(self, screen, pos, scale, color):
        if self.tick > 50:
            return
        w, h = self.font.render(self.buffer[:self.cursor], True, color).get_size()
        w *= scale
        h *= scale
        if not (0 <= self.cursor < len(self.buffer)):
            dw, dh = self.font.render(' ', True, color).get_size()
        else:
            dw, dh = self.font.render(self.buffer[self.cursor], True, color).get_size()
        dw *= scale
        dh *= scale
        surface_cursor = pg.Surface((dw, dh), pg.SRCALPHA)
        surface_cursor.fill(color)
        surface_cursor.set_alpha(60)
        screen.blit(surface_cursor, (pos[0] + w, pos[1]))

    def update(self, dt):
        self.tick += 1
        if self.tick > 100:
            self.tick = 0


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    font = pg.font.SysFont("Calibri", 24)
    editor = Editor(font, BINDING_EMACS)
    while True:
        screen.fill("#003333")
        for event in pg.event.get():
            editor.listen(event)
        editor.render(screen, (0, 0), 1, "#ffffff", "#ffffff")
        editor.update(0)
        pg.display.update()
