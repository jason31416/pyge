import pygame as pygame
import time
import random
from typing import Dict

Surface = pygame.Surface

class Picture:
    x = 0
    y = 0
    def __init__(self, pic: pygame.Surface, x = 0, y = 0):
        self.pic = pic
        self.x = x
        self.y = y
        self.name = "unnamed"
        self.setup()

    def setup(self):
        pass

    def move(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.name

    def set_size(self, w, h):
        self.pic = pygame.transform.scale(self.pic, (w, h))
        return self

    def set_angle(self, angle):
        self.pic = pygame.transform.rotate(self.pic, angle)
        return self

    def set_surface(self, surf):
        self.pic = surf
        return self

    def collide(self, opic = None):
        if opic is None:
            return self.pic.get_rect().move(self.x, self.y).collidepoint(pygame.mouse.get_pos())
        elif isinstance(opic, Picture):
            return self.pic.get_rect().move(self.x, self.y).colliderect(opic.pic.get_rect().move(opic.x, opic.y))
        elif type(opic) == pygame.Rect:
            return self.pic.get_rect().move(self.x, self.y).colliderect(opic)
        elif type(opic) == tuple:
            return self.pic.get_rect().move(self.x, self.y).collidepoint(opic)

    def draw(self, gm):
        gm.sc.blit(self.pic, (self.x, self.y))

    def update(self, gm):
        pass

class music:
    def __init__(self, file):
        self.file = file
        self.music = pygame.mixer.Sound(file)

    def play(self):
        self.music.play()

    def play_forever(self):
        self.music.play(-1)

    def stop(self):
        self.music.stop()

    @property
    def volume(self):
        return self.music.get_volume()

    @volume.setter
    def volume(self, vol):
        self.music.set_volume(vol)

def random_str(length: int) -> str:
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz123456789") for _ in range(length))

class Game:
    def __init__(self, sc: pygame.Surface = None):
        pygame.init()
        if sc is None:
            self.sc = pygame.display.set_mode((800, 600))
            self.scsetup()
        else:
            self.sc = sc
        self.running = True
        self.events = []
        self.keys = []
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_click = pygame.mouse.get_pressed()
        self.tick = 0
        self.tick_rate = 20
        self.all_objs: Dict[str, Dict[str, Picture]] = {"main": {}}
        self.use_threading = False
        self.now_page = "main"
        self.all_events = ["QUIT", "KEYDOWN", "KEYUP", "MOUSEMOTION", "MOUSEBUTTONDOWN"]
        self.evlistener = {}
        self.is_event_active = {}
        for i in self.all_events:
            self.evlistener[i] = []
            self.is_event_active[i] = False
        self.add_event_listener("QUIT", self.quit)
        self.setup()

    def scsetup(self):
        pass

    def setup(self):
        pass

    def update_back(self):
        pass

    def update_front(self):
        pass

    def add_event(self, event):
        self.all_events.append(event)
        self.evlistener[event] = []
        self.is_event_active[event] = False

    def catch_event(self, event):
        self.is_event_active[event] = False

    def active_event(self, event):
        self.is_event_active[event] = True

    def add_event_listener(self, event, func):
        self.evlistener[event].append(func)

    def remove_event_listener(self, event, func):
        self.evlistener[event].remove(func)

    def add_obj(self, obj: Picture, name: str = None, page: str = None):
        if name == "unnamed":
            raise NameError("Name cannot be 'unnamed'")
        if page is None:
            page = self.now_page
        if name is None:
            name = random_str(20)
        obj.name = name
        self.all_objs[page][name] = obj

    set_obj = add_obj

    def rem_obj(self, name: str, page: str = None):
        if name == "unnamed":
            raise NameError("Name cannot be 'unnamed'")
        if page is None:
            page = self.now_page
        if name in self.all_objs[page].keys():
            self.all_objs[page].pop(name)

    def get_obj(self, name: str, page: str = None):
        if page is None:
            page = self.now_page
        if name in self.all_objs[page].keys():
            return self.all_objs[page][name]
        else:
            raise KeyError("Object not found")

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def quit(self, gm):
        self.running = False
        pygame.quit()

    def draw_text(self, text, x, y, size = 24, font = None, color = (255, 255, 255)):
        ft = pygame.font.Font(font, size)
        txt = ft.render(text, True, color)
        self.sc.blit(txt, (x, y))

    def add_page(self, page):
        self.all_objs[page] = {}

    def get_current_page_objs(self):
        return self.all_objs[self.now_page]

    def set_page(self, page):
        self.now_page = page

    def run(self):
        while self.running:
            self.sc.fill((0, 0, 0))
            ticktime = time.time()
            self.events = pygame.event.get()
            self.keys = pygame.key.get_pressed()
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_click = pygame.mouse.get_pressed()
            self.update_back()
            ks = list(self.all_objs[self.now_page].keys())
            for i in ks:
                if i not in self.all_objs[self.now_page].keys():
                    continue
                if not self.use_threading:
                    self.all_objs[self.now_page][i].draw(self)
                self.all_objs[self.now_page][i].update(self)
            for ev in self.events:
                if ev.type == pygame.QUIT:
                    self.active_event("QUIT")
                if ev.type == pygame.KEYDOWN:
                    self.active_event("KEYDOWN")
                if ev.type == pygame.KEYUP:
                    self.active_event("KEYUP")
            if self.mouse_click[0]:
                self.active_event("MOUSEBUTTONDOWN")
            self.update_front()
            for i in self.all_events:
                if self.is_event_active[i]:
                    for j in self.evlistener[i]:
                        j(self)
            if self.running:
                pygame.display.update()
                while ticktime + 1/self.tick_rate > time.time():
                    time.sleep(0.001)
                self.tick += 1

# objs:

class Text(Picture):
    def __init__(self, text, font = None, fontsz = 24, color = (0, 0, 0), x=0, y=0):
        ft = pygame.font.Font(font, fontsz)
        super().__init__(ft.render(text, True, color), x, y)
        self.font = ft
        self.color = color
        self._text = text

    @property
    def text(self):
        return self.text

    @text.setter
    def text(self, text):
        self._text = text
        print(self.__dict__)
        self.pic = self.font.render(text, True, self.color)


# funcs:

def load_img(path: str, size=None):
    img = pygame.image.load(path)
    if size is not None:
        img = pygame.transform.scale(img, size)
    return img

def rect(w, h, color=(0, 0, 0)):
    sf = pygame.Surface((w, h))
    sf.fill(color)
    return sf