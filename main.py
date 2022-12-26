import pygame
import os
import math
import random

PURPLE = (100,88,132)
BLACK = (0,0,0)

FPS = 60
VEL = 3

PLAYER_WIDTH, PLAYER_HEIGHT = 62,50
ZOMBIE_WIDTH, ZOMBIE_HEIGHT = 50, 50
GUN_WIDTH, GUN_HEIGHT = 10, 4



class Player(pygame.sprite.Sprite):
    def __init__(self, width, height,pos_x,pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join('Biker Idle', 'tile000.png')))
        self.sprites.append(pygame.image.load(os.path.join('Biker Idle', 'tile001.png')))
        self.sprites.append(pygame.image.load(os.path.join('Biker Idle', 'tile002.png')))
        self.sprites.append(pygame.image.load(os.path.join('Biker Idle', 'tile003.png')))
        
        self.move_sprite = []
        self.move_sprite.append(pygame.image.load(os.path.join('Biker Run', 'tile000.png')))
        self.move_sprite.append(pygame.image.load(os.path.join('Biker Run', 'tile001.png')))
        self.move_sprite.append(pygame.image.load(os.path.join('Biker Run', 'tile002.png')))
        self.move_sprite.append(pygame.image.load(os.path.join('Biker Run', 'tile003.png')))
        self.move_sprite.append(pygame.image.load(os.path.join('Biker Run', 'tile004.png')))
        self.move_sprite.append(pygame.image.load(os.path.join('Biker Run', 'tile005.png')))

        self.current_sprite = 0
        self.current_move_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.image = pygame.transform.scale(self.image,(height,width))
        self.orig_image =self.image
        self.rect = self.image.get_rect(center=(pos_x,pos_y))
        self.direction = "right"

        self.moving = False
    def update(self, keys_pressed):
        self.moving = False
        self.current_sprite +=0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        
        if self.direction == "left":
                self.image = pygame.transform.flip(self.sprites[int(self.current_sprite)], True, False)
        else:
            self.image = self.sprites[int(self.current_sprite)]
        
        
        if keys_pressed[pygame.K_w] and self.rect.y - VEL > 0: #move forwawrd
            self.rect.y  -= VEL
            if self.direction == "left":
                self.image = pygame.transform.flip(self.move_sprite[int(self.current_move_sprite)], True, False)
            else:
                self.image = self.move_sprite[int(self.current_move_sprite)]
            self.current_move_sprite +=0.1
            
            if self.current_move_sprite >= len(self.move_sprite):
                self.current_move_sprite = 0   
            self.moving = True

        if keys_pressed[pygame.K_a] and self.rect.x - VEL > 0: #move left
            self.rect.x  -= VEL
            self.image = pygame.transform.flip(self.move_sprite[int(self.current_move_sprite)], True, False)
            self.direction = "left"
            self.current_move_sprite +=0.1
            if self.current_move_sprite >= len(self.move_sprite):
                self.current_move_sprite = 0   
            self.moving = True

        if keys_pressed[pygame.K_s] and self.rect.y + VEL + self.rect.height < HEIGHT - 18: #move back
            self.rect.y   += VEL
            if self.direction == "left":
                self.image = pygame.transform.flip(self.move_sprite[int(self.current_move_sprite)], True, False)
            else:
                self.image = self.move_sprite[int(self.current_move_sprite)]
            self.current_move_sprite +=0.1
            if self.current_move_sprite >= len(self.move_sprite):
                self.current_move_sprite = 0
            self.moving = True

        if keys_pressed[pygame.K_d] and self.rect.x + VEL + self.rect.width < WIDTH: #move right
            self.rect.x  += VEL
            self.image = self.move_sprite[int(self.current_move_sprite)]
            self.direction = "right"
            self.current_move_sprite +=0.1
            if self.current_move_sprite >= len(self.move_sprite):
                self.current_move_sprite = 0
            self.moving = True
        
player = Player(PLAYER_HEIGHT, PLAYER_WIDTH, 300, 100)
player_group = pygame.sprite.Group()
player_group.add(player)           

