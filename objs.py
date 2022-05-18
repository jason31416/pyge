import pyge
import pyge.game as game
import time
import pygame
import pyperclip
import time

class Button(game.Picture):
    def __init__(self, sf: game.Surface, onclick, x=0, y=0):
        super().__init__(sf, x, y)
        self.onclick = onclick

    def update(self, gm):
        if self.collide():
            if gm.mouse_click[0]:
                self.onclick()

class Switch(game.Picture):
    def __init__(self, x=0, y=0, fgclr = (255,255,255), onclr = (0,255,0), offclr = (255,0,0)):
        sf = game.Surface((40, 20))
        sf.fill(offclr)
        sf2 = game.Surface((18, 18))
        sf2.fill(fgclr)
        sf.blit(sf2, (1, 1))
        self.onclr = onclr
        self.offclr = offclr
        self.fgclr = fgclr
        super().__init__(sf, x, y)
        self.on = False
        self.lstclick = 0

    def update(self, gm: game.Game):
        if self.collide() and gm.mouse_click[0] and time.time() - self.lstclick > 0.4:
            self.on = not self.on
            self.pic.fill(self.onclr if self.on else self.offclr)
            sf2 = game.Surface((18, 18))
            sf2.fill(self.fgclr)
            self.pic.blit(sf2, ((1, 1) if not self.on else (21, 1)))
            self.lstclick = time.time()

class TextBox(game.Picture):
    def __init__(self, x=0, y=0):
        super().__init__(game.Surface((50, 20)), x, y)
        self.text = ""
        self.curser_on = False
        self.focus = False
        self.lst_input = ""
        self.fm_input = -1
        self.clr = (255, 255, 255)
        self.font = None
        self.size = 24
        self.sz = [0, 0]
        self.lst_input_tick = 0
        self.ref_tick = 2
        self.ref_tick_cont = 1
        self.lst_ipt = ""
        self.md = True
        self.show_max = 20
    def update(self, gm: game.Game):
        if self.text.count("\n") > self.show_max:
            self.text = "\n".join(self.text.split("\n")[-self.show_max:])
        if gm.mouse_click[0]:
            self.focus = self.get_click()
        if self.focus and self.curser_on and (gm.tick-self.lst_input_tick>self.ref_tick or (self.md and gm.tick-self.lst_input_tick>self.ref_tick_cont)):
            if (gm.keys[pygame.K_RMETA] or gm.keys[pygame.K_LMETA]) and gm.keys[pygame.K_v]:
                self.text += pyperclip.paste()
                self.lst_input_tick = gm.tick+3
                return
            if gm.keys[pygame.K_BACKSPACE] and len(self.text)>self.fm_input and (gm.tick-self.lst_input_tick>self.ref_tick+1 or (self.md and gm.tick-self.lst_input_tick>self.ref_tick_cont+1)):
                self.text = self.text[:-1]
                self.lst_input_tick = gm.tick
                if self.lst_ipt == "backspace":
                    self.md = True
                else:
                    self.md = False
                self.lst_ipt = "backspace"
            with_shift = {'1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"', ',': '<', '.': '>', '/': '?'}
            for i in list(range(ord('a'), ord('z')+1))+list(range(ord('0'), ord('9')+1))+[pygame.K_SPACE, pygame.K_QUOTE, pygame.K_BACKSLASH, pygame.K_SLASH, pygame.K_COMMA, pygame.K_COLON, pygame.K_PERIOD]:
                if gm.keys[i]:
                    if gm.keys[pygame.K_LSHIFT] or gm.keys[pygame.K_RSHIFT]:
                        self.text += with_shift[chr(i)]
                    else:
                        self.text += chr(i)
                    self.lst_input_tick = gm.tick
                    if self.lst_ipt == (with_shift[chr(i)] if gm.keys[pygame.K_LSHIFT] or gm.keys[pygame.K_RSHIFT] else chr(i)):
                        self.md = True
                    else:
                        self.md = False
                    self.lst_ipt = chr(i)
            if gm.keys[pygame.K_RETURN]:
                self.lst_input = self.text[self.fm_input:]
                self.text += "\n"
                self.curser_on = False
                if self.lst_ipt == "\n":
                    self.md = True
                else:
                    self.md = False
                self.lst_input_tick = gm.tick+3
                self.lst_ipt = "\n"
    def allow_input(self):
        self.fm_input = len(self.text)
        self.curser_on = True
    def get_input(self):
        return self.lst_input
    def get_text(self):
        return self.text
    def set_text(self, text):
        self.text = text
    def clear(self):
        self.text = ""
    def print(self, txt, end="\n"):
        self.text+=txt+end
    def get_click(self):
        if pyge.pygame.Rect(self.x, self.y, self.sz[0], self.sz[1]).collidepoint(pyge.pygame.mouse.get_pos()):
            return True
        return False
    def draw(self, gm: game.Game):
        txtd = self.text
        self.sz = [0, 0]
        if self.curser_on and gm.tick%10<5 and self.focus:
            txtd += "_"
        yy = self.y
        for i in txtd.split("\n"):
            t = gm.draw_text(i, self.x, yy, color=self.clr, size=self.size, font=self.font)
            yy += self.size+3
            self.sz[0] = max(self.sz[0], t.get_width())
        self.sz[1] = yy
