import pygame, math, time, sys
from asteroids import Asteroid
from player import Player
from lasers import Laser
from particles import Emitter

import random

pygame.font.init()

#===== Fonctions =====
#=== Checker d'emplacement - Optimisation ===
def checkGridCollision(asteroid1:tuple, asteroid2:tuple, screenSize:tuple, cellSize=4)-> bool:
    '''
    Permet de partager la fenêtre en plusieurs cellules distinct pour permettre de meilleures collisions
    '''
    screenWidth=screenSize[0]
    screenHeight=screenSize[1]
    
    aste1LocX=asteroid1[0]
    aste2LocX=asteroid2[0]
    aste1LocY=asteroid1[1]
    aste2LocY=asteroid2[1]
    
    for x in range(1,cellSize+1):
        if screenWidth/cellSize*(x-1)<asteroid1[0]<=screenWidth/cellSize*x:
            aste1LocX=x
        if screenWidth/cellSize*(x-1)<asteroid2[0]<=screenWidth/cellSize*x:
            aste2LocX=x
            
        if screenHeight/cellSize*(x-1)<asteroid1[1]<=screenHeight/cellSize*x:
            aste1LocY=x
        if screenHeight/cellSize*(x-1)<asteroid2[1]<=screenHeight/cellSize*x:
            aste2LocY=x
        
    return aste1LocX==aste2LocX and aste1LocY==aste2LocY

#=== Détecteur de collisions ===
def collisionChecker(coord1:tuple, coord2:tuple, size1:float, size2:float)-> bool:
    '''
    Permet de détecter les collisions entres 2 objets
    '''
    return (coord2[0]-coord1[0])**2+(coord2[1]-coord1[1])**2<=(size1**2+size2**2)

#==========




