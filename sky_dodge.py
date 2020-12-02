import pygame
import random
import time

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # pohyb hráče
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

    # objekt zůstane na obrazovce
        if self.rect.left < 0:
            self.rect.left =0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top =0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        if Time.bool == False:
            self.rect.move_ip(-self.speed, 0)
        else:
            self.rect.move_ip(-self.speed/3, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        if Time.bool == False:
            self.rect.move_ip(-5, 0)
        else:
            self.rect.move_ip(-5/3, 0)
        if self.rect.right < 0:
            self.kill()

class Time(pygame.sprite.Sprite):
    bool = False
    def __init__(self):
        super(Time, self).__init__()
        self.surf = pygame.image.load("images/time.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        if Time.bool == False:
            self.rect.move_ip(-3, 0)
        else:
            self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()
        if pygame.sprite.spritecollideany(player, hours):
            clock_pickup_sound.play()
            Time.bool = True
            self.kill()

    
pygame.mixer.init()

pygame.init()
pygame.font.init()

text = pygame.font.SysFont('Arial', 15) ###############
surv= pygame.font.SysFont('Arial', 15) ###############


clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

score_count = 0
survival_time = 0

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

ADDSCORE = pygame.USEREVENT + 3
pygame.time.set_timer(ADDSCORE, 4000)

ADDTIME = pygame.USEREVENT + 4
pygame.time.set_timer(ADDTIME, 7000)

CHECKTIME = pygame.USEREVENT + 5
pygame.time.set_timer(CHECKTIME, 6999)

player = Player()

hours = pygame.sprite.Group()
clouds = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# sound source: Chris Bailey - artist Tripnet
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("sound/Sky_dodge_theme.ogg")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.4)

# sound sources: Chris Bailey - artist Tripnet
move_up_sound = pygame.mixer.Sound("sound/Jet_up.ogg")
move_down_sound = pygame.mixer.Sound("sound/Jet_down.ogg")
collision_sound = pygame.mixer.Sound("sound/Boom.ogg")


clock_pickup_sound = pygame.mixer.Sound("sound/Small_bell.mp3")

move_up_sound.set_volume(0.2)
move_down_sound.set_volume(0.2)
collision_sound.set_volume(1.0)
clock_pickup_sound.set_volume(1.1)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
            survival_time += 1
 
        elif event.type == ADDSCORE:
            score_count += 100
        
        elif event.type == ADDTIME:
            new_time = Time()
            hours.add(new_time)
            all_sprites.add(new_time)
        
        elif event.type == CHECKTIME:
            Time.bool = False

        

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    enemies.update()
    clouds.update()
    hours.update()

    textscore = text.render(f'Score: {score_count}', True, (0, 0, 0)) ###########
    textsurvival = surv.render(f'Time: {survival_time} seconds', True, (0, 0, 0)) ###########

    screen.fill((26, 68, 133))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        screen.blit(textscore,(10,20))
        screen.blit(textsurvival,(10,0))
    # collision check
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

        move_down_sound.stop()
        move_up_sound.stop()
        pygame.mixer.music.stop()
        pygame.time.delay(50)
        collision_sound.play()
        pygame.time.delay(500)
        running = False


    pygame.display.flip()

    clock.tick(45)

pygame.mixer.quit()