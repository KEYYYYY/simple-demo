from random import randint
from datetime import datetime

import pygame
from pygame import locals
from sys import exit

from game_roles import SIZE, Player, Enemy


# 初始化游戏
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('✈️')

# 载入游戏音乐
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 载入背景图
background = pygame.image.load('resources/image/background.png')
# 载入游戏结束图片
gameover = pygame.image.load('resources/image/gameover.png')
# 载入所有飞机和子弹图片
plane_img = pygame.image.load('resources/image/shoot.png')

# 设置玩家相关参数
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家飞机图片区域
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家飞机爆炸图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# 定义子弹对象使用的surface相关参数
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 定义敌机对象使用的surface相关参数
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

clock = pygame.time.Clock()
enemies1 = pygame.sprite.Group()
# 存储被击毁的飞机
enemies_down = pygame.sprite.Group()
shoot_frequency = 0
enemy1_frequency = 0
score = 0
running = True
is_save = False


while running:
    # 控制游戏最大帧数为60
    clock.tick(60)

    # 控制敌机生成频率，并生成敌机
    if not player.is_hit:
        if enemy1_frequency % 15 == 0:
            enemy1_pos = [randint(0, SIZE[0] - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy1_frequency += 1
        if enemy1_frequency >= 15:
            enemy1_frequency = 0

    # 移动子弹，若超出窗口范围则删除
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # 移动敌机，若超出窗口范围则删除
    for enemy in enemies1:
        enemy.move()
        # 判断玩家是否被击中
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SIZE[1]:
            enemies1.remove(enemy)

    # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # 绘制背景和飞机和子弹
    screen.fill(0)
    if not player.is_hit:
        screen.blit(background, (0, 0))
        player.image_index = 0
    else:
        player.image_index = 2
        screen.blit(gameover, (0, 0))
        if not is_save:
            with open('data.txt', 'a', encoding='utf-8') as f:
                f.write(
                    '{datetime}: {score}\n'.format(
                        datetime=datetime.now(), score=score)
                )
                is_save = not is_save

    screen.blit(player.images[player.image_index], player.rect)
    player.img_index = shoot_frequency

    # 绘制击毁动画
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 3:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(
            enemy_down.down_imgs[enemy_down.down_index], enemy_down.rect)
        enemy_down.down_index += 1

    # 绘制得分
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    player.bullets.draw(screen)
    enemies1.draw(screen)

    # 更新屏幕
    pygame.display.update()

    # 处理移动事件
    key_pressed = pygame.key.get_pressed()
    if not player.is_hit:
        if key_pressed[locals.K_UP]:
            player.move_up()
        if key_pressed[locals.K_DOWN]:
            player.move_down()
        if key_pressed[locals.K_LEFT]:
            player.move_left()
        if key_pressed[locals.K_RIGHT]:
            player.move_right()
        if key_pressed[locals.K_f]:
            bullet_sound.play()
            player.shoot(bullet_img)

    # 处理游戏退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