class Game():
    def __init__(self)-> None:
        self.fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fenetre_width, self.fenetre_height = pygame.display.get_surface().get_size()
        self.horloge = pygame.time.Clock()
        
        #=== Player ===
        self.player=Player(self.fenetre_width, self.fenetre_height)
        self.playerSize=self.player.getSize()
        
        self.playerSprite=pygame.image.load('./img/player.png').convert_alpha()
        self.playerSprite=self.playerSprite.copy()
        self.playerSprite=pygame.transform.scale(self.playerSprite, (self.playerSize, self.playerSize))
        pygame.display.set_icon(self.playerSprite)

        self.playerSpriteMove=pygame.image.load('./img/playerMove.png').convert_alpha()
        self.playerSpriteMove=self.playerSpriteMove.copy()
        self.playerSpriteMove=pygame.transform.scale(self.playerSpriteMove, (self.playerSize, self.playerSize))

        self.playerSpriteInvincible=pygame.image.load('./img/playerInvincible.png').convert_alpha()
        self.playerSpriteInvincible=self.playerSpriteInvincible.copy()
        self.playerSpriteInvincible=pygame.transform.scale(self.playerSpriteInvincible, (self.playerSize, self.playerSize))

        self.playerInvincibleState=[0, True, 0] #[Dernier changement invisible, état invisible/visible, compteur de changements]
          
        #=== Lasers ===
        self.shootDelay=0
        self.lasersAll=[]
                
        #=== Asteroids ===
        self.asteroidNumber=6
        self.asteroidsAll=[Asteroid(self.fenetre_width, self.fenetre_height, random.randint(100, self.fenetre_width), random.randint(100, self.fenetre_height)) for _ in range(self.asteroidNumber)]

        #=== Pause Menu ===
        self.isPaused=False
        self.pauseMenu_buttons={}
        
        #=== Game Over Menu ===
        self.gameOverMenu_buttons={}
        self.scoreVal=0

        #=== Fonts ===
        self.mainFont_Little_Bold = pygame.font.Font('./font/asteroidBold.ttf', ((self.fenetre_width+self.fenetre_height)//2)//25-10)
        self.mainFont_Large = pygame.font.Font('./font/asteroid.ttf', ((self.fenetre_width+self.fenetre_height)//2)//15)
        self.mainFont_Large_Bold = pygame.font.Font('./font/asteroidBold.ttf', ((self.fenetre_width+self.fenetre_height)//2)//10)
    
        #=== Particles ===
        self.particleAll=[]


    #===== Méthodes =====
    #=== Affichages ===
    def generateParticles(self)-> None:
        '''
        Permet d'afficher et de mettre à jour les particules existantes
        '''
        for particle in self.particleAll:
            particleCoord=particle.getCoord()
            particleOrigin=particle.getOrigin()

            particleDTL=particle.getDTL()

            if abs(particleCoord[0]-particleOrigin[0])>particleDTL or abs(particleCoord[1]-particleOrigin[1])>particleDTL:
                self.particleAll.remove(particle)
            else:
                pygame.draw.circle(self.fenetre, particle.getColor(), particleCoord, particle.getSize())
                particle.move()     


    def generateLasers(self)-> None:
        '''
        Permet d'afficher et de mettre à jour les lasers existants
        '''
        for laser in self.lasersAll:
            laserCoord=laser.getCoord()

            if not -10<=laserCoord[0]<=self.fenetre_width+10 or not -10<=laserCoord[1]<=self.fenetre_height+10:
                self.lasersAll.remove(laser)
            else:
                pygame.draw.circle(self.fenetre, laser.getColor(), laser.getCoord(), laser.getSize())
                laser.move()
            
            
    def generateAsteroids(self)-> None:
        '''
        Permet d'afficher et de mettre à jour les astéroides existants
        '''
        for asteroid in self.asteroidsAll:
            asteroid1Coord=asteroid.getCoord()
            asteroid1Size=asteroid.getSize()

            #= Vérification de sécurité =
            if asteroid1Coord[0]<=0 or asteroid1Coord[0]>=self.fenetre_width:
                self.asteroidsAll.remove(asteroid)
                continue
            if asteroid1Coord[1]<=0 or asteroid1Coord[1]>=self.fenetre_height:
                self.asteroidsAll.remove(asteroid)
                continue


            #= Collisions avec le joueur =
            if not self.player.getInvincible():
                playerCoord=self.player.getCoord()
                playerSize=self.player.getSize()
                if checkGridCollision(asteroid1Coord, playerCoord, (self.fenetre_width, self.fenetre_height), 2):
                    if collisionChecker((asteroid1Coord[0]-asteroid1Size/2, asteroid1Coord[1]-asteroid1Size/2), (playerCoord[0], playerCoord[1]), asteroid1Size, playerSize):
                        self.particleAll.extend(Emitter(playerCoord[0], playerCoord[1], self.fenetre_width, self.fenetre_height).ExplosionFlame(20, 10, 5))
                        playerLife=self.player.getLife()
                        if playerLife>0:
                            self.player.setLife(playerLife-1)
                            self.player.reset()


            #= Collisions avec les lasers =
            for laser in self.lasersAll:
                laserCoord=laser.getCoord()
                laserSize=laser.getSize()

                if checkGridCollision(asteroid1Coord, laserCoord, (self.fenetre_width, self.fenetre_height), 2):
                    if collisionChecker(asteroid1Coord, laserCoord, asteroid1Size, laserSize):
                        if self.player.getScore()>=10000:
                            self.particleAll.extend(Emitter(laserCoord[0], laserCoord[1], self.fenetre_width, self.fenetre_height).Explosionjeb_(25, 17, 4))
                        else:
                            self.particleAll.extend(Emitter(laserCoord[0], laserCoord[1], self.fenetre_width, self.fenetre_height).Explosion(20, 17, (160,160,160), 3))
                        
                        self.player.score+=int(asteroid1Size)
                        if asteroid1Size/2<asteroid.minSize:
                            self.asteroidsAll.remove(asteroid)
                        else:
                            self.lasersAll.remove(laser)
                            self.asteroidsAll.extend(asteroid.divide())
                            self.asteroidsAll.remove(asteroid)
                        break

            #= Collisions avec les autres astéroides =
            for asteroid2 in self.asteroidsAll:
                if asteroid==asteroid2:
                    continue

                asteroid2Coord=asteroid2.getCoord()
                asteroid2Size=asteroid.getSize()
                
                if checkGridCollision(asteroid1Coord, asteroid2Coord, (self.fenetre_width, self.fenetre_height), 2):
                    asteroid1Speed=asteroid.getSpeed()
                    asteroid2Speed=asteroid2.getSpeed()
                    
                    if collisionChecker(asteroid1Coord, asteroid2Coord, asteroid1Size, asteroid2Size):
                        #= Physique des astéroides =
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

    def generatePlayer(self)-> None:
        '''
        Permet d'afficher et de mettre à jour le joueur et ses actions
        '''
        #=== Données du joueur ===
        playerSpeed, playerBaseSpeed, playerMaxSpeed=self.player.getSpeed()
        playerFriction=self.player.getFriction()
        playerInvincible=self.player.getInvincible()
        playerEngine, playerEngineSatus, playerEngineColor=self.player.getEngine()

        playerCoord=self.player.getCoord()
        playerRot=self.player.getRotation()
        playerRot_Format=self.player.getRotationFormat()
        playerLastShoot=self.player.getLastShoot()

        PlayerSprite_rect = self.playerSprite.get_rect(center = self.playerSprite.get_rect(topleft = (playerCoord)).center)
        
        #=== Actions du joueur ===
        keys = pygame.key.get_pressed()

        #Sprite du joueur
        if playerInvincible:
            if self.playerInvincibleState[2]>=16:
                self.player.setInvincible(False)
                self.playerInvincibleState=[0, True, 0]

            if time.time()-self.playerInvincibleState[0]>=0.15:
                self.playerInvincibleState[0]=time.time()
                self.playerInvincibleState[1]=not self.playerInvincibleState[1]
                self.playerInvincibleState[2]+=1

            if self.playerInvincibleState[1]:
                if keys[pygame.K_z]:
                    rotatedPlayerSprite = pygame.transform.rotate(self.playerSpriteMove, playerRot)
                else:
                    rotatedPlayerSprite = pygame.transform.rotate(self.playerSprite, playerRot)
            else:
                rotatedPlayerSprite = pygame.transform.rotate(self.playerSpriteInvincible, playerRot)
        else:
            if keys[pygame.K_z] and playerEngineSatus:
                rotatedPlayerSprite = pygame.transform.rotate(self.playerSpriteMove, playerRot)
            else:
                rotatedPlayerSprite = pygame.transform.rotate(self.playerSprite, playerRot)
                
        PlayerSprite_rect = rotatedPlayerSprite.get_rect(center = self.playerSprite.get_rect(topleft = (playerCoord)).center)
        self.fenetre.blit(rotatedPlayerSprite, PlayerSprite_rect.topleft)


        #= Déplacements =
        if keys[pygame.K_z] and playerEngine>0 and playerEngineSatus:
            playerDirections=self.player.getDirections()

            if not playerSpeed>=playerMaxSpeed:
                if playerSpeed<=playerBaseSpeed:
                    self.player.setSpeed(playerBaseSpeed*1.02)
                else:
                    self.player.setSpeed(playerSpeed*1.02)
            else:
                self.player.setSpeed(playerMaxSpeed)
            
            if playerDirections[1]==0:
                playerDirections=(playerDirections[0], -1)

            self.player.propulse(playerDirections[0],playerDirections[1])
            self.player.setEngine(playerEngine-0.6)
        else:
            if not playerSpeed<=0.01:
                self.player.setSpeed(playerSpeed*playerFriction)
                self.player.propulse(self.player.lastMove[0], self.player.lastMove[1])
                self.player.setEngine(playerEngine+0.5)
            if playerEngine<=0:
                self.player.setEngineStatus(False)
            elif playerEngine>=75 and playerEngineSatus==False:
                self.player.setEngineStatus(True)

                
        if keys[pygame.K_q] or keys[pygame.K_d]:
            if keys[pygame.K_q]:
                self.player.rotate(1)
                self.player.setSpeed(playerSpeed*playerFriction)
            if keys[pygame.K_d]:
                self.player.rotate(-1)
                self.player.setSpeed(playerSpeed*playerFriction)

            directionX=math.cos((math.pi*playerRot_Format)/180)*-1
            directionY=math.sin((math.pi*playerRot_Format)/180)
            self.player.setDirections(directionX, directionY)

        #= Tirs =
        if keys[pygame.K_SPACE]:
            if time.time()*1000-playerLastShoot>=self.shootDelay:

                if time.time()*1000-playerLastShoot>1000:
                    self.player.setRafaleCompt(0)

                playerDirections=self.player.getDirections()
                playerRafaleCompt=self.player.getRafaleCompt()
                    
                if playerRafaleCompt>=6:
                    self.shootDelay=500
                    self.player.setRafaleCompt(0)
                else:
                    self.shootDelay=70
                    self.player.setRafaleCompt(playerRafaleCompt+1)
                    self.lasersAll.append(Laser(PlayerSprite_rect.center[0], PlayerSprite_rect.center[1], playerDirections[0], playerDirections[1], self.fenetre_width, self.fenetre_height))

                self.player.setLastShoot(time.time()*1000)
                
            
            
        #=== Score ===
        if self.player.getScore()<=9:
            PlayerScore = self.mainFont_Large.render("00"+str(self.player.getScore()), True, (255,255,255))
        elif self.player.getScore()<=99:
            PlayerScore = self.mainFont_Large.render("0"+str(self.player.getScore()), True, (255,255,255))
        else:
            PlayerScore = self.mainFont_Large.render(str(self.player.getScore()), True, (255,255,255))
        PlayerScore_Rect = PlayerScore.get_rect()
        PlayerScore_Rect.center = (self.fenetre_width/2, 80)
        self.fenetre.blit(PlayerScore, PlayerScore_Rect)
        pygame.draw.rect(self.fenetre, (255, 255, 255), (self.fenetre_width/2-PlayerScore_Rect.width/2-10, 80-PlayerScore_Rect.height/2, PlayerScore_Rect.width+10, PlayerScore_Rect.height), 3)

        #=== Vies ===
        PlayerLife = self.mainFont_Large.render("A"*self.player.getLife(), True, (255,255,255))
        PlayerLife_Rect = PlayerLife.get_rect()
        PlayerLife_Rect.center=PlayerScore_Rect.center
        PlayerLife_Rect.left = 30
        self.fenetre.blit(PlayerLife, PlayerLife_Rect)

        #=== Engine ===
        engineRect=pygame.Rect(PlayerScore_Rect.left-self.fenetre_width/4, PlayerScore_Rect.bottom-PlayerLife_Rect.height/2-20, self.fenetre_width/6, 50)

        pygame.draw.rect(self.fenetre, playerEngineColor, (PlayerScore_Rect.left-self.fenetre_width/4, PlayerScore_Rect.bottom-PlayerLife_Rect.height/2-20, self.fenetre_width/6*playerEngine/100, 50))
        pygame.draw.rect(self.fenetre, (255, 255, 255), engineRect, 3)
        if playerEngine<=75:
            pygame.draw.line(self.fenetre, (255,255,255), (engineRect.midbottom[0]+engineRect.width/4, engineRect.bottom-3), (engineRect.midtop[0]+engineRect.width/4, engineRect.top), 3)

        if playerEngine<=30:
            engineText = self.mainFont_Little_Bold.render(str(int(playerEngine))+"%", True, (168,52,58))
        else:
            engineText = self.mainFont_Little_Bold.render(str(int(playerEngine))+"%", True, (120,120,120))
        engineText_Rect = engineText.get_rect()
        engineText_Rect.center=engineRect.center
        self.fenetre.blit(engineText, engineText_Rect)


    #===== Menus =====
    #Pause
    def DisplayPauseMenu(self):
        buttonsPadding=50
        pauseBoxSize=self.fenetre_width/6

        #=== Pause Menu Title ===
        PauseMenuTitle = self.mainFont_Large_Bold.render("PAUSE", True, (255,255,255))
        PauseMenuTitle_Rect = PauseMenuTitle.get_rect()
        PauseMenuTitle_Rect.center = (self.fenetre_width/2, self.fenetre_height/6)
        self.fenetre.blit(PauseMenuTitle, PauseMenuTitle_Rect)
        pygame.draw.rect(self.fenetre, (255, 255, 255), (PauseMenuTitle_Rect.center[0]-PauseMenuTitle_Rect.width/2-pauseBoxSize/2, PauseMenuTitle_Rect[1], PauseMenuTitle_Rect.width+pauseBoxSize, PauseMenuTitle_Rect.height), 3)

        #=== Play Button ===
        PlayGameBtn = self.mainFont_Large.render("Continue", True, (255,255,255))
        PlayGameBtn_Rect = PlayGameBtn.get_rect()
        PlayGameBtn_Rect.center = (self.fenetre_width/2, self.fenetre_height/3+80)
        self.pauseMenu_buttons["continue"]=PlayGameBtn_Rect
        self.fenetre.blit(PlayGameBtn, PlayGameBtn_Rect)

        #=== Restart Button ===
        RestartBtn = self.mainFont_Large.render("RESTART", True, (255,255,255))
        RestartBtn_Rect = RestartBtn.get_rect()
        RestartBtn_Rect.center = (self.fenetre_width/2, PlayGameBtn_Rect.center[1]+PlayGameBtn_Rect.height+buttonsPadding)
        self.pauseMenu_buttons["restart"]=RestartBtn_Rect
        self.fenetre.blit(RestartBtn, RestartBtn_Rect)

        #=== Quit Button ===
        QuitBtn = self.mainFont_Large.render("QUIT", True, (255,255,255))
        QuitBtn_Rect = QuitBtn.get_rect()
        QuitBtn_Rect.center = (self.fenetre_width/2, RestartBtn_Rect.center[1]+RestartBtn_Rect.height+buttonsPadding)
        self.pauseMenu_buttons["quit"]=QuitBtn_Rect
        self.fenetre.blit(QuitBtn, QuitBtn_Rect)
    
    #GameOver
    def DisplayGameOver(self, scoreVal:int):
        buttonsPadding=50
        scoreBoxSize=self.fenetre_width/6

        #=== GameOver Title ===
        GameOverTitle = self.mainFont_Large_Bold.render("Game over", True, (255,255,255))
        GameOverTitle_Rect = GameOverTitle.get_rect()
        GameOverTitle_Rect.center = (self.fenetre_width/2, self.fenetre_height/6)
        self.fenetre.blit(GameOverTitle, GameOverTitle_Rect)

        #=== Score Title ===
        playerScore=self.player.getScore()
        if scoreVal<playerScore:
            if playerScore<=120:
                scoreVal+=1
            else:
                scoreVal+=(playerScore//100)
        else:
            scoreVal=playerScore
        ScoreTitle = self.mainFont_Large_Bold.render(str(scoreVal), True, (255,255,255))
        ScoreTitle_Rect = ScoreTitle.get_rect()
        ScoreTitle_Rect.center = (self.fenetre_width/2, GameOverTitle_Rect.center[1]+ScoreTitle_Rect.height+buttonsPadding)
        self.fenetre.blit(ScoreTitle, ScoreTitle_Rect)
        pygame.draw.rect(self.fenetre, (255, 255, 255), (ScoreTitle_Rect.center[0]-ScoreTitle_Rect.width/2-scoreBoxSize/2, ScoreTitle_Rect[1], ScoreTitle_Rect.width+scoreBoxSize, ScoreTitle_Rect.height), 3)

        #=== Play again Button ===
        PlayGameBtn = self.mainFont_Large.render("Play again", True, (255,255,255))
        PlayGameBtn_Rect = PlayGameBtn.get_rect()
        PlayGameBtn_Rect.center = (self.fenetre_width/2, ScoreTitle_Rect.bottom+self.fenetre_height/4)
        self.gameOverMenu_buttons["replay"]=PlayGameBtn_Rect
        self.fenetre.blit(PlayGameBtn, PlayGameBtn_Rect)

        #=== Quit Button ===
        QuitBtn = self.mainFont_Large.render("QUIT", True, (255,255,255))
        QuitBtn_Rect = QuitBtn.get_rect()
        QuitBtn_Rect.center = (self.fenetre_width/2, PlayGameBtn_Rect.center[1]+PlayGameBtn_Rect.height+buttonsPadding)
        self.gameOverMenu_buttons["quit"]=QuitBtn_Rect
        self.fenetre.blit(QuitBtn, QuitBtn_Rect)

        return scoreVal
    #==========

    
    #===== Game =====    
    def Start(self)-> None:
        while True:
            self.fenetre.fill((0,0,0))
            
            if not self.isPaused and not self.player.getLife()<=0:
                pygame.mouse.set_pos(self.fenetre_width/2, self.fenetre_height/2)
                pygame.mouse.set_visible(False)

                #=== Passage au niveau suivant ===
                if len(self.asteroidsAll)<=0:
                    if not self.player.level>=14:
                        self.player.level+=1
                    self.asteroidsAll=[Asteroid(self.fenetre_width, self.fenetre_height, random.randint(100, self.fenetre_width), random.randint(100, self.fenetre_height)) for _ in range(self.asteroidNumber+self.player.level)]
                    self.player.reset()

                #=== Affichage des Lasers ===
                self.generateLasers()
                #======

                #=== Affichage des Asteroides ===
                self.generateAsteroids()
                #======
                    
                #=== Affichage du joueur et de ses actions ===
                self.generatePlayer()
                #======

                #=== Affichage des Particules ===
                self.generateParticles()
                #======

            elif self.isPaused:
                pygame.mouse.set_visible(True)
                self.DisplayPauseMenu()
            else:
                pygame.mouse.set_visible(True)
                self.scoreVal=self.DisplayGameOver(self.scoreVal)

            
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                #= Menu Pause =
                if event.type == pygame.KEYDOWN:
                    if event.key==27:
                        self.isPaused=not self.isPaused

                #= Fonctionnement des boutons des menus =
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos=pygame.mouse.get_pos()
                    if self.isPaused:
                        for b in self.pauseMenu_buttons:
                            buttonRect=self.pauseMenu_buttons[b]
                            if buttonRect.left<=mousePos[0]<=buttonRect.right and buttonRect.top<=mousePos[1]<=buttonRect.bottom:
                                if b=="continue":
                                    self.isPaused=False
                                elif b=="restart":
                                    game=Game()
                                    game.Start()
                                elif b=="quit":
                                    pygame.quit()
                                    sys.exit()
                    if self.player.getLife()<=0:
                        for b in self.gameOverMenu_buttons:
                            buttonRect=self.gameOverMenu_buttons[b]
                            if buttonRect.left<=mousePos[0]<=buttonRect.right and buttonRect.top<=mousePos[1]<=buttonRect.bottom:
                                if b=="replay":
                                    game=Game()
                                    game.Start()
                                elif b=="quit":
                                    pygame.quit()
                                    sys.exit() 
                    
            self.horloge.tick(70)
