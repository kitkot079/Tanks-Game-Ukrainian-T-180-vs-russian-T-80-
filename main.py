from pygame import*
from random import randint
mixer.init()
mixer.music.load("pustynya-atmosfernye-zvuki.mp3")
mixer.music.set_volume(10)
mixer.music.play()

firesound = mixer.Sound("shot_sound.mp3")
firesound.set_volume(0.5)

hp = 3 

font.init()
myfont = font.Font(None, 36)
font1 = font.Font(None, 80)
win = font1.render("YOU WIN", True, (255,255,255))
lose = font1.render("YOU LOSE", True, (255,255,255))


window = display.set_mode((1920, 1080))
bg = transform.scale(image.load("pustynya_map.png"), (1920, 1080))
clock = time.Clock()
game = True
finish = False

lost = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        sprite.Sprite.__init__(self)
        self.speed = player_speed
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        buttons = key.get_pressed()
        if buttons[K_w] and self.rect.y >4:
            self.rect.y -= self.speed
        if buttons[K_s] and self.rect.y <1900:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("artillery_shell.png", self.rect.x, self.rect.centery-10, 50, 10, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__(player_image, player_x, player_y, width, height, player_speed)
        self.vertical_speed = randint(-1, 1)  
    def update(self):       
        self.rect.x += self.speed
        self.rect.y += self.vertical_speed       
        if self.rect.y <= 0 or self.rect.y >= 1080 - self.rect.height:
            self.vertical_speed *= -1       
        if self.rect.x >= 1920:
            self.rect.x = randint(-400, -50)
            self.rect.y = randint(0, 1080 - self.rect.height)
            self.vertical_speed = randint(-1, 1)        
        for enemy in Enemys:
            if enemy != self and sprite.collide_rect(self, enemy):              
                if self.rect.x > enemy.rect.x: 
                    self.rect.x += 2
                else:  
                    self.rect.x -= 2
                if self.rect.y > enemy.rect.y: 
                    self.rect.y += 2
                else: 
                    self.rect.y -= 2

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.kill()

bullets  = sprite.Group()
Enemys = sprite.Group()
for i in range(4):
    enemy = Enemy("rus TANK.PNG", -30, randint(0, 1000), 393.5, 152.75, randint(1, 2))
    Enemys.add(enemy)
rocket = Player('URK TANK.PNG', 1500, 500, 393.5, 152.75, 2)




while game == True:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                rocket.fire()
                firesound.play()

    if finish != True:
        window.blit(bg, (0, 0))
        Enemys.draw(window)
        Enemys.update()
        rocket.draw()
        rocket.update()
        bullets.update()
        bullets.draw(window)
        if sprite.spritecollide(rocket, Enemys, True):
            hp -= 1
            enemy = Enemy("rus TANK.PNG", -30, randint(0, 1000), 393.5, 152.75, randint(1, 2))
            Enemys.add(enemy)
        if sprite.groupcollide(Enemys, bullets, True, True):
            score += 1
            enemy = Enemy("rus TANK.PNG", -30, randint(0, 1000), 393.5, 152.75, randint(1, 2))
            Enemys.add(enemy)
        if score > 50:
            finish = True
            window.blit(win, (800, 500))
        if hp <= 0 or lost >= 5:
            finish = True
            window.blit(lose, (800, 500))
        textlost = myfont.render("WASTED: "+ str(lost), True, (255, 255, 255))
        window.blit(textlost, (5, 20))
        textlost = myfont.render("LIVES: "+ str(hp), True, (255, 255, 255))
        window.blit(textlost, (5, 45))
        textlost = myfont.render("SCORE: "+ str(score), True, (255, 255, 255))
        window.blit(textlost, (5, 70))

    else:
        time.delay(5000)
        finish = False
        lost = 0
        score = 0
        hp = 3
        for enemy in Enemys:
            enemy.kill()
        for bullet in bullets:
            bullet.kill()
        for i in range(4):
            enemy = Enemy("rus TANK.PNG", -30, randint(0, 1000), 393.5, 152.75, randint(1, 2))
            Enemys.add(enemy)

    display.update()
    clock.tick(143)
        