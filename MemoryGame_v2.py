import time
import thumby
import math

from sys import path as syspath
syspath.append("/Games/MemoryGame") #fix imports
import ThumbyEngine
import random

class ScoreKeeper:
    score: int
    bPlayerWon: bool
    

G_BLACKBOARD = ScoreKeeper()


class InputScores(ThumbyEngine.Level):
    def init(self, _engine):
        self.engine = _engine
        global G_BLACKBOARD
        self.engine.visuals.set_text("Game over!")
        thumby.display.drawText("Score: ", 0, 8, 1)
        thumby.display.drawText(str(G_BLACKBOARD.score), 30, 8, 1)
        instructions = "[A] Reset Game"
        thumby.display.drawText(instructions, 10, 28, 1)
        
    def update(self):
        if thumby.buttonA.justPressed():
            thumby.reset()
            
    def save(self):
        pass


class Game(ThumbyEngine.Level):
    
    cards = {
        thumby.buttonL: "<=", 
        thumby.buttonR: "=>", 
        thumby.buttonU: "/\\", 
        thumby.buttonD: "\/", 
        thumby.buttonA: "A", 
        thumby.buttonB: "B"
    }
    input_window = 5
    flash = 1.5
    score = 0
    phases = ["flash", "wait", "input"]
    current_phase = "flash"
    sequence = []
    input_sequence = []
    sequence_length = 3
    multipler = 0.5
    time_up = False
    time_started = False
    
    def init(self, _engine):
        self.engine = _engine
        self.card_y = self.engine.visuals.y_center
        self.card_x = self.engine.visuals.x_center - 5
        
    def update(self):
        if self.current_phase == "flash":
            self.engine.visuals.flash_screen("white")
            self.engine.visuals.flash_screen("black")
            card = random.choice(list(self.cards.values()))
            self.sequence.append(card)
            self.engine.visuals.clear_all()
            self.engine.visuals.set_text_loc(self.card_x, self.card_y)
            self.engine.visuals.set_text(card)
            self.current_phase = "wait"
            return
        elif self.current_phase == "wait":
            time.sleep(self.flash)
            if len(self.sequence) == self.sequence_length:
                self.current_phase = "input"
            else:
                self.current_phase = "flash"
            return
        else:
            # Start Input Mode
            if self.time_started is False:
                self.engine.visuals.clear_all()
                self.engine.visuals.set_text("Input the sequence!")
                self.engine.visuals.set_text_loc(0,0)
                self.timer = ThumbyEngine.SimpleTimer()
                self.timer.start(self.input_window, self.SequenceTimeUp)
                self.time_started = True
                return
            # Continue Input Mode
            if self.time_up is False:
                # get time remaining so we can print it to screen
                self.engine.visuals.clear_all()
                self.engine.visuals.set_text("Input the sequence!")
                self.engine.visuals.set_text_loc(0,0)
                
                # get input
                if thumby.buttonA.justPressed():
                    self.input_sequence.append("A")
                if thumby.buttonB.justPressed():
                    self.input_sequence.append("B")
                if thumby.buttonU.justPressed():
                    self.input_sequence.append("/\\")
                if thumby.buttonD.justPressed():
                    self.input_sequence.append("\/")
                if thumby.buttonL.justPressed():
                    self.input_sequence.append("<=")
                if thumby.buttonR.justPressed():
                    self.input_sequence.append("=>")
                
                # Print the player's input to the screen
                self.PrintSequenceToScreen()
                
                # Check if win or loss condition met
                if len(self.input_sequence) == len(self.sequence):
                    
                    del self.timer
                    
                    if self.input_sequence == self.sequence:
                        self.BlackboardUpdate(True)
                        self.PrintMessageToScreen("Correct! +1")
                        self.score += 1
                        time.sleep(2.5)
                        self.ResetLoop()
                        return
                    
                    else:
                        self.BlackboardUpdate(False)
                        self.PrintMessageToScreen("Incorrect!")
                        time.sleep(2.5)
                        i = InputScores()
                        self.engine.set_level(i)
                        return
                
                # If win/loss condition not met, update timer
                self.timer.update()
                return
            # If timer fired, then handle this loss condition
            if self.time_up is True:
                self.BlackboardUpdate(False)
                self.PrintMessageToScreen("Time Up!")
                thumby.display.update()
                time.sleep(2.5)
                i = InputScores()
                self.engine.set_level(i)
                return
    
    def SequenceTimeUp(self):
        if self.time_up is False:
            self.time_up = True
        else:
            self.time_up = False
        self.time_started = False
    
    def PrintSequenceToScreen(self):
        self.engine.visuals.fill_screen("black")
        time_remaining = str(self.timer.time_remaining() / 1000)
        thumby.display.drawText(
            time_remaining, 
            (self.engine.visuals.x_center - 3),
            (self.engine.visuals.y_center + 10),
            1
        )
        msg = ""
        for x in self.input_sequence:
            msg += x
        thumby.display.drawText(msg, 0, 8, 1)
    
    def PrintMessageToScreen(self, msg):
        thumby.display.drawText(msg, 0, 17, 1)
        thumby.display.update()
        
    def BlackboardUpdate(self, _result: bool):
        global G_BLACKBOARD
        G_BLACKBOARD.bPlayerWon = _result
        G_BLACKBOARD.score = self.score
    
    def IncreaseDifficulty(self):
        self.sequence_length += 1
        self.flash -= 0.3
        
    def ResetLoop(self):
        self.IncreaseDifficulty()
        self.time_started = False
        self.time_up = False
        self.current_phase = "flash"
        self.sequence = []
        self.input_sequence = []


class MainMenu(ThumbyEngine.Level):
    
    def constructMenu(self):
        # TO DO - load high scores
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        title = "-MEMORY BONANZA-"
        thumby.display.drawText(title, 5, 2, 1)
        # s1 = "Top Score 1"
        # thumby.display.drawText(s1, 0, 8, 1)
        # s2 = "Top Score 2"
        # thumby.display.drawText(s2, 0, 14, 1)
        # s3 = "Top Score 3"
        # thumby.display.drawText(s3, 0, 20, 1)
        instructions = "[A] Start Game"
        thumby.display.drawText(instructions, 10, 28, 1)
    
    def init(self, _engine):
        self.engine = _engine
        self.constructMenu()
    
    def update(self):
        if thumby.buttonA.justPressed():
            g = Game()
            self.engine.set_level(g)
            return
        

def main():
    e = ThumbyEngine.ThumbyEngine()
    l = MainMenu()
    e.set_level(l)
    e.set_default_level(l)
    e.run()

  
main()
