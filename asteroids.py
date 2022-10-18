from random import randint, random, choice, uniform
import time

class Asteroid():
    def __init__(self, screenWidth, screenHeight, x=None, y=None, size=None)-> None:
        if x==None:
            self.x = screenWidth/2
        else:
            self.x=x
        if y==None:
            self.y = screenHeight/2
        else:
            self.y=y

        self.maxX=screenWidth
        self.maxY=screenHeight
        
        self.minSize=30
        self.maxSize=130
        if size==None:
            self.r = randint(60, self.maxSize)
        else:
            self.r=size

        self.speed_x=choice([x for x in range(-4, 4) if x!=0])
        self.speed_y=choice([x for x in range(-4, 4) if x!=0])
        self.color=(255, 255, 255)

        self.xDirection=random()
        self.yDirection=random()

        self.lastBounce=None

    #=== Getters ===
    def getCoord(self)-> tuple:
        return self.x, self.y

    def getSpeed(self)-> tuple:
        return self.speed_x, self.speed_y

    def getDirection(self)-> tuple:
        return self.xDirection, self.yDirection
    
    def getSize(self)-> float:
        return self.r


    #=== Setters ===
    def changeSpeed(self, x:float, y:float)-> None:
        '''
        Permet de changer précisément la vitesse x et y de l'astéroide
        '''
        if 1<self.speed_x<=5 or -5>=self.speed_x>-1:
            self.speed_x=x
        if 1<self.speed_y<=5 or -5>=self.speed_y>-1:
            self.speed_y=y
        
    def move(self)-> None:
        '''
        Permet de continuer le mouvement de l'astéroide
        '''
        if 0<=self.x-self.r and self.x+self.r<=self.maxX:
            self.x+=self.xDirection*self.speed_x
        else:
            self.speed_x*=-1
            self.x+=self.xDirection*self.speed_x
            
        if 0<=self.y-self.r and self.y+self.r<=self.maxY:
            self.y+=self.yDirection*self.speed_y
        else:
            self.speed_y*=-1
            self.y+=self.yDirection*self.speed_y

    def bounce(self, collider:object)-> None:
        '''
        Permet d'inverser le sens de direction de l'astéroide
        '''
        if self.lastBounce!=collider:
            self.speed_x*=-1
            self.speed_y*=-1
            self.xDirection=random()
            self.yDirection=random()
            self.lastBounce=collider
            
    def divide(self)-> list:
        '''
        Permet de diviser l'astéroide en 2 nouveaux astéroides enfants
        '''
        asteroidSize=self.r
        asteroidCoor=self.getCoord()

        #Nouvelle taille de l'enfant 1
        asteroidChild1Size=asteroidSize/uniform(1.8, 3.3)
        if asteroidChild1Size<self.minSize:
            asteroidChild1Size=self.minSize

        #Nouvelle taille de l'enfant 2
        asteroidChild2Size=asteroidSize/uniform(1.8, 3.3)
        if asteroidChild1Size<self.minSize:
            asteroidChild1Size=self.minSize


        #Nouvelle position de l'enfant 1
        possibleNewPos=[x for x in range(-self.maxSize, self.maxSize) if not -10+-max(asteroidChild1Size, asteroidChild2Size)<=x<=max(asteroidChild1Size, asteroidChild2Size)+10]
        newAsteroid1Pos=[asteroidCoor[0]+choice(possibleNewPos), asteroidCoor[1]+choice(possibleNewPos)]

        if newAsteroid1Pos[0]-asteroidChild1Size<=0:
            newAsteroid1Pos[0]=newAsteroid1Pos[0]+(asteroidChild1Size*2+20)
        elif newAsteroid1Pos[0]+asteroidChild1Size>=self.maxX:
            newAsteroid1Pos[0]=newAsteroid1Pos[0]-(asteroidChild1Size*2+20)

        if newAsteroid1Pos[1]-asteroidChild1Size<=0:
            newAsteroid1Pos[1]=newAsteroid1Pos[1]+(asteroidChild1Size*2+20)
        elif newAsteroid1Pos[1]+asteroidChild1Size>=self.maxY:
            newAsteroid1Pos[1]=newAsteroid1Pos[1]-(asteroidChild1Size*2+20)
        

        #Création des nouveaux enfants
        asteroidChild1=Asteroid(self.maxX, self.maxY, newAsteroid1Pos[0], newAsteroid1Pos[1], asteroidChild1Size)
        asteroidChild1Speed=asteroidChild1.getSpeed()
        asteroidChild1.changeSpeed(asteroidChild1Speed[0]*1.5, asteroidChild1Speed[1]*1.5)

        asteroidChild2=Asteroid(self.maxX, self.maxY, asteroidCoor[0], asteroidCoor[1], asteroidChild2Size)
        asteroidChild2Speed=asteroidChild2.getSpeed()
        asteroidChild2.changeSpeed(asteroidChild2Speed[0]*1.5, asteroidChild2Speed[1]*1.5)

        newAsteroids=[asteroidChild1, asteroidChild2]
        return newAsteroids
        

