# Lanre Yakubu
# Slide and Catch game Part II
"""
Created on Nov  7, 2024
"""

import pygame
import simpleGE
import random

class Ball(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("soccerBall.png")
        self.setSize(25, 25)
        self.reset()
        self.ballSound = simpleGE.Sound("sound.mp3")
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(3, 8)

    def process(self):
        self.y += self.dy
        self.checkBounds()

    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class Character(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("player_0.png")
        self.setSize(60, 60)
        self.position = (300, 380)
        self.moveSpeed = 5
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (120, 30)
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 10"
        self.center = (500, 100)

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("storyboard.png")
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 10
        self.score = 0
        
        self.character = Character(self)
        self.balls = [Ball(self) for _ in range(3)]
        
        self.lblScore = LblScore()
        self.lblTime = LblTime()
        
        self.sprites = [self.character] + self.balls + [self.lblScore, self.lblTime]

    def process(self):
        
        for ball in self.balls:
            if ball.collidesWith(self.character):
                ball.ballSound.play()
                ball.reset()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
        
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        
        
        if self.timer.getTimeLeft() < 0:
            print(f"Final Score: {self.score}")
            self.stop()

class Instruction(simpleGE.Scene):
    def __init__(self, score):
        super().__init__()
        self.setImage("storyboard.png")
        
        self.response = "quit"
        
        
        self.instruction = simpleGE.MultiLabel()
        self.instruction.textLines = [
            "You are the character.",
            "Move with the left and right arrow keys",
            "and catch as much ball as you can",
            "in only ten seconds",
            "",
            "Good Luck!"
        ]
        
        self.instruction.center = (320, 240)
        self.instruction.size = (500, 250)
        
        
        self.prevScore = score
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Last score: {self.prevScore}"
        self.lblScore.center = (320, 50)
        
       
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play (up)"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit (down)"
        self.btnQuit.center = (550, 400)
        
        self.sprites = [self.instruction, self.lblScore, self.btnQuit, self.btnPlay]
        
    def process(self):
       
        if self.btnQuit.clicked:
            self.response = "quit"
            self.stop()
        if self.btnPlay.clicked:
            self.response = "play"
            self.stop()

        
        if self.isKeyPressed(pygame.K_UP):
            self.response = "play"
            self.stop()
        if self.isKeyPressed(pygame.K_DOWN):
            self.response = "quit"
            self.stop()

def main():
    keepGoing = True
    score = 0
    
    while keepGoing:
      
        instruction = Instruction(score)
        instruction.start()
        
        
        if instruction.response == "play":
            game = Game()
            game.start()
            score = game.score  
        else:
            keepGoing = False
            
if __name__ == "__main__":
    main()
