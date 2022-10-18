class Player():
    def __init__(self, maxX, maxY)-> None:
        self.x=maxX/2
        self.y=maxY/2
        self.angle=0
        self.color=(255,255,255)
        self.size=65

        self.maxX=maxX
        self.maxY=maxY

        self.lastMove=(0,0)

        self.xDirection=0
        self.yDirection=0
        self.baseSpeed=2
        self.maxSpeed=6
        self.speed=self.baseSpeed
        
        self.friction=0.993
        self.rotSpeed=4.5

        self.engine=100
        self.engineStatus=True
        self.engineColor=(230, 230, 230)

        self.lastShoot=0
        self.RafaleCompt=0

        self.lifes=3
        self.invincible=True
        self.score=0
        self.level=1

    #=== Getters ===
    def getCoord(self)-> tuple:
        return self.x, self.y
    
    def getRotation(self)-> float:
        return self.angle
    def getRotationFormat(self)-> float:
        return self.angle-90
    
    def getSpeed(self)-> tuple:
        return self.speed, self.baseSpeed, self.maxSpeed
        
    def getFriction(self)-> float:
        return self.friction
        
    def getDirections(self)-> tuple:
        return self.xDirection, self.yDirection

    def getLastShoot(self)-> float:
        return self.lastShoot
    def getRafaleCompt(self)-> int:
        return self.RafaleCompt
    
    def getLife(self)-> int:
        return self.lifes
    
    def getSize(self)-> int:
        return self.size

    def getInvincible(self)-> bool:
        return self.invincible
    
    def getScore(self)-> int:
        return self.score

    def getEngine(self)-> tuple:
        return self.engine, self.engineStatus, self.engineColor


    #=== Setters ===
    def move(self, x, y)-> None:
        '''
        Permet de déplaceer le joueur à la position x,y
        '''
        if 0<=self.x and self.x<=self.maxX-self.size:
            self.x=x
        else:
            if self.x<=0:
                self.x+=1
            if self.x>=self.maxX-self.size:
                self.x-=1

        if 0<=self.y and self.y<=self.maxY-self.size:
            self.y=y
        else:
            if self.y<=0:
                self.y+=1
            if self.y>=self.maxY-self.size:
                self.y-=1

    def setSpeed(self, s:float)-> None:
        '''
        Permet de changer la vitesse du joueur
        '''
        self.speed=s

    def setDirections(self, Dx, Dy)-> None:
        '''
        Permet de changer la direction x et y du joueur
        '''
        self.xDirection=Dx
        self.yDirection=Dy

    def setLastShoot(self, t)-> None:
        '''
        Permet de mettre à jour le timestamp du dernier laser tiré
        '''
        self.lastShoot=t
    def setRafaleCompt(self, i:int)-> None:
        '''
        Permet de mettre à jour le compteur de rafale
        '''
        self.RafaleCompt=i

    def setInvincible(self, state:bool)-> None:
        '''
        Permet de changer l'état d'invincibilité du joueur
        '''
        self.invincible=state
        
    def setLife(self, l:int)-> None:
        '''
        Permet de mettre à jour les points de vies du joueur
        '''
        self.lifes=l

    def setEngine(self, i:float)-> None:
        '''
        Permet de changer la valeur de l'engine du joueur
        '''
        if i>100:
            self.engine=100
        elif i<=0:
            self.engine=0
        else:
            self.engine=i
    def setEngineStatus(self, b:bool)-> None:
        '''
        Permet de changer l'état de l'engine du joueur
        '''
        self.engineStatus=b
        if self.engineStatus:
            self.engineColor=(230, 230, 230)
        else:
            self.engineColor=(168,52,58)

    def propulse(self, x, y)-> None:
        '''
        Permet de continuer le mouvement du joueur
        '''
        self.lastMove=(x,y)
        self.move(self.x+x*self.speed, self.y+y*self.speed)

    def rotate(self, r:float)-> None:
        '''
        Permet de changer la rotation du joueur
        '''
        self.angle+=r*self.rotSpeed

    def reset(self)-> None:
        '''
        Permet de réinitialiser partiellement le joueur
        '''
        self.setInvincible(True)
        self.move(self.maxX/2, self.maxY/2)
        self.setEngine(100)