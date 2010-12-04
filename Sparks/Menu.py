#! /usr/bin/env python
# Sparks - A vectorial shooter programmed by Haltux
# Copyright (C) 2010 Haltux
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


import sys, os
import math, random

import pygame
from pygame.locals import *

from Engine import *
from GameObjects import *
import Game
import levels
import Colors

NB_OPTIONS_DISPLAYED = 7

class MenuOption:

    def __init__(self, text, font, command):

        self.text = text
        self.font = font
        self.cmd = command
        self.selected = False


    def command(self):
        if self.cmd: self.cmd()

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def render(self, screen,num_line,nb_line):      
        if self.selected:
            ren = self.font.render(self.text, (Colors.COLOR_DEPTH>8), (255,255,255))
        else:
            ren = self.font.render(self.text, (Colors.COLOR_DEPTH>8), (175,175,175))
        pos = (SCREEN_WIDTH/2-ren.get_width()/2, SCREEN_HEIGHT/4*3 + (-nb_line/2+num_line)*self.font.get_height())            
        screen.blit(ren, pos)


class Menu(object):

    def __init__(self, screen,parent=None):
        self.parent=parent
        self.screen = screen
        self.options = []
        self.font = load_font("nasaliza.ttf", 30)
        self.font2 = load_font("nasaliza.ttf", 70)
        self.font3 = load_font("nasaliza.ttf", 20)
        self.all = Group()
        Asteroid.containers = self.all
        self.clock = pygame.time.Clock()
        self._define_menu_entries()
        self.options[0].select()
        self.option = 0
        self.axis_reset = True
        self.timer_last_move = 0 

    def _define_menu_entries(self):
        self.AddOption("Menu template", 0)

    def AddOption(self, text, command):
        option = MenuOption(text, self.font, command)
        self.options.append(option)

    def __moveDown(self):
        for o in self.options:
            o.selected = False
        self.option += 1
        if self.option >= len(self.options):
            self.option = 0
        self.options[self.option].select()

    def __moveUp(self):
        for o in self.options:
            o.selected = False
        self.option -= 1
        if self.option < 0:
            self.option = len(self.options)-1
        self.options[self.option].select()

    def __menuInput(self):
        self.events = pygame.event.get()
        for e in self.events:
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if (e.type == KEYDOWN and e.key == K_ESCAPE or e.type == KEYDOWN and e.key == K_PAGEUP or e.type == KEYDOWN and e.key == K_SYSREQ or e.type == JOYBUTTONDOWN and e.button==JOY_BACK):
                self._escape()
            if (e.type == KEYDOWN and e.key == K_UP):
                self.__moveUp()
            if (e.type == KEYDOWN and e.key == K_DOWN):
                self.__moveDown()
            if (e.type == KEYDOWN and e.key == K_RETURN or e.type == KEYDOWN and e.key == K_END or e.type == KEYDOWN and e.key == K_RETURN or e.type == JOYBUTTONDOWN and e.button==JOY_FIRE):
                self.options[self.option].command()
                    
        time = pygame.time.get_ticks()
        axis_value=getDirJoyYAxis()
        if abs(axis_value)>0.4 and (self.axis_reset or (time-self.timer_first_move>300 and time-self.timer_last_move>100)):
            self.timer_last_move=time
            if self.axis_reset:
                self.timer_first_move=time
                self.axis_reset=False                       
            if axis_value>0.4:
                self.__moveDown()
            if axis_value<-0.4:
                self.__moveUp()
        if axis_value>-0.2 and axis_value<0.2:
            self.axis_reset=True                   

               
            
    def __drawScene(self):
        pygame.display.flip()
        self.screen.fill((0, 0, 0))
        self.all.draw(self.screen)
        for star in Stars():
            self.screen.set_at(star, (200, 200, 200))
        first=max(0,min(self.option-NB_OPTIONS_DISPLAYED+2,len(self.options)-NB_OPTIONS_DISPLAYED))
        i=first
        while i<min(first+NB_OPTIONS_DISPLAYED,len(self.options)):
            self.options[i].render(self.screen,i-first, min(len(self.options),NB_OPTIONS_DISPLAYED))
            i+=1
        render_text(self.screen, "Sparks", self.font2, (SCREEN_WIDTH/2, SCREEN_HEIGHT/4), True)
        render_text(self.screen, "By HalTux", self.font3, (SCREEN_WIDTH/2, SCREEN_HEIGHT/3), True)
        
    def _escape(self):
        if self.parent!=None:
            self.parent.Run()
            
        
    def loop(self):
        
        while 1:
            self.clock.tick(60)
            self.all.update()
            self.__menuInput()
            self.__drawScene()

    def Run(self):
        self.loop()
        
class MainMenu(Menu):

    def __init(self,screen,parent=None):
        Menu.__init__(self, screen, parent)

    def _define_menu_entries(self):
        self.AddOption("Arcade Mode", self.__choose_difficulty)
        self.AddOption("Custom Levels", self.runCustomLevels)
        self.AddOption("Quit Game", self.quitGame)

        
    def __choose_difficulty(self): 
        DifficultyMenu(self.screen,parent=self).Run()    

    def quitGame(self): 
        pygame.quit()
        sys.exit()     
        
    def runCustomLevels(self):
        CustomLevelMenu(self.screen,parent=self).Run()
        
    def start_game(self,diff):
        game = Game.Game()
        game.initialize(self.screen,Game.MODE_ARCADE,diff)    
        game.Run()
          
        
class CustomLevelMenu(Menu):
    def _define_menu_entries(self):
        for level in levels.CUSTOM_LEVELS:
            self.AddOption(level.name, self.__choose_difficulty_command(level))
        self.AddOption("back", self._escape)

    def __choose_difficulty(self,level): 
        self.level=level
        DifficultyMenu(self.screen,parent=self).Run()    
        
    def __choose_difficulty_command(self,level):
        return (lambda :self.__choose_difficulty(level)) 
        
    def start_game(self,diff):
        replay=True
        while (replay):
            game = Game.Game()
            game.initialize(self.screen,Game.MODE_LEVEL,diff,self.level(diff))
            replay = game.Run()
                      

class DifficultyMenu(Menu):
    def _define_menu_entries(self):
        strDiffs=["Easy","Normal","Hard","Very hard"]
        for i in range(0,4):
            self.AddOption(strDiffs[i], self.__set_difficulty_command(i))
        self.AddOption("back", self._escape)
        
    def __set_difficulty_command(self,diff):
        return (lambda :self.parent.start_game(diff))
    
    
 