class Gun(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('guns', '2 Guns','8_1.png'))
        self.orig_image = self.image
        self.flip_orig_image = pygame.transform.flip(self.orig_image, False, True)
        self.rect = self.image.get_rect(center=(pos_x,pos_y))

    def update(self):
        
        if player.moving == False:
            self.image = self.orig_image.set_alpha(0)
            print("not moving")
        else:
            x_mouse = pygame.mouse.get_pos()[0]
            y_mouse = pygame.mouse.get_pos()[1]
            x_diff = self.rect.x - x_mouse
            y_diff = self.rect.y-y_mouse
            
            angle = math.degrees(math.atan2(-y_diff, x_diff)) - 180
            if player.direction == 'left':
                self.image = pygame.transform.rotate(self.flip_orig_image, angle)
            else:
                self.image = pygame.transform.rotate(self.orig_image, angle)

        self.rect = self.image.get_rect(center=player.rect.center)

        # if player.direction == 'left':
        #     self.image = pygame.transform.flip(self.image, False, True)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x ,pos_y, targetx, targety):
        super().__init__()
        self.image = pygame.image.load(os.path.join('guns', '5 Bullets', '8.png'))
        self.rect =self.image.get_rect(center = (pos_x,pos_y))
        angle = math.atan2(targety-pos_y, targetx-pos_x)
        self.dx = math.cos(angle)*7
        self.dy = math.sin(angle)*7
        
        self.x = pos_x
        self.y = pos_y
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
            
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        


zombie_group = pygame.sprite.Group()

class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('zombiefiles', 'male', 'Idle (1).png')) 
        self.image = pygame.transform.scale(self.image, (ZOMBIE_HEIGHT,ZOMBIE_WIDTH))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(pos_x,pos_y))

        self.x = pos_x
        self.y = pos_y
        if self.rect.x < player.rect.x:
            self.location = 'left'
        else:
            self.location = 'right'
    def update(self, target_x, target_y):
       
        if self.location != player.direction:
            angle = math.atan2(target_y-self.y, target_x-self.x)
            self.dx = math.cos(angle)*.5
            self.dy = math.sin(angle)*.5
            if self.dx < 0:
                self.image = pygame.transform.flip(self.orig_image, True, False)
            elif self.dx>0:
                self.image = self.orig_image
            self.x += self.dx
            self.y += self.dy
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

        if self.rect.x < player.rect.x:
            self.location = 'left'
        else:
            self.location = 'right'
    

WIDTH, HEIGHT = 500,500

sides = ['top', 'bottom', 'left', 'right']

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apocalypse Rerising")



CROSSHAIR_IMAGE = pygame.image.load(
    os.path.join('crosshair.png'))

cursor_rect = CROSSHAIR_IMAGE.get_rect()



gun = Gun(300, 100) 
gun_group = pygame.sprite.Group()
gun_group.add(gun)

bullet_group = pygame.sprite.Group()


def draw_window():
    WIN.fill(PURPLE)
    pygame.draw.rect(WIN, BLACK, (0, 0, WIDTH, HEIGHT), 10 )
    player_group.draw(WIN)
    gun_group.draw(WIN)
    bullet_group.draw(WIN)
    zombie_group.draw(WIN)
    WIN.blit(CROSSHAIR_IMAGE, cursor_rect)
    pygame.display.update()


def main():

    bullets = []

    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    run = True
    while run:
        cursor_rect.center = pygame.mouse.get_pos()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x_diff = player.rect.x - mx
                y_diff = player.rect.y-my
                
                angle = math.degrees(math.atan2(-y_diff, x_diff)) +180
                if (player.direction == "right" and (angle <=90 or angle >= 270)) or (player.direction == "left" and 90 < angle <270):
                    bullet_group.add(Bullet(gun.rect.centerx, gun.rect.centery ,mx,my))
                    

                
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_z]:
            side = random.choice(sides)
            if side == 'top':
                zy = 0
                zx = random.randrange(WIDTH)
            elif side == 'bottom':
                zy = HEIGHT
                zx =random.randrange(WIDTH)
            elif side == 'left':
                zy = random.randrange(HEIGHT)
                zx = 0
            elif side == 'right':
                zy = random.randrange(HEIGHT)
                zx = WIDTH
            zombie_group.add(Zombie(zx, zy))


        player_group.update(keys_pressed)
        gun_group.update() 
        bullet_group.update()
        zombie_group.update(player.rect.x, player.rect.y)
        
        for bullet in bullet_group:
            enemy_hits = pygame.sprite.spritecollide(bullet, zombie_group, False)
            for zombie in enemy_hits:
                zombie.kill()
        for zombie in zombie_group:
            player_hit = pygame.sprite.spritecollide(zombie, player_group, False)
            for players in player_hit:
                players.kill()
                


        if not player_group:
            run = False
        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
