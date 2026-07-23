"""
poop = regain health
dog bone kills chocolate
chocolate kills dog
eat treats to be able to poop

show stats: health, chocolates eaten, treats eaten, amount of times pooped

should probably disallow going outside of border whenever learned

bone bounce back
"""


import pygame
from random import randint, uniform
import time
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("C:/Users/Mikec/PycharmProjects/PythonProjects/Game_Dev/Doggy", "5100114.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (WIDTH/2,HEIGHT/2))
        self.dir = pygame.Vector2()
        self.speed = 300
        self.rotation = 0

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # cooldown
        self.can_bark = True
        self.bark_time = 0
        self.cd_dur = 1000

    def bark_timer(self):
        if not self.can_bark:
            current_time = pygame.time.get_ticks() # time since game start or time since "pygame.init()"
            if current_time - self.bark_time >= self.cd_dur:
                self.can_bark = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.dir.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.dir = self.dir.normalize() if self.dir else self.dir
        self.rect.center += self.dir * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_bark:
            midtop_x, midtop_y = self.rect.midtop
            midtop_y += bone_correction
            Bone(bone_surf, (midtop_x, midtop_y), (all_sprites, bone_sprites))
            self.can_bark = False
            self.bark_time = pygame.time.get_ticks()

        self.bark_timer()

class Flower(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WIDTH), randint(0, HEIGHT)))
        self.rotation = 0

class Bone(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(midtop = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation = 0

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.top < -125:
            self.kill()

        # rotation
        self.rotation += 250 * dt
        self.image = pygame.transform.rotate(self.original_surf, self.rotation)
        self.rect = self.image.get_frect(center = self.rect.center)
        
class Food(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.dir = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.center += self.dir * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime: # better to just check when below the floor
            self.kill()

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.image = frames
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        pygame.time.delay(25)
        self.kill()

def collisions():
    global running

    chocolate_collisions =  pygame.sprite.spritecollide(player, food_sprites, True, pygame.sprite.collide_mask)
    if chocolate_collisions:
        print(chocolate_collisions[0])
        running = False
        
    for bone in bone_sprites:
        bone_collisions = pygame.sprite.spritecollide(bone, food_sprites, True)
        if bone_collisions:
            bone.kill()
            AnimatedExplosion(explosion_frames, bone.rect.midtop, all_sprites)

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (240, 240, 240))
    text_rect = text_surf.get_frect(midbottom = (WIDTH / 2, HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240, 240,  240), text_rect.inflate(20, 15).move(0, -3), 5, 10)

# setup
pygame.init()

WIDTH = 1280
HEIGHT = 720
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# import
flower_surf = pygame.image.load(join("C:/Users/Mikec/PycharmProjects/PythonProjects/Game_Dev/Doggy/flower.png")).convert_alpha()
# food_surf = pygame.image.load(join("C:/Users/Mikec/PycharmProjects/PythonProjects/Game_Dev/Doggy", "dogtreat.png")).convert_alpha()
food_surf = pygame.image.load(join("C:/Users/Mikec/PycharmProjects/PythonProjects/Game_Dev/Doggy", "chocolate.png")).convert_alpha()
bone_surf = pygame.image.load(join("C:/Users/Mikec/PycharmProjects/PythonProjects/Game_Dev/Doggy", "bone.png")).convert_alpha()
explosion_frames = pygame.image.load(join("C:/Users/Mikec/PycharmProjects/PythonProjects/Game_Dev/Doggy/explosion.png")).convert_alpha() # use list comprhension for multiple frames
print(explosion_frames)
font = pygame.font.Font(None, 50)

bone_surf = pygame.transform.scale(bone_surf, (500, 500)) # scales down dogtreat image
bone_correction = -100
food_surf = pygame.transform.scale(food_surf, (150, 150)) # scales down dogtreat image
explosion_frames = pygame.transform.scale(explosion_frames, (300, 300)) # scales down dogtreat image

# sprites
all_sprites = pygame.sprite.Group()
food_sprites = pygame.sprite.Group()
bone_sprites = pygame.sprite.Group()
flower_surf = pygame.transform.scale(flower_surf, (50,50))
for i in range(25):
    Flower(all_sprites, flower_surf)
player = Player(all_sprites)

# importing images
player_surf = pygame.image.load(join("C:/Users/Mikec/PycharmProjects/PythonProjects/Game_Dev/Doggy", "5100114.png")).convert_alpha()

# rect
player_rect =  player_surf.get_frect(center = (WIDTH/2,HEIGHT/2))

player_dir = pygame.math.Vector2()

running = True
clock = pygame.time.Clock()

# custom events -> dogtreat event
food_event = pygame.event.custom_type()
pygame.time.set_timer(food_event, 1000)

while running:
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == food_event:
            x, y = randint(50, WIDTH - 50), -100
            Food(food_surf, (x, y), (all_sprites, food_sprites))

    # update
    all_sprites.update(dt)
    collisions()
        
    # draw game
    display_surface.fill('#008000')
    all_sprites.draw(display_surface)
    display_score()


    pygame.display.update()
 
pygame.quit()