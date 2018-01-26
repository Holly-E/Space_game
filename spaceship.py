# Spaceship Game
import simplegui
import math
import random

# globals for user interface
WIDTH = 900
HEIGHT = 700
score = 0
lives = 3
time = 0
a_missile = False

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def pos_update(pos, vel):
    inputs = {0: WIDTH,
              1: HEIGHT }

    for i in inputs:
        pos[i] = (pos[i] + vel[i]) % inputs[i]

# define classes
# Image Info class to load images
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, (self.image_center[0] * 3, self.image_center[1]), self.image_size, self.pos, (self.radius * 2, self.radius * 2), self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, (self.radius * 2, self.radius * 2), self.angle)

    def update(self):
        # change ship direction
        self.angle += self.angle_vel

        # accelerate ship
        accel_const = .7
        self.forward = angle_to_vector(self.angle)
        if self.thrust:
            ship_thrust_sound.play()
            self.vel[0] += self.forward[0] * accel_const
            self.vel[1] += self.forward[1] * accel_const
        else:
            ship_thrust_sound.rewind()
            ship_thrust_sound.pause()

        # account for friction
        friction_const = .03
        self.vel[0] *= (1 - friction_const)
        self.vel[1] *= (1 - friction_const)

        # position update
        pos_update(self.pos, self.vel)

    def shoot(self):
        global a_missile
        missile_pos = [(self.pos[0] + self.radius * self.forward[0]), (self.pos[1] + self.radius * self.forward[1])]
        missile_vel = [(self.vel[0] + self.forward[0] * 8), (self.vel[1] + self.forward[1] * 8)]
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, (self.radius * 2, self.radius * 2), self.angle)

    def update(self):
        # change sprite direction
        self.angle += self.angle_vel

        # position update
        pos_update(self.pos, self.vel)

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
def art_assets():
    global debris_info, debris_image, nebula_info, nebula_image, splash_info, splash_image, ship_info, ship_image, missile_info, missile_image
    global asteroid_info, asteroid_image, explosion_info, explosion_image, soundtrack, missile_sound, ship_thrust_sound, explosion_sound
    # debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
    #                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
    debris_info = ImageInfo([320, 240], [640, 480])
    debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

    # nebula images - nebula_brown.png, nebula_blue.png
    nebula_info = ImageInfo([400, 300], [800, 600])
    nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

    # splash image
    splash_info = ImageInfo([200, 150], [400, 300])
    splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

    # ship image
    ship_info = ImageInfo([45, 45], [90, 90], 40)
    ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

    # missile image - shot1.png, shot2.png, shot3.png
    missile_info = ImageInfo([5,5], [10, 10], 3, 50)
    missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

    # asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
    asteroid_info = ImageInfo([45, 45], [90, 90], 60)
    asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

    # animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
    explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
    explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

    # sound assets purchased from sounddogs.com, please do not redistribute
    # alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
    # please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
    #soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")
    soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
    missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
    missile_sound.set_volume(.5)
    ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
    explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# define event handlers
def draw(canvas):
    global time, WIDTH, HEIGHT

    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    if a_missile:
        a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    if a_missile:
        a_missile.update()

    # draw score and lives
    # pink rgb(241, 27, 215)  lt_purple #C0B9F5 ship_blue #5085B9
    canvas.draw_text("Score: " + str(score), (WIDTH * .75, HEIGHT * .08), 30, '#3C19EA', 'monospace')
    canvas.draw_text("Lives: " + str(lives), (WIDTH * .07, HEIGHT * .08), 30, '#DEDDE3', 'monospace')

# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    a_rock = Sprite([random.randint(0, WIDTH), random.randint(0, HEIGHT)], [random.randint(-7, 7), random.randint(-3, 3)], random.randint(0, 360), (random.randint(-15, 15) / 100.0), asteroid_image, asteroid_info)

# keydown handler
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel += -.05
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel += .05
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = True
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

# keyup handler
def keyup(key):

    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = False

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and one sprite
art_assets()
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
