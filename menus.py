import pygame, sys, random, math
from game import Game
from asteroids import Asteroid
from game import checkGridCollision, collisionChecker

pygame.init()

class MainMenu():
    def __init__(self) -> None:
        self.fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fenetre_width, self.fenetre_height = pygame.display.get_surface().get_size()
        self.horloge = pygame.time.Clock()

        self.mainFont_Large = pygame.font.Font('./font/asteroid.ttf', ((self.fenetre_width+self.fenetre_height)//2)//13)
        self.mainTitle=pygame.image.load('./img/MainTitlePaint.png').convert_alpha()

        self.buttons=[]

        #=== Astéroides en fond ===
        self.asteroidsAll=[Asteroid(self.fenetre_width, self.fenetre_height, random.randint(100, self.fenetre_width), random.randint(100, self.fenetre_height)) for _ in range(6)]


    def generateAsteroids(self)-> None:
        '''
        Permet de mettre à jour et d'afficher les astéroides
        '''
        for asteroid in self.asteroidsAll:
            asteroid1Coord=asteroid.getCoord()
            asteroid1Size=asteroid.getSize()

            for asteroid2 in self.asteroidsAll:
                if asteroid==asteroid2:
                    continue

                asteroid2Coord=asteroid2.getCoord()
                asteroid2Size=asteroid.getSize()
                
                if checkGridCollision(asteroid1Coord, asteroid2Coord, (self.fenetre_width, self.fenetre_height), 2):
                    asteroid1Speed=asteroid.getSpeed()
                    asteroid2Speed=asteroid2.getSpeed()
                    
                    if collisionChecker(asteroid1Coord, asteroid2Coord, asteroid1Size, asteroid2Size):
                        vCollision = {"x": asteroid2Coord[0]-asteroid1Coord[0], "y":  asteroid2Coord[1]-asteroid1Coord[1]}
                        distance = math.sqrt((asteroid2Coord[0]-asteroid1Coord[0])**2+(asteroid2Coord[1]-asteroid1Coord[1])**2)
                        if distance==0:
                            continue

                        vCollisionNorm = {"x": vCollision["x"]/distance, "y": vCollision["y"]/distance}
                        vRelativeVelocity = {"x": asteroid1Speed[0]-asteroid2Speed[0], "y": asteroid1Speed[1]-asteroid2Speed[1]}
                        speed = vRelativeVelocity["x"]*vCollisionNorm["x"]+vRelativeVelocity["y"]*vCollisionNorm["y"]

                        impulse = 2*speed/(asteroid1Size + asteroid2Size)/10
                        asteroid.changeSpeed(asteroid1Speed[0]+(impulse*asteroid2Size*vCollisionNorm["x"]), asteroid1Speed[1]+(impulse*asteroid2Size*vCollisionNorm["y"]))
                        asteroid2.changeSpeed(asteroid2Speed[0]+(impulse*asteroid1Size*vCollisionNorm["x"]), asteroid2Speed[1]+(impulse*asteroid1Size*vCollisionNorm["y"]))

                        asteroid2.bounce(asteroid)
                        asteroid.bounce(asteroid2)
            
            asteroid.move()
            pygame.draw.circle(self.fenetre, asteroid.color, asteroid1Coord, asteroid1Size, 2)


    def Start(self)-> None:
        while True:
            self.fenetre.fill((0,0,0))

            #=== Affichage des astéroides en fond ===
            self.generateAsteroids()

            #=== Affichage du titre du film ===
            self.fenetre.blit(self.mainTitle, (self.fenetre_width/2-self.mainTitle.get_width()/2, self.fenetre_height/4-self.mainTitle.get_height()/2))

            #=== Play Button ===
            PlayGameBtn = self.mainFont_Large.render("PLAY GAME", True, (255,255,255))
            PlayGameBtn_Rect = PlayGameBtn.get_rect()
            PlayGameBtn_Rect.center = (self.fenetre_width/2, self.fenetre_height/2+30)
            self.buttons.append(PlayGameBtn_Rect)
            self.fenetre.blit(PlayGameBtn, PlayGameBtn_Rect)
            pygame.draw.line(self.fenetre, (255,255,255), PlayGameBtn_Rect.bottomleft, PlayGameBtn_Rect.bottomright, 2)

            #=== Quit Button ===
            QuitBtn = self.mainFont_Large.render("QUIT", True, (255,255,255))
            QuitBtn_Rect = QuitBtn.get_rect()
            QuitBtn_Rect.center = (self.fenetre_width/2, self.fenetre_height/4*3+50)
            self.buttons.append(QuitBtn_Rect)
            self.fenetre.blit(QuitBtn, QuitBtn_Rect)
            pygame.draw.line(self.fenetre, (255,255,255), QuitBtn_Rect.bottomleft, QuitBtn_Rect.bottomright, 2)

            pygame.display.update()
            #= Fonctionnement des boutons du menu =
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos=pygame.mouse.get_pos()
                    for b in self.buttons:
                        if b.left<=mousePos[0]<=b.right and b.top<=mousePos[1]<=b.bottom:
                            if b==PlayGameBtn_Rect:
                                game=Game()
                                game.Start()
                            elif b==QuitBtn_Rect:
                                pygame.quit()
                                sys.exit()
                    
            self.horloge.tick(70)