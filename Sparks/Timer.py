'''
Created on 24 nov. 2010

@author: Julien
'''

import pygame
import Constants

time = 0
clock = pygame.time.Clock() 


def get_frame_time():
    return min(clock.get_time(),50) 

def tick():
    global time,clock
    clock.tick(Constants.MAX_FPS)
    time += get_frame_time()

class Timer():

    def __init__(self):
        self.start_time=0
        self.reset_timer()

    def reset_timer(self):
        self.start_time = time 
            
    def get_timer(self):
        return time-self.start_time
    
class TimerManager():
    
    def __init__(self):
        self.timers={}
        
    def add_timer(self,timerId):
        self.timers[timerId]=Timer()
        self.timers[timerId].reset_timer()  
        
    def reset_timer(self,timerId):
        self.timers[timerId].reset_timer()
        
    def get_timer(self,timerId):
        return self.timers[timerId].get_timer()                