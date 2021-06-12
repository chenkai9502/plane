import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply

from pygame.locals import *
from random import *

def add_small_enemies(group1,group2,num):
    for i in range(num):
        el = enemy.SmallEnemy(bg_size)
        group1.add(el)
        group2.add(el)

def draw_score_bombs_lifes():
    bomb_text = bomb_font.render("X %d"% bomb_num,True,WHITE)
    text_rect = bomb_text.get_rect()
    screen.blit(bomb_image,(10,height-10-bomb_rect.height))
    screen.blit(bomb_text,(20+bomb_rect.width,height-5-text_rect.height))

    if life_num:
        for i in range(life_num):
            screen.blit(life_image,\
                        (width-10-(i+1)*life_rect.width,\
                         height-10-life_rect.height))

    score_text = score_font.render("Score:%s"%str(score),True,WHITE)
    screen.blit(score_text,(10,5))

def draw_me():

    global me_destroy_index, life_num
    if me.active:
        if switch_image:
            screen.blit(me.image1,me.rect)
        else:
            screen.blit(me.image2,me.rect)
    else:
        if not (delay % 3):
            if me_destroy_index == 0:
                me_down_sound.play()
            screen.blit(me.destroy_images[me_destroy_index],me.rect)
            me_destroy_index = (me_destroy_index + 1) % 4
            if me_destroy_index == 0:
                life_num -= 1
                me.reset()
                pygame.time.set_timer(INVINCIBLE_TIME, 3*1000)

def draw_small():
    global e1_destroy_index,score
    for each in small_enemies:
        if each.active:
            each.move()
            screen.blit(each.image,each.rect)

        elif not (delay%3):
            if e1_destroy_index == 0:
                enemy1_down_sound.play()
            screen.blit(each.destroy_images[e1_destroy_index],each.rect)
            e1_destroy_index = (e1_destroy_index+1)%4
            if e1_destroy_index == 0:
                score += 1000
                each.reset()

def continueOrQuit():
    global record_score, score, life_num
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    pygame.time.set_timer(SUPPLY_TIME,0)
    record_score_text = score_font.render("Best: %d"%record_score,True,(255,255,255))
    gameover_text1 = gameover_font.render("Your Score",True,(255,255,255))
    gameover_text1_rect = gameover_text1.get_rect()
    gameover_text1_rect.left,gameover_text1_rect.top = \
        (width - gameover_text1_rect.width) // 2,height // 3
    screen.blit(gameover_text1,gameover_text1_rect)

    gameover_text2 = gameover_font.render(str(score),True,(255,255,255))
    gameover_text2_rect = gameover_text2.get_rect
    gameover_text2_rect.left,gameover_text2_rect.top = \
        (width - gameover_text2_rect.width) // 2,\
    gameover_text1_rect.bottom + 10
    screen.blit(gameover_text2,gameover_text2_rect)

    again_rect.left,again_rect.top = \
        (width - again_rect.width) //2, \
        gameover_text2_rect.bottom + 50
    screen.blit(again_image,again_rect)

    gameover_rect.left,gameover_rect.top = \
        (width - again_rect.width) // 2, \
        again_rect.bottom + 10
    screen.blit(gameover_image,gameover_rect)

    if pygame.mouse.get_pressed()[0]:
        if score > record_score:
            record_score = score
            with open("record.txt","w") as f:
                f.write(str(score))
        pos = pygame.mouse.get_pos()
        if again_rect.left < pos[0] < again_rect.right and \
            again_rect.top < pos[1] <again_rect.bottom:
            life_num = 3
            score = 0
            main()
        elif gameover_rect.left < pos[0] <gameover_rect.right and \
            gameover_rect.top < pos[1] <gameover_rect.bottom:
            pygame.quit()
            sys.exit()

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("2021雷霆出击V1.0 明德学院信息系计科18 碧空战将")

background = pygame.image.load("images/background.png").convert()
bg1_top = 0
bg2_top = -700

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

score = 0
score_font = pygame.font.Font("font/font.ttf",36)

paused = False
pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
paused_rect = pause_nor_image.get_rect()
paused_rect.left,paused_rect.top = width - paused_rect.width - 10,10
paused_image = pause_nor_image

level = 1

bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
bomb_rect = bomb_image.get_rect()
bomb_font = pygame.font.Font("font/font.ttf",48)
bomb_num = 3

life_image = pygame.image.load("images/life.png").convert_alpha()
life_rect = life_image.get_rect()
life_num = 1

with open("record.txt","r") as f:
    record_score = int(f.read())

gameover_font = pygame.font.Font("font/font.TTF",48)
again_image = pygame.image.load("images/again.png").convert_alpha()
again_rect = again_image.get_rect()
gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
gameover_rect = gameover_image.get_rect()

me = myplane.MyPlane(bg_size)

enemies = pygame.sprite.Group()

small_enemies = pygame.sprite.Group()
add_small_enemies(small_enemies,enemies,15)

bullet1 = []
bullet1_index = 0
BULLET1_NUM = 4
for i in range(BULLET1_NUM):
    bullet1.append(bullet.Bullet1(me.rect.midtop))

bullet2 = []
bullet2_index = 0
BULLET2_NUM = 12
for i in range(BULLET2_NUM // 3):
    bullet2.append(bullet.Bullet2((me.rect.centerx-33,me.rect.centery)))
    bullet2.append(bullet.Bullet2((me.rect.centerx+30,me.rect.centery)))
    bullet2.append(bullet.Bullet2((me.rect.centerx-1,me.rect.centery)))

delay = 100

bullet_supply = supply.Bullet_Supply(bg_size)
bomb_supply = supply.Bomb_Supply(bg_size)
SUPPLY_TIME =  USEREVENT
pygame.time.set_timer(SUPPLY_TIME,30*1000)

DOUBLE_BULLET_TIME = USEREVENT + 1

is_double_bullet = False
is_Triple_Tap = False

INVINCIBLE_TIME = USEREVENT + 2

switch_image = True

clock = pygame.time.Clock()

e1_destroy_index = 0
e2_destroy_index = 0
e3_destroy_index = 0
me_destroy_index = 0


def main():
    global bullet1_index, bullet2_index, delay,bg1_top,bg2_top,bullets,paused,paused_image
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME,30*1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME,0)

        bg1_top = (bg1_top+1) if bg1_top <= 700 else -700
        bg2_top = (bg2_top+1) if bg2_top <= 700 else -700

        screen.blit(background,(0,bg1_top))
        screen.blit(background,(0,bg2_top))

        if life_num and not paused:
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            if not (delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-33,me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx+30,me.rect.centery))
                    if is_Triple_Tap:
                        bullets[bullet2_index+2].reset((me.rect.centerx-1,me.rect.centery))
                    bullet2_index = (bullet2_index+3)%BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index+1)%BULLET1_NUM

            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            e.active = False
            draw_small()
            enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False
            draw_me()
        elif life_num == 0:
            continueOrQuit()

        screen.blit(paused_image,paused_rect)

        draw_score_bombs_lifes()


        delay = (delay-1) if delay else 100

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()