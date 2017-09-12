import pygame as py
from random import randint


P1CONTROLS = {"up": py.K_w, "down": py.K_s, "left": py.K_a, "right": py.K_d}
P2CONTROLS = {"up": py.K_UP, "down": py.K_DOWN, "left": py.K_LEFT, "right": py.K_RIGHT}


class Menu:

    def __init__(self):
        self.surface = py.Surface((640, 480))
        self.title_font = py.font.SysFont("timesnewroman", 48)
        self.m_font = py.font.SysFont("timesnewroman", 24)
        self.win_font = py.font.SysFont("timesnewroman", 36)

    def menu(self, surface):

        t = self.title_font.render("X-TREME PONG", True, (255, 0, 0))
        a = self.m_font.render("START", True, (255, 255, 255))
        b = self.m_font.render("START", True, (0, 0, 255))
        surface.blit(t, (320 - t.get_width()/2, 60))
        surface.blit(a, (320 - a.get_width()/2, 300))
        py.display.update()

        blink = True

        menu = True
        while menu:
            for event in py.event.get():
                if event.type == py.QUIT:
                    menu = False
                if event.type == py.KEYDOWN:
                    if event.key == py.K_RETURN:
                        menu = False
                if event.type == py.USEREVENT+1:
                    blink = not blink
                if event.type == py.KEYDOWN:
                    if event.key == py.K_F12:
                        if not surface.get_flags():
                            surface = py.display.set_mode((640, 480), py.FULLSCREEN)
                        else:
                            surface = py.display.set_mode((640, 480))
            surface.fill((0, 0, 0))
            surface.blit(t, (320 - t.get_width()/2, 60))
            if blink:
                surface.blit(a, (320 - a.get_width()/2, 300))
            else:
                surface.blit(b, (320 - a.get_width()/2, 300))
            py.display.update()

    def win(self, surface, p):

        t = self.title_font.render("X-TREME PONG", True, (255, 0, 0))
        a = self.m_font.render("REMATCH", True, (255, 255, 255))
        b = self.m_font.render("REMATCH", True, (0, 0, 255))

        if p == 1:
            w = self.win_font.render("Player 1 wins!", True, (255, 0, 0))
        else:
            w = self.win_font.render("Player 2 wins!", True, (0, 0, 255))

        surface.blit(t, (320 - t.get_width() / 2, 60))
        surface.blit(a, (320 - a.get_width() / 2, 300))

        py.display.update()

        blink = True

        menu = True
        while menu:
            for event in py.event.get():
                if event.type == py.QUIT:
                    menu = False
                if event.type == py.KEYDOWN:
                    if event.key == py.K_RETURN:
                        menu = False
                if event.type == py.USEREVENT + 1:
                    blink = not blink
                if event.type == py.KEYDOWN:
                    if event.key == py.K_F12:
                        if not surface.get_flags():
                            surface = py.display.set_mode((640, 480), py.FULLSCREEN)
                        else:
                            surface = py.display.set_mode((640, 480))
            surface.fill((0, 0, 0))
            surface.blit(t, (320 - t.get_width() / 2, 60))
            if blink:
                surface.blit(a, (320 - a.get_width() / 2, 300))
            else:
                surface.blit(b, (320 - a.get_width() / 2, 300))
            surface.blit(w, (320 - w.get_width() / 2, 250))
            py.display.update()



class Particle:

    def __init__(self, loc):
        self.rect = py.Rect((loc[0]-2, loc[1]-2), (4, 4))

        self.surface = py.Surface(self.rect.size, py.SRCALPHA)
        self.surface = self.surface.convert()
        self.surface.fill((255, 255, 0))

        self.opacity = 255

    def update(self):
        i = randint(0, 3)

        if i == 0:
            self.rect.x += 1
        elif i == 1:
            self.rect.x -=  1
        elif i == 2:
            self.rect.y += 1
        elif i == 3:
            self.rect.y -= 1

        self.opacity -= 5


class Player:

    def __init__(self, player):
        self.rect = py.Rect((0, 0), (24, 96))
        self.surface = py.Surface(self.rect.size)

        if player == 1:
            self.surface.fill((255, 0, 0))
            self.rect.x, self.rect.y = (20, 200)
            self.controls = P1CONTROLS
        else:  # Player 2
            self.surface.fill((0, 0, 255))
            self.rect.x, self.rect.y = (596, 200)
            self.controls = P2CONTROLS

        self.score = 0
        self.penalty = 2  # Game gets harder as you score more points

    def update(self):
        keys = py.key.get_pressed()

        if keys[self.controls["up"]]:  # Go up
            self.rect.y -= self.penalty
        if keys[self.controls["down"]]:  # Go down
            self.rect.y += self.penalty

        if self.rect.bottom > 480:
            self.rect.bottom = 480
        elif self.rect.top < 0:
            self.rect.top = 0

    def reset(self):
        self.score = 0
        self.penalty = 2


