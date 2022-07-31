import pygame
import os
import time
import random
pygame.init()
pygame.font.init()

w, h = 2000, 1500
# pygame surface
WIN = pygame.display.set_mode((w, h))
pygame.display.set_caption("Space Shooter")

# load imagsgsggsggss
redspa = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png")), (135, 135))
greenspa = pygame.transform.scale(pygame.image.load(os.path.join(
    "assets", "pixel_ship_green_small.png")), (130, 130))
bluspa = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png")), (120, 120))

# playaa
yelspa = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow.png")), (200, 200))

# lazers
redspall = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "pixel_laser_red.png")), (150, 150))
greenspall = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png")), (150, 150))
bluspall = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "pixel_laser_blue.png")), (150, 150))

# plalasa
yelspall = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# background
bgawww = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (w, h))


def collide(obj2, obj1):
    # mask helps compiler determine if 2 objects' PIXELS
    # have actually overlapped or its transparent border
    # in case of the latter, it's NOT collision
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


class laserz:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def offscreen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class ship():
    # enemy ships, player ship
    cooldown = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        # wait a while brfore shoting another laser

    def draw(self, window):
        #pygame.draw.rect(window, (255,0,0), (self.x, self.y, 150, 150), 0)
        window.blit(self.ship_img, (self.x, self.y))
        for las in self.lasers:
            las.draw(window)

    def movelas(self, vel, objs):
        self.cooldownz()
        for las in self.lasers:
            las.move(vel)
            if las.offscreen(h):
                self.lasers.remove(las)
            elif las.collision(objs):
                objs.health -= 20
                self.lasers.remove(las)

    def cooldownz(self):
        if self.cool_down_counter >= self.cooldown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = laserz(self.x + 40, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class playa(ship):  # inheritance
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.ship_img = yelspa
        self.laser_img = yelspall
        self.mask = pygame.mask.from_surface(
            self.ship_img)  # mask - pixel perfect collision
        self.max_hel = health

    def getw(self):
        return self.ship_img.get_width()

    def geth(self):
        return self.ship_img.get_height()

    def movelas(self, vel, objsen):
        self.cooldownz()
        for las in self.lasers:
            las.move(vel)
            if las.offscreen(h):
                self.lasers.remove(las)
            else:
                for objs in objsen:
                    if las.collision(objs):
                        objsen.remove(objs)
                        if las in self.lasers:
                            self.lasers.remove(las)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                         self.ship_img.get_height()+40, self.ship_img.get_width(), 25))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() +
                         40, self.ship_img.get_width()*(self.health/self.max_hel), 25))


class enem(ship):
    col_map = {
        "red": (redspa, redspall), "blue": (bluspa, bluspall),
        "green": (greenspa, greenspall)
    }

    def __init__(self, x, y, color,  health=100):
        super().__init__(x, y, health=health)
        self.ship_img, self.laser_img = self.col_map[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = laserz(self.x - 10, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def main():
    run = True
    fps = 60
    # checking for collision and shiz
    # 60 times every second
    lvl = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 100)
    lost_font = pygame.font.SysFont("comicsans", 200)
    sh1 = playa(900, 1180)
    enemies = []  # stores position of enemy shipz
    wavelength = 0
    enm_vel = 5
    lost = False
    lost_count = 0
    laser_vel = 15
    clock = pygame.time.Clock()

    def redraw_window():
        # handles all drawying
        # redraw every frame
        WIN.blit(bgawww, (0, 0))
        # pygame coordinates ~ opencv coords
        # draw test
        level_label = main_font.render(f"Level: {lvl}", 1, (255, 255, 0))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 0, 0))

        WIN.blit(lives_label, (50, 50))
        WIN.blit(level_label, (w - lives_label.get_width()-50, 50))
        sh1.draw(WIN)  # WIN - window

        for en in enemies:
            en.draw(WIN)
        if lost == True:
            lost_label = lost_font.render(f"LOST!!!!", 1, (0, 255, 255), 0)
            WIN.blit(lost_label, (650, 700))

        pygame.display.update()

    while run:
        clock.tick(fps)
        # makes sure i game stays consistent
        # at same speed in every system
        redraw_window()

        if(lives <= 0 or sh1.health <= 0):
            lost = True
            lost_count += 1
            wavelength = 0

        if lost:
            if lost_count > fps:
                run = False
        if len(enemies) == 0 and lost == False:
            lvl += 1
            wavelength += 5
            # creating enemies
            for i in range(wavelength):
                enemy = enem(random.randrange(
                    300, w-300), random.randrange(-300*lvl, -100), random.choice(["red", "green", "blue"]))
                enemies.append(enemy)

        # checking for event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # if event.type == pygame.KEYDOWN
        # tracking keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and sh1.x - 20 > 0:  # left
            sh1.x -= 20
        if keys[pygame.K_d] and sh1.x + 20 + sh1.getw() < w:  # right
            sh1.x += 20
        if keys[pygame.K_w] and sh1.y - 20 > 0:  # up
            sh1.y -= 20
        if keys[pygame.K_s] and sh1.y + 20 + sh1.geth() + 10 < h:  # down
            sh1.y += 20
        if keys[pygame.K_SPACE]:
            sh1.shoot()

        for enemy in enemies:
            enemy.move(enm_vel)
            enemy.movelas(laser_vel, sh1)

            if random.randrange(0, 120) == 1:
                enemy.shoot()
            if(collide(enemy, sh1)):  # collision
                sh1.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.ship_img.get_height() > h:  # else off screen
                lives -= 1
                enemies.remove(enemy)

        sh1.movelas(-laser_vel, enemies)


def mainmenu():  # main menuuuuu
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(bgawww, (0, 0))
        title_label = title_font.render(
            "Press the mouse to begin... ^_^", 1, (234, 121, 50))
        WIN.blit(title_label, (w/2 - title_label.get_width()/2, h/2))
        pygame.display.update()
        for vent in pygame.event.get():
            if vent.type == pygame.QUIT:
                run = False
            if vent.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


mainmenu()
