import random

class Emitter():
    def __init__(self, x, y, screenWidth, screenHeight)-> None:
        self.x=x
        self.y=y

        self.maxX=screenWidth
        self.maxY=screenHeight

    #=== Getters ===
    def getCoord(self)-> tuple:
        return self.x, self.y

        
    #=== Particles ===
    def Explosion(self, amount:int, speed:float, color:tuple, size:int)-> list:
        '''
        Permet de faire des particules d'explosion unicolore
        '''
        return [Particle(self.x, self.y, speed, color, size) for _ in range(amount)]

    def Explosionjeb_(self, amount:int, speed:float, size:int)-> list:
        '''
        Permet de faire des particules d'explosion multicolore
        '''
        return [Particle(self.x, self.y, speed, [random.randint(0,255) for _ in range(3)], size) for _ in range(amount)]

    def ExplosionFlame(self, amount:int, speed:float, size:int)-> list:
        '''
        Permet de faire des particules d'explosion aux couleurs de flammes
        '''
        return [Particle(self.x, self.y, speed, random.choice([(230, 41, 41), (222, 96, 42), (222, 162, 42)]), size) for _ in range(amount)]



class Particle():
    def __init__(self, x, y, speed:float, color:tuple, size:int):
        self.x=x
        self.y=y

        self.origin=(x,y)

        self.speed=speed

        self.xDirection=random.random()*random.choice([-1, 1])
        self.yDirection=random.random()*random.choice([-1, 1])

        self.color=color
        self.distanceToLive=random.randint(50, 220)
        self.r=size

    #=== Getters ===
    def getCoord(self)-> tuple:
        return self.x, self.y

    def getSize(self)-> int:
        return self.r

    def getColor(self)-> tuple:
        return self.color

    def getOrigin(self)-> tuple:
        return self.origin

    def getDTL(self)-> int:
        '''
        Permet de récupérer la variable distanceToLive du joueur. (DTL=La distance maximum d'éloignement de son point source)
        '''
        return self.distanceToLive


    #=== Setters ===
    def move(self)-> None:
        '''
        Permet de continuer le mouvement de la particule
        '''
        self.x+=self.xDirection*self.speed
        self.y+=self.yDirection*self.speed