class Ball:

    def __init__(self, p1, p2, penalty_max):
        self.p1 = p1
        self.p2 = p2

        self.rect = py.Rect((32, 32), (16, 16))
        self.surface = py.Surface(self.rect.size)
        self.surface.set_colorkey(255)
        self.surface.fill(255)
        py.draw.circle(self.surface, (255, 255, 255), (8, 8), 8, 1)

        self.vx = 2
        self.vy = 2

        self.penalty_max = penalty_max
        self.pop = py.mixer.Sound("pop.wav")

    def update(self):

        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.colliderect(self.p1.rect):
            self.vx = self.p2.penalty
            self.pop.play(loops=0, maxtime=0, fade_ms=0)
            if self.rect.center[1] > self.p1.rect.center[1]:
                self.vy = abs(self.p2.penalty)
            else:
                self.vy = -abs(self.p2.penalty)

        elif self.rect.colliderect(self.p2.rect):
            self.vx = -self.p1.penalty
            self.pop.play(loops=0, maxtime=0, fade_ms=0)
            if self.rect.center[1] > self.p2.rect.center[1]:
                self.vy = abs(self.p1.penalty)
            else:
                self.vy = -abs(self.p1.penalty)

        if self.rect.y < 0:
            self.vy *= -1
            self.pop.play(loops=0, maxtime=0, fade_ms=0)
        elif self.rect.y > 464:
            self.vy *= -1
            self.pop.play(loops=0, maxtime=0, fade_ms=0)

        if self.rect.x < -16:
            self.p2.score += 1
            if self.p2.penalty != self.penalty_max:
                self.p2.penalty += 1
            self.reset(2)
        elif self.rect.x > 640:
            self.p1.score += 1
            if self.p1.penalty != self.penalty_max:
                self.p1.penalty += 1
            self.reset(1)

    def reset(self, winner):
        self.rect.y = 224

        if winner == 1:
            self.rect.x = 500
            self.vx = -2
            self.vy = 2
        else:
            self.rect.x = 140
            self.vx = 2
            self.vy = 2


class Pong:


    def __init__(self):
        self.screen = py.display.set_mode((640, 480))  # Init screen
        py.display.set_caption("Pong")
        self.clock = py.time.Clock()  # Init time clock

        py.init()
        py.mixer.init(frequency=22050, size=-16, channels=2, buffer=32)  # Decreased buffer because it lags
        py.mixer.music.load("song.mp3")
        py.mixer.music.play(-1)
        self.font = py.font.SysFont("timesnewroman", 24)

        self.GAME_TICK = py.USEREVENT + 1
        py.time.set_timer(self.GAME_TICK, 5)
        self.SECOND_TICK = py.USEREVENT + 2
        py.time.set_timer(self.SECOND_TICK, 1000)


        self.penalty_max = 5
        self.penalty_timer = 15  # 15 seconds

        self.p1 = Player(1)
        self.p2 = Player(2)
        self.ball = Ball(self.p1, self.p2, self.penalty_max)
        self.particles = []

        self.time = 0
        self.menu = Menu()

        self.app = True

    def run(self):
        self.menu.menu(self.screen)

        while self.app:
            self.clock.tick(60)
            self.event()
            self.draw()

    def event(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.app = False

            if event.type == self.GAME_TICK:
                self.update()
            if event.type == self.SECOND_TICK:
                self.time += 1
                if self.time%self.penalty_timer == 0:
                    if self.p1.penalty != self.penalty_max:
                        self.p1.penalty += 1
                    if self.p2.penalty != self.penalty_max:
                        self.p2.penalty += 1

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.app = False
                if event.key == py.K_F12:
                    if not self.screen.get_flags():
                        self.screen = py.display.set_mode((640, 480), py.FULLSCREEN)
                    else:
                        self.screen = py.display.set_mode((640, 480))

    def update(self):
        self.p1.update()
        self.p2.update()
        self.ball.update()
        self.particles.append(Particle(self.ball.rect.center))

        for part in self.particles:
            part.update()
            if part.opacity == 0:
                self.particles.remove(part)

        if self.p1.score == 5:
            self.menu.win(self.screen, 1)
            self.p1.reset()
            self.p2.reset()
            self.ball.reset(randint(1, 2))
            self.time = 0
        elif self.p2.score == 5:
            self.menu.win(self.screen, 2)
            self.p1.reset()
            self.p2.reset()
            self.ball.reset(randint(1, 2))
            self.time = 0

    def draw(self):
        self.screen.fill((0, 0, 0))

        for part in self.particles:
            self.screen.blit(part.surface, part.rect)

        self.screen.blit(self.p1.surface, self.p1.rect)
        self.screen.blit(self.p2.surface, self.p2.rect)
        self.screen.blit(self.ball.surface, self.ball.rect)


        sc = self.font.render("Score:"+str(self.p1.score), True, (255, 0, 0))
        self.screen.blit(sc, (140 - sc.get_rect().width/2, 20))
        sc = self.font.render("Score:"+str(self.p2.score), True, (0, 0, 255))
        self.screen.blit(sc, (500 - sc.get_rect().width/2, 20))
        sc = self.font.render(str(self.time), True, (255, 255, 255))
        self.screen.blit(sc, (320 - sc.get_rect().width/2, 20))

        py.display.update()


if __name__ == "__main__":
    p = Pong()
    p.run()
