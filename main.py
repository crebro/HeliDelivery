import pygame
import os
from models import levels, package
pygame.init()
pygame.mixer.init()

width, height = 400, 300
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('HeliDelivery')

class Chopper:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = self.getImages()
        self.image_counter = 0
        self.destroyed = False
        self.destroyedCabin = pygame.transform.scale(pygame.image.load(os.path.join('assets\\broken_parts', 'cabine.png')), (50, 50))
        self.destroyedBack = pygame.transform.scale(pygame.image.load(os.path.join('assets\\broken_parts', 'helicopter_back.png')), (50, 50))
        self.playDestroyed = False
        self.packageLoaded = True
        self.delivered = 0

    def getImages(self):
        giveList = []
        for num in range(1, 9):
            giveList.append(pygame.transform.scale(pygame.image.load(os.path.join('assets\\separated_frames', f'helicopter_{num}.png')), (100, 50)))
        return giveList

    def drawonScreen(self, surface, background, packagelist, helipadxy):
        
        if not(self.destroyed):
            
            surface.blit(self.images[self.image_counter], (self.x, self.y))
            if self.image_counter == 7:
                self.image_counter = 0
            self.image_counter += 1
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.y -= 5
                
            if keys[pygame.K_s]:
                if self.y < height//2:
                    self.y += 5
                if not(self.x > helipadxy[0]-20) or not(self.x < helipadxy[0]+100):
                    if self.y > height//2 - 10:
                        self.destroyed = True
                        self.playDestroyed = True
                elif self.y > height//2 -10 and background.packagesToDeliver == len(packagelist):
                    print('level completed')
                
               
            if keys[pygame.K_a]:
                background.x += 10
                for pack in packagelist:
                    pack.x += 10
            if keys[pygame.K_d] and -background.x < background.image.get_width():
           
                background.x -= 10
                for pack in packagelist:
                    pack.x -= 10

            
            if keys[pygame.K_SPACE] and background.packagesToDeliver > len(packagelist) and self.packageLoaded:
                if self.x > background.x + background.deliveryRange[0] and self.x < background.x + background.deliveryRange[1]:
                    self.delivered += 1
                packagelist.append(package.Package(self.x, self.y))
                self.packageLoaded = False


            if keys[pygame.K_TAB]:
                self.packageLoaded = True
        else:
            surface.blit(self.destroyedBack, (self.x, self.y))
            surface.blit(self.destroyedCabin, (self.x + self.destroyedBack.get_width(), self.y))
            if self.playDestroyed:
                crash_sound = pygame.mixer.Sound("assets\\explosion.wav")
                pygame.mixer.Sound.play(crash_sound)

                pygame.mixer.music.play(1)
                print('played')
                self.playDestroyed = False

        



def main():
    level1 = levels.Level1(0, 0)
    packageList = []
    playmusic = True
    stopmusic = False
    pygame.mixer.music.load(os.path.join('assets', 'HelicopterSound.wav'))
    run = True
    helicopter = Chopper(width//2, height//2-50)
    helipad = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'helipad.png')), (100, 50))
    clock = pygame.time.Clock()
    while run:
        helipadxy = (level1.x+width//2,  height//2+helicopter.images[helicopter.image_counter].get_height()/2)
        clock.tick(60)
        win.fill((255, 255, 255))
        level1.drawSelf(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        win.blit(helipad, helipadxy)
        helicopter.drawonScreen(win, level1, packageList, helipadxy)
        
        if playmusic:
            pygame.mixer.music.play(-1)
            playmusic = False
        if stopmusic:
            pygame.mixer.music.stop()
            stopmusic = False
        if helicopter.destroyed:
            playmusic = False
            stopmusic = True

        for package in packageList:
            package.moveDown(win, 300)
                
            
        # helicopter.move()w
        pygame.display.update()


main()
pygame.quit()