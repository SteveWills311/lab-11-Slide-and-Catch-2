"""
Steve Wills
11/10/24
Slide and Catch part 2
"""

import random, pygame, simpleGE

class Ball(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("golfball.png")
        self.setSize(25, 25)
        self.minSpeed = 5
        self.maxSpeed = 15
        self.reset()
        
    def reset(self):
        self.y = 15
        self.x = random.randint(15, 625)
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
            
class TinCup(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("tincup.png")
        self.setSize(75, 75)
        self.position = (320, 400)
        self.moveSpeed = 10
    
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
        if self.isKeyPressed(pygame.K_UP):
            self.y -= self.moveSpeed
        if self.isKeyPressed(pygame.K_DOWN):
            self.y += self.moveSpeed
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)

class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 10"
        self.center = (500, 30)

class Game(simpleGE.Scene):
        def __init__(self):
            super().__init__()
            self.setImage("BGC.png")
            self.sndBall = simpleGE.Sound("coin.wav")
            self.numBalls = 7
            self.score = 0
            self.lblScore = LblScore()
            self.timer = simpleGE.Timer()
            self.timer.totalTime = 10
            self.lblTime = LblTime()
            self.tinCup = TinCup(self)
            self.balls = []
            for i in range(self.numBalls):
                self.balls.append(Ball(self))
                
            #self.ball = Ball(self)
            self.sprites = [self.tinCup,
                            self.balls,
                            self.lblScore,
                            self.lblTime]
        
        def process(self):
            for ball in self.balls:
                if ball.collidesWith(self.tinCup):
                    ball.reset()
                    self.sndBall.play()
                    self.score += 1
                    self.lblScore.text = f"Score: {self.score}"
                    
            self.lblTime.text = f"Time left: {self.timer.getTimeLeft():.1f}"
            if self.timer.getTimeLeft() < 0:
                print(f"Score: {self.score}")
                self.stop()
            

class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        self.prevScore = prevScore
        
        self.setImage("BGC.png")
        self.response = "Quit"
                
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are a golf hole...",
        "All arrow keys move the hole",
        "You have 10 seconds to put as",
        "many balls in the hole as you can!",
        "Easiest Hole in One ever....."]
        self.directions.center = (320, 200)
        self.directions.size = (500, 250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score: 0"
        self.lblScore.center = (320, 400)
        
        self.lblScore.text = f"Last Score: {self.prevScore}"
        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]

       
    
 


    def process(self):
        if self.btnPlay.clicked:
           self.response = "Play"
           self.stop()
           
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()

def main():
    
    keepGoing = True
    lastScore = 0
    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        
        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
        else:
            keepGoing = False

if __name__ == "__main__":
    main()
            