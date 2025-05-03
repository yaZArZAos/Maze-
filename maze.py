from pygame import *

clock = time.Clock()
mixer.init()

font.init()
font1 = font.SysFont('Arial', 70)

win = font1.render('YOU WIN', True, (235, 123, 123))
lose = font1.render('YOU LOSE', True, (255, 0, 0))
mixer.music.load('jungles.ogg')
kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')

window = display.set_mode((700, 500))
display.set_caption('Maze')
background = transform.scale(
    image.load('background.jpg'),
    (700, 500)
)

class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__()
        self.image = transform.scale(
            image.load(filename),
            (w, h)
        )
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_press = key.get_pressed()
        if key_press[K_w] and self.rect.y >0:
            self.rect.y -= self.speed
        elif key_press[K_s] and self.rect.y <450:
            self.rect.y += self.speed
        elif key_press[K_a] and self.rect.x >0:
            self.rect.x -= self.speed
        elif key_press[K_d] and self.rect.x <650:
            self.rect.x += self.speed
        
class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= 650:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, w, h, color, x, y):
        super().__init__()
        self.image = Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



player = Player('hero.png', 50, 50, 5, 50, 400)
enemy = Enemy('cyborg.png', 50, 50, 5, 525, 250)
treasure = GameSprite('treasure.png', 50, 50, 5, 560, 400)
w1 = Wall(450, 10, (154, 205, 50), 100, 20)
w2 = Wall(350, 10, (154, 205, 50), 100, 480)
w3 = Wall(10, 380, (154, 205, 50), 100, 20)


mixer.music.play()
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
  
    if finish != True:
       window.blit(background,(0, 0))
       player.update()
       enemy.update()
      
       player.reset()
       enemy.reset()
       treasure.reset()


       w1.draw_wall()
       w2.draw_wall()
       w3.draw_wall()


       #Ситуация "Проигрыш"
    if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3):
        finish = True
        window.blit(lose, (200, 200))
        kick.play()


       #Ситуация "Выигрыш"
    if sprite.collide_rect(player, treasure):
        finish = True
        window.blit(win, (200, 200))
        money.play()


    display.update()
    clock.tick(60)
