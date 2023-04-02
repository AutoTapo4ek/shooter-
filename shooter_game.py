#Создай собственный Шутер!

from pygame import *
from random import randint

font.init()
font2 = font.SysFont('Arial', 40)

img_back = "eeee.png" 
img_hero = "52243234.png" 
img_enemy = "gg.png"
img_bullet = "keg.png"

score = 0
lost = 0

class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)

       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed

       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
       keys = key.get_pressed()
       if keys[K_a] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_d] and self.rect.x < win_width - 90:
           self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 7, self.rect.top, 25, 30, 10 )
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

win_width = 900 
win_height = 700
display.set_caption('импостер')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
    
finish = False
run = True 
FPS = 1
speed = 1
while run:
   for e in event.get():
       if e.type == QUIT:
            run = False

       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               ship.fire()

   if not finish:
       window.blit(background,(0,0))

       text = font2.render("Счет:" + str(score), 1, (255,255,255))

       window.blit(text, (10, 20))

       text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))

       window.blit(text_lose, (10, 50))

       ship.update()

       monsters.update()

       bullets.update()

       ship.reset()

       monsters.draw(window)

       bullets.draw(window)

       collides = sprite.groupcollide(monsters, bullets, True, True)

       for c in collides:
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)

       if score >= 30:
           finish = True
           font = font.Font('Arial', 40)
           win = font.render('Ты белый!', True, (255 ,215  ,0))
           window.blit(win, (230, 250))

       if lost >= 20 or len(sprite.spritecollide(ship, monsters, False)) > 0:
           finish = True
           font = font.SysFont('Arial', 40)
           lose = font.render('Ты негр!', True, (255, 0, 0))
           window.blit(lose, (150, 350,))

       display.update()

       

       

   time.delay(1)

