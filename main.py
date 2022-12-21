import pygame
import os
import math

WIDTH, HEIGHT = 500,500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apocalypse Rerising")


PURPLE = (100,88,132)
BLACK = (0,0,0)

FPS = 60
VEL = 3

PLAYER_WIDTH, PLAYER_HEIGHT = 62,50
GUN_WIDTH, GUN_HEIGHT = 10, 4

CROSSHAIR_IMAGE = pygame.image.load(
    os.path.join('crosshair.png'))

cursor_rect = CROSSHAIR_IMAGE.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height,pos_x,pos_y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Biker Idle', 'tile000.png'))
        self.image = pygame.transform.scale(self.image,(height,width))
        self.rect = self.image.get_rect(center=(pos_x,pos_y))

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_w] and self.rect.y - VEL > 0: #move forwawrd
            self.rect.y  -= VEL    
        if keys_pressed[pygame.K_a] and self.rect.x - VEL > 0: #move left
            self.rect.x  -= VEL
        if keys_pressed[pygame.K_s] and self.rect.y + VEL + self.rect.height < HEIGHT - 18: #move back
            self.rect.y   += VEL
        if keys_pressed[pygame.K_d] and self.rect.x + VEL + self.rect.width < WIDTH: #move right
            self.rect.x  += VEL
    def create_bullet(self):
        return Bullet(self.rect.x, self.rect.y)



class Gun(Player):
    def __init__(self,width, height,pos_x,pos_y):
        super().__init__(width, height,pos_x,pos_y)
        self.image = pygame.image.load(os.path.join('guns', '2 Guns','8_1.png'))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(pos_x,pos_y))

    def update(self):
        x_mouse = pygame.mouse.get_pos()[0]
        y_mouse = pygame.mouse.get_pos()[1]
        x_diff = self.rect.x - x_mouse
        y_diff = self.rect.y-y_mouse
        
        angle = math.degrees(math.atan2(-y_diff, x_diff)) - 180
        self.image = pygame.transform.rotate(self.orig_image, angle)

    

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x ,pos_y):
        super().__init__(pos_x ,pos_y)
        self.image = pygame.image.load(os.path.join('guns', '5 Bullets', '8.png'))
        self.rect = self.image.get_rect(center=(pos_x,pos_y))
    def update(self):
        self.rect.x += 5
        
        








player = Player(PLAYER_HEIGHT, PLAYER_WIDTH, 300, 100)
player_group = pygame.sprite.Group()
player_group.add(player)

gun = Gun(PLAYER_HEIGHT, PLAYER_WIDTH, 300, 100)
gun_group = pygame.sprite.Group()
gun_group.add(gun)

bullet_group = pygame.sprite.Group()

def draw_window():
    WIN.fill(PURPLE)
    pygame.draw.rect(WIN, BLACK, (0, 0, WIDTH, HEIGHT), 10 )
    bullet_group.draw(WIN)
    player_group.draw(WIN)
    gun_group.draw(WIN)
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
                bullet_group.add(player.create_bullet())
        keys_pressed = pygame.key.get_pressed()
        player_group.update(keys_pressed)
        gun_group.update() 
        bullet_group.update()       
        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
