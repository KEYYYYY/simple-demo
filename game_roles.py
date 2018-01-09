import pygame

SIZE = WIDTH, HEIGHT = 480, 800


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        super(Bullet, self).__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rects, init_pos):
        super(Player, self).__init__()
        self.images = []
        for i in range(len(player_rects)):
            self.images.append(plane_img.subsurface(
                player_rects[i]).convert_alpha())
        self.rect = player_rects[0]
        self.rect.topleft = init_pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.image_index = 0
        self.is_hit = False

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def move_up(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def move_down(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        else:
            self.rect.top += self.speed

    def move_left(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def move_right(self):
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        else:
            self.rect.right += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        super(Enemy, self).__init__()
        self.image = enemy_img
        self.rect = enemy_img.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 6
        self.down_index = 0

    def move(self):
        self.rect.top += self.speed
