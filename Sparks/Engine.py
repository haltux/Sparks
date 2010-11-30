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
import Colors 
import pygame
from pygame.locals import *

from Constants import *
import Game


def load_font(file, size):
    return pygame.font.Font(os.path.join(os.path.dirname(__file__), "data", "fonts", file), size)

def render_text(surface, text, font, pos, center=False):
    ren = font.render(text, (Colors.COLOR_DEPTH>8), (255, 255, 255))
    pos = [pos[0] - ren.get_width()/2, pos[1] - ren.get_height()/2]
    surface.blit(ren, pos)
    return ren

def load_highscore():
    return 0
#
#    f = os.path.expanduser(os.path.join("~",".sparks"))
#    if os.path.exists(f):
#        hs = open(os.path.expanduser(os.path.join("~",".sparks")), "rU").read()
#        return int(hs)
#    else:
#        hs = open(os.path.expanduser(os.path.join("~",".sparks")), "w").write(str(0))
#        return 0

def save_highscore(score):
    pass
    #open(os.path.expanduser(os.path.join("~",".sparks")), "w").write(str(score))



def generate_secure_pos():
    return random.choice((\
                         [random.randrange(0, SCREEN_WIDTH/3),random.randrange(0, SCREEN_HEIGHT)],\
                         [random.randrange(0, SCREEN_WIDTH/3)+SCREEN_WIDTH*2/3,random.randrange(0, SCREEN_HEIGHT)]))

def generate_pos():
    return [random.randrange(0, SCREEN_WIDTH),random.randrange(0, SCREEN_HEIGHT)]


def angle_to_target(pos1, pos2):
    x = pos2[0] - pos1[0]
    y = pos2[1] - pos1[1]
    angle = math.atan2(y, x)
    return int((angle * 180.0)/math.pi)


def angle_approach(a,b,speed):
    d= angle_diff(a,b)
    if d>speed:
        return a+speed
    else:
        if d<-speed:
            return a-speed
        else:
            return b


def approach(a,b,speed):
    if a < b-speed:
        return a+speed
    else:
        if a >b+speed:
            return a-speed
        else:
                return b

def angle_diff(a1,a2):
    diff = a2-a1
    while diff>180:
        diff-= 360
    while diff<-180:
        diff+=360
    return diff

def distance((x1,y1),(x2,y2)):
    return int(math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)))

def manhattan_distance((x1,y1),(x2,y2)):
    return abs(x2-x1)+abs(y2-y1)

def screen_reduction(v):
    return v*SCREEN_WIDTH/WORLD_WIDTH

def generate_rect((x1,y1),(x2,y2)):
    return pygame.Rect(min(x1,x2),min(y1,y2),abs(x1-x2),abs(y1-y2))
    

stars = []
for i in range(30):
    stars.append([random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)])

def Stars():
    return stars
#
#def rotate_points(self):
#    self.drawpoints = []
#    for p in self.points:
#        newX = int(p[0]*math.cos(math.radians(-self.__angle))*self.__scale - p[1]*math.sin(math.radians(-self.__angle))*self.__scale + self.pos[0])
#        newY = int(p[0]*math.sin(math.radians(-self.__angle))*self.__scale + p[1]*math.cos(math.radians(-self.__angle))*self.__scale + self.pos[1])
#        self.drawpoints.append((newX,newY))

def LifeImage(surface, pos):
    points = []
    for p in SHIP_NORMAL_POINTS:
        newX = int(p[0]*math.cos(math.radians(180))*0.6 - p[1]*math.sin(math.radians(180))*0.6 + pos[0])
        newY = int(p[0]*math.sin(math.radians(180))*0.6 + p[1]*math.cos(math.radians(180))*0.6 + pos[1])
        points.append((newX,newY))
    if Game.USE_ANTIALIAS:
        pygame.draw.aalines(surface,(255,255,255),1,points,DRAW_WIDTH)
    else:
        pygame.draw.lines(surface,(255,255,255),1,points,DRAW_WIDTH)


class Group(pygame.sprite.RenderPlain):
    def draw(self, surface):
        surface_blit = surface.blit
        for spr in self.sprites():
            if spr.light<255 or not PRECOMPUTE_SPRITES or (DO_NOT_PRECOMPUTE_BIG_SPRITES and spr.width>BIG_SPRITE_THRESHOLD*SPRITE_SCALE):
                spr.draw(surface)
            else:
                self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []      
        """
        
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            spr.image.set_alpha(spr.light)
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []
"""

    def update(self):
        for s in self.sprites():
            s.update()
            
class VectorialGroup(pygame.sprite.Group):

    def draw(self, surface):
        for s in self.sprites():
            s.draw(surface)

    def update(self):
        for s in self.sprites():
            s.update()
    

