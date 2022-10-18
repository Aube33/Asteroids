class Laser():
    def __init__(self, x, y, xDirection, yDirection, screenWidth, screenHeight)-> None:
        self.x=x
        self.y=y

        self.maxX=screenWidth
        self.maxY=screenHeight

        self.speed=15

        self.xDirection=xDirection
        self.yDirection=yDirection

        self.color=(255,255,255)

        self.r=4

    #=== Getters ===
    def getCoord(self)-> tuple:
        return self.x, self.y

    def getSize(self)-> int:
        return self.r

    def getColor(self)-> tuple:
        return self.color


    #=== Setters ===
    def move(self)-> None:
        '''
        Permet de continuer le mouvement du laser
        '''
        if -200<=self.x and self.x<=self.maxX+200 or -200<=self.y and self.y<=self.maxY+200:
            #Sécurité au début du jeu pour les projectiles
            if self.xDirection==0 and self.yDirection==0:
                self.yDirection=0.01
                self.yDirection=-0.99

            self.x+=self.xDirection*self.speed
            self.y+=self.yDirection*self.speed