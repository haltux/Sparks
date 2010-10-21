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
from Menu import *
from Sound import *
from Collider import  *
from Control import  *

import levels



STATE_BEGIN_LEVEL = 0
STATE_MAIN = 1
STATE_LEVEL_FINISHED = 2
STATE_DEATH = 3
STATE_END_LEVEL = 4
STATE_END_GAME = 5

MODE_ARCADE = 0
MODE_LEVEL = 1


class Game(object):
    instance = None
    def __new__(cls):
        if not Game.instance:
            Game.instance = object.__new__(cls)
        return Game.instance


    def initialize(self,screen,mode=MODE_ARCADE,diff=0,level=None):
        self.screen= screen
        self.mode = mode
        self.difficulty=diff
        self.chosen_level=level
        self.sprites = Group()
        self.clearables = Group()
        self.asteroids = Group()
        self.ufos = Group()
        self.playershots = Group()
        self.enemyshots = Group()
        self.enemies = Group()
        self.bulls = Group()
        self.cowards = Group()
        self.particles = VectorialGroup()      
        self.destroyables = Group()  


        Ship.containers = self.sprites
        PlayerShot.containers = self.sprites, self.playershots, self.clearables
        EnemyShot.containers = self.sprites, self.enemyshots, self.clearables
        Asteroid.containers = self.sprites, self.asteroids, self.enemies, self.clearables,self.destroyables
        Bull.containers = self.sprites, self.bulls, self.enemies, self.clearables,self.destroyables
        Coward.containers = self.sprites, self.cowards, self.enemies, self.clearables,self.destroyables
        Turner.containers = self.sprites, self.enemies, self.clearables,self.destroyables
        Particle.containers = self.particles
        MissileLauncher.containers = self.sprites, self.enemies, self.clearables,self.destroyables
        Missile.containers = self.sprites, self.enemies, self.clearables,self.destroyables
        Mine.containers = self.sprites, self.enemies, self.clearables,self.destroyables
        Miner.containers = self.sprites, self.enemies, self.clearables,self.destroyables
        CornerKeeper.containers = self.sprites, self.enemies, self.clearables
        
        self.collider = Collider()

        self.ship = Ship()
        self.paused = False

        self.clock = pygame.time.Clock()
        self.events = []

        self.num_level = 0


        self.score = 0
        if mode==MODE_ARCADE:
            self.lives = 5
        else:
            self.lives = 1
        self.done = False
        self.highscore = load_highscore()

        self.timer_restart = 0

        self.font = load_font("nasaliza.ttf", 20)
        self.font2 = load_font("nasaliza.ttf", 60)
        self.font3 = load_font("nasaliza.ttf", 30)
        load_sounds()

        self.state_timer=0;
        self.state=STATE_MAIN

        self.num_level = 0
        self.__new_level(self.num_level)

        self.text_end_game=[""]
        self.restart=False

    def clearSprites(self):
        for s in self.clearables:
            pygame.sprite.Sprite.kill(s)

    def killSprites(self):
        for s in self.clearables:
            s.kill()




    def __drawScene(self):
        self.screen.fill((0, 0, 0))
        for star in Stars():
            self.screen.set_at(star, (200, 200, 200))
        self.sprites.draw(self.screen)
        self.particles.draw(self.screen)
        render_text(self.screen, "Score: %06d" % self.score, self.font, (10, 10))
        render_text(self.screen, "High: %06d" % self.highscore, self.font, (SCREEN_WIDTH/2, 10),True)
        render_text(self.screen, "Level: %d" % self.num_level, self.font, (SCREEN_WIDTH-140, 10))
        for i in range(self.lives):
            LifeImage(self.screen, (20 + i*20, 50))
        if self.state==STATE_END_GAME:
            render_text(self.screen, self.text_end_game[0], self.font2, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2-40), True)
            i=1
            while i<len(self.text_end_game):
                render_text(self.screen, self.text_end_game[i], self.font3, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2+self.font3.get_height()*i), True)
                i+=1
        if self.state==STATE_MAIN and self.state_timer<50:
            render_text(self.screen, "Level "+str(self.num_level+1), self.font2, (SCREEN_WIDTH/2, SCREEN_HEIGHT/3), True)
        pygame.display.flip()

    def __gameInput(self):
        self.events = pygame.event.get()
        for e in self.events:
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if (e.type == KEYDOWN and e.key == K_ESCAPE) or (e.type == JOYBUTTONDOWN and e.button==JOY_ESCAPE):
                self.restart = False
                self.done = True

            if (e.type == KEYDOWN and e.key == K_p) or (e.type == JOYBUTTONDOWN and e.button==JOY_PAUSE):
                self.paused ^= 1
            if (e.type == KEYDOWN and e.key == K_SPACE) or (e.type == JOYBUTTONDOWN and e.button==JOY_FIRE):
                if self.state==STATE_END_GAME:
                    self.done = True                       
            if e.type == ACTIVEEVENT:
                if (e.state == 2 and e.gain == 0) or (e.state == 6 and e.gain == 0):
                    self.paused = True
                elif e.state == 6 and e.gain == 1:
                    self.paused = False

    def __updateGame(self):
        self.state_timer+=1
        self.level_timer+=1
        if self.state==STATE_MAIN:
            if not self.ship.alive():
                self.state_timer=0
                self.state=STATE_DEATH
                self.lives -= 1
#            self.level.process(self.level_timer)
            if not self.level.is_finished():
                self.level.process(self)
                if len(self.bulls)>MAX_BULL:
                    self.saturation_timer += 1
                    if self.saturation_timer%10==0:
                        oldest_bull = max(self.bulls,key=lambda b:b.timer+random.randint(0,200) if b.bulltype==Bull.BASIC else 0)
                        oldest_bull.change_type(Bull.BERZERKER)
                else:
                    self.saturation_timer = 0
            else:
                if not self.destroyables:
                    self.state_timer=0
                    self.state=STATE_LEVEL_FINISHED
        elif self.state==STATE_LEVEL_FINISHED:
            if self.state_timer>50:
                if self.mode==MODE_ARCADE:
                    self.num_level += 1
                    self.lives+=1
                    self.__new_level(self.num_level)
                    self.state_timer=0
                    self.state=STATE_MAIN
                else:
                    self.state_timer=0
                    self.text_end_game=["Congratulations!"]
                    self.text_end_game+=["You finished level \"" + str(self.level.name)+"\""]
                    self.text_end_game+=["with difficulty " + str(self.difficulty+1)]
                    self.text_end_game+=["","Try higher difficulty level!"]
                    self.restart = False
                    self.state=STATE_END_GAME

        elif self.state==STATE_DEATH:
            if self.state_timer>50:
                if self.lives>0:
                    self.ship = Ship()
                    self.state_timer=0
                    self.state=STATE_MAIN
                else:
                    if self.mode==MODE_ARCADE:
                        self.text_end_game=["Game Over"]
                        self.text_end_game+=[""]                        
                        self.text_end_game+=["You achieved a score of " + str(self.score)]
                        self.text_end_game+=["at difficulty " + str(self.difficulty+1)]
                    else:
                        self.text_end_game=["Try again!"]
                        self.restart = True                                              
                    self.state=STATE_END_GAME

    def __new_level(self,num_level):
        if self.mode==MODE_ARCADE:
            self.level=levels.get_next_level(num_level, self.difficulty)
        else:
            self.level=self.chosen_level
        self.level_timer =0
        self.ship.pos = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        self.ship.velocity = [0, 0]




    def __convert_oldest_bulls(self):
        to_remove=len(self.bulls)-MAX_BULL
        sorted_bulls = sorted(self.bulls,key=lambda b:-b.timer)
        for i,b in enumerate(sorted_bulls):
            if i<to_remove:
                b.kill()

    def __mainLoop(self):

        while not self.done:
            self.clock.tick(MAX_FPS)            
            self.sprites.update()
            self.particles.update()

            while self.paused: self.__gameInput()
            self.__gameInput()
            self.collider.DetectCollisions()

            self.__updateGame()
            self.__drawScene()
            
                
        

    def Run(self):
        self.__mainLoop()
        return self.restart