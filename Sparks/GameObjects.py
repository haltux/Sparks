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
from Constants import *

from Sound import *

from Control import *

import Colors

import Timer

ANGLE_PRECISION = 8
FADE_PRECISION = 8

class Sprite(pygame.sprite.Sprite):

    __map_pcimages={}
    __map_pcdrawpoints={}
    __map_pcrects={}
    __map_pcwidth={}

    def __init__(self,pos, points, scale=1,color=Colors.COLOR_WHITE):
        
        pygame.sprite.Sprite.__init__(self)
        self.__points = points
        self.__scale = SPRITE_SCALE*scale
        self.color = color
        self.light = 255
        (self.sx,self.sy) = pos
        (self.x,self.y)= (screen_reduction(self.sx),screen_reduction(self.sy))
        (self.old_x,self.old_y) = (self.x,self.y)
        (self.old2_x,self.old2_y) = (self.x,self.y)
        
        self.angle=0
        
        
        for group in [self.containers]:
            self.add(group)

        self.timer = Timer.Timer()
        self.last_call_compute_drawpoints = -1
        self.vx = 0
        self.vy = 0

        self.adrawpoints=[(0,0) for _ in range(0,len(points))]

        self.__precompute_images()
        self.__update_rect()
        self.__update_drawpoints()

    def set_initial_points(self):
        raise TypeError("get_initial_points should be implemented")

    def set_initial_position(self):
        raise TypeError("get_initial_points should be implemented")

    def change_points(self,points):
        self.__points = points
        self.__precompute_images()

    def change_color(self,color):
        self.color = color
        self.__precompute_images()

    def turn(self,angle):
        self.angle=self.angle+angle *   GLOBAL_SPEED * Timer.get_frame_time() / 1000

    def get_scale(self):
        return self.__scale
    
    def get_image_hash(self):
        return hash((self.__points,self.color,self.__scale))

    def __get_precomputed_drawpoints(self,angle):
        return self.__pcdrawpoints[(int(self.angle)%360)/ANGLE_PRECISION]
#
#    def __get_precomputed_rect(self,angle):
#        return self.__pcrects[(int(self.angle)%360)/ANGLE_PRECISION]

    def __get_precomputed_image(self,angle):
        return self.__images[(int(self.angle)%360)/ANGLE_PRECISION]

    def compute_drawpoints(self):
        if self.timer.get_timer()>self.last_call_compute_drawpoints:
            self.drawpoints=[]
            for p in self.__points:
                newX = int(p[0]*math.cos(math.radians(self.angle))*self.get_scale() - p[1]*math.sin(math.radians(self.angle))*self.get_scale())+self.x
                newY = int(p[0]*math.sin(math.radians(self.angle))*self.get_scale() + p[1]*math.cos(math.radians(self.angle))*self.get_scale())+self.y
                self.drawpoints.append((newX,newY))
            self.last_call_compute_drawpoints=self.timer.get_timer()
            


    def __precompute_images(self):
        h = self.get_image_hash()
        if h in Sprite.__map_pcimages:
            self.__images=Sprite.__map_pcimages[h]
            self.__pcdrawpoints=Sprite.__map_pcdrawpoints[h]
            self.__pcrects=Sprite.__map_pcrects[h]
            self.width = Sprite.__map_pcwidth[h]
        else:
            self.__images=[]
            
            radius=0
            for p in self.__points:            
                radius=max(radius,int(math.sqrt(p[0]*p[0]+p[1]*p[1])*self.get_scale())+1)
            
            self.width = radius*2+1
            self.__pcdrawpoints=[]
            self.__pcrects=[]
            
            for angle in range(0,360,ANGLE_PRECISION):
                image = pygame.surface.Surface(( self.width, self.width))
                rdrawpoints=[]               
                for p in self.__points:
                    newX = int(p[0]*math.cos(math.radians(angle))*self.get_scale() - p[1]*math.sin(math.radians(angle))*self.get_scale())+radius
                    newY = int(p[0]*math.sin(math.radians(angle))*self.get_scale() + p[1]*math.cos(math.radians(angle))*self.get_scale())+radius
                    rdrawpoints.append((newX,newY))

                xl = [x for (x,_) in rdrawpoints]
                yl = [y for (_,y) in rdrawpoints]
                
                self.__pcrects.append((min(xl),min(yl),max(xl)-min(xl),max(yl)-min(yl)))
                self.__pcdrawpoints.append(rdrawpoints)

                if Game.USE_ANTIALIAS:
                    pygame.draw.aalines(image,Colors.get_color_def(self.color),1,rdrawpoints,DRAW_WIDTH)
                else:
                    pygame.draw.lines(image,Colors.get_color_def(self.color),1,rdrawpoints,DRAW_WIDTH)
                    
                print(self.color)
                    
                image.set_colorkey(Colors.COLOR_BLACK)
                self.__images.append(image)

                
            Sprite.__map_pcimages[h] = self.__images
            Sprite.__map_pcwidth[h] = self.width
            Sprite.__map_pcdrawpoints[h] = self.__pcdrawpoints
            Sprite.__map_pcrects[h] = self.__pcrects
            
            

#            
#            self.__pcdrawpoints=[]
#            self.__pcrects=[]
# 
#            for angle in range(0,360,ANGLE_PRECISION):
#                rdrawpoints=[]
#                for p in self.__points:
#                    newX = int(p[0]*math.cos(math.radians(angle))*self.get_scale() - p[1]*math.sin(math.radians(angle))*self.get_scale())
#                    newY = int(p[0]*math.sin(math.radians(angle))*self.get_scale() + p[1]*math.cos(math.radians(angle))*self.get_scale())
#                    rdrawpoints.append((newX,newY))
#
#                xl = [x for (x,_) in rdrawpoints]
#                yl = [y for (_,y) in rdrawpoints]
#                
#                newImage = pygame.surface.Surface((20,20))
#                
#                self.__pcrects.append((min(xl),min(yl),max(xl)-min(xl),max(yl)-min(yl)))
#                self.__pcdrawpoints.append(rdrawpoints)
#            Sprite.__map_pcdrawpoints[self.__points] = self.__pcdrawpoints
#            Sprite.__map_pcrects[self.__points] = self.__pcrects


    def draw(self, surface):
        self.adrawpoints=[]
        xc=self.x-self.width/2
        yc=self.y-self.width/2
        for (x,y) in self.__get_precomputed_drawpoints(self.angle):
            self.adrawpoints.append((xc+x,yc+y))
        if Game.USE_ANTIALIAS:
            pygame.draw.aalines(surface,Colors.generate_shade(self.color, self.light),1,self.adrawpoints,DRAW_WIDTH)
        else: 
            pygame.draw.lines(surface,Colors.generate_shade(self.color, self.light),1,self.adrawpoints,DRAW_WIDTH)



    def __update_rect(self):
#        pass
#        current_rrect = self.__get_precomputed_rect(self.angle)
#        self.rect = Rect(screen_reduction(current_rrect[0]+self.sx),screen_reduction(current_rrect[1]+self.sy),screen_reduction(current_rrect[2]),screen_reduction(current_rrect[3]))
        self.rect = Rect(self.x-self.width/2,self.y-self.width/2,self.width,self.width)
    def __update_drawpoints(self):
#        self.adrawpoints=[]
#        for (x,y) in self.__get_precomputed_drawpoints(self.angle):
#            self.adrawpoints.append((screen_reduction(self.sx+x),screen_reduction(self.sy+y)))
        self.image = self.__get_precomputed_image(self.angle)

    def update(self):
        if not self.isBlocked():
            self.sx += self.vx *   GLOBAL_SPEED * Timer.get_frame_time() / 1000
            self.sy += self.vy *   GLOBAL_SPEED * Timer.get_frame_time() / 1000

        self.old2_x = self.old_x
        self.old2_y = self.old_y

        self.old_x = self.x
        self.old_y = self.y

        self.x = screen_reduction(self.sx)
        self.y = screen_reduction(self.sy)

        self._checkLimits()
        self.__update_rect()
        self.__update_drawpoints()


    def _checkLimits(self):
        if self.sx > WORLD_WIDTH:
            self.sx = WORLD_WIDTH-1
            if self.vx>0:
                self._bounce_x()
        if self.sx < 0:
            self.sx = 1
            if self.vx<0:
                self._bounce_x()
        if self.sy > WORLD_HEIGHT:
            self.sy = WORLD_HEIGHT-1
            if self.vy>0:
                self._bounce_y()
        if self.sy < 0:
            self.sy = 1
            if self.vy<0:
                self._bounce_y()

    def _bounce_x(self):
        self.vx = -self.vx

    def _bounce_y(self):
        self.vy = -self.vy


    def get_color(self):
        return self.color

    def isBlocked(self):
        return False
    
    def distance(self,other_sprite):
        return distance((self.sx,self.sy),(other_sprite.sx,other_sprite.sy))
    
    def manhattan_distance(self,other_sprite):
        return manhattan_distance((self.sx,self.sy),(other_sprite.sx,other_sprite.sy))
    

class Ship(Sprite):

    def __init__(self):

        Sprite.__init__(self, pos=(WORLD_WIDTH/2, WORLD_HEIGHT/2),points=SHIP_ACCEL_POINTS,color=Colors.COLOR_WHITE)
        self.vx = 0
        self.vy = 0
        self.shot_delay = 200
        self.timer_previous_shot = 0
        self.speed = 3
        self.shooting_angle =0
        self.is_shooting = False

#    def draw(self,surface):
#        if (not self.is_invincible()) or (self.timer/5)%2:
#            pygame.draw.polygon(surface,self.get_color(),self.adrawpoints,0)


    def is_invincible(self):
        return self.timer.get_timer()<1500

    def update(self):
        Sprite.update(self)


 
        joyX1 = int(getDirJoyXAxis()*256)*self.speed
        joyY1 = int(getDirJoyYAxis()*256)*self.speed
        self.vx = joyX1
        self.vy = joyY1
        
        disp = int(math.sqrt(self.vx*self.vx+self.vy*self.vy)/16) #disp between 0 and 256
        

        
        if abs(joyX1)+abs(joyY1)>50:
            self.angle=angle_to_target((0,0),(joyX1,joyY1))
            for i in range(0,3):
                pass#Particle((self.sx+random.randint(-1000,1000),self.sy+random.randint(-1000,1000)),(-self.vx/8+random.randint(0,disp*2)-disp,-self.vy/8+random.randint(0,disp*2)-disp))


        joyX2 = int(getFireJoyXAxis()*256)
        joyY2 = int(getFireJoyYAxis()*256)
        if abs(joyX2)+abs(joyY2)>120:
            self.is_shooting=True
            if self.timer.get_timer() - self.timer_previous_shot>=self.shot_delay:
                self.timer_previous_shot = self.timer.get_timer()
                play_shoot()
                self.shooting_angle  = angle_to_target((0,0),(joyX2,joyY2))

                PlayerShot((self.sx,self.sy),self.shooting_angle)
                PlayerShot((self.sx,self.sy),self.shooting_angle+10)
                PlayerShot((self.sx,self.sy),self.shooting_angle-10)
        else:
            self.is_shooting=False


    def kill(self):
        pygame.sprite.Sprite.kill(self)
        for i in range(100):
            Particle((self.sx,self.sy),life_length=1000)
            


class Shot(Sprite):

    def __init__(self, pos, angle):
        Sprite.__init__(self,pos,SHOT_POINTS)

        self.color = Colors.COLOR_WHITE

        self.speed = 4000
        self.nose_distance = 2048
        self.life = 1000
        
        self.angle = angle
        self.direction = angle
        
        self.vx = int(self.speed*math.cos(math.radians(self.direction)))
        self.vy = int(self.speed*math.sin(math.radians(self.direction)))


    def update(self):
        Sprite.update(self)

        self.life -= Timer.get_frame_time()
        if self.life <= 0:
            pygame.sprite.Sprite.kill(self)

    def _bounce_x(self):
        self.kill()

    def _bounce_y(self):
        self.kill()


    def kill(self):
        pygame.sprite.Sprite.kill(self)
        for i in range(5):
            Particle((self.sx,self.sy))

class EnemyShot(Shot):
    def __init__(self,pos,angle):
        Shot.__init__(self, pos, angle)
        self.speed = 800
        self.life = 200


class PlayerShot(Shot):
    def __init__(self,pos,angle):
        Shot.__init__(self, pos, angle)
        self.speed = 3000
        self.life = 300
        



class Enemy(Sprite):

    def __init__(self,pos,points,scale=1,color=Colors.COLOR_LIGHT_BLUE,appearance_delay=APPEARANCE_DELAY):
        Sprite.__init__(self,pos,points,scale,color)
        self.hitpoints=1
        self.color = color      
        self.appearance_delay=appearance_delay
        self.light = 0
        self.reward = 1


    def update(self):
        Sprite.update(self)
        if self.timer.get_timer() < self.appearance_delay:
            self.light = self.timer.get_timer()*255/self.appearance_delay
        else:
            self.light = 255
#            self.image = self.stored_image
#        else:
#            self.image=self.ghost_image

    def get_reward(self):
        return self.reward;

    def hit(self):
        self.hitpoints-=1
        if self.hitpoints<=0:
            self.kill()

    def kill(self):
        Sprite.kill(self)
        Game.Game().score += self.get_reward()        
        for i in range(20):
            Particle((self.sx,self.sy))

    def isActive(self):
        return (self.timer.get_timer() >= self.appearance_delay)
    
    def isBlocked(self):
        return not self.isActive()

  

#        self.rect.center = (self.x,self.sy)

class Mine(Enemy):
    def __init__(self,pos):
        Enemy.__init__(self,pos,BULL_POINTS,scale=0.3,color=Colors.COLOR_LIGHT_RED)
        self.vx=0
        self.vy=0
        self.reward = 100
        
    def update(self):
        Enemy.update(self)
        if self.timer.get_timer()>5000:
            self.explode()
        
    def explode(self):
        for angle in range(0,360,30):
            EnemyShot((self.sx,self.sy),angle)
        Enemy.kill(self)
            

        

class Asteroid(Enemy):

    def __init__(self, pos,direction=random.randrange(0,360),size=3,appearance_delay=APPEARANCE_DELAY):
        Enemy.__init__(self,pos,random.choice([ASTEROID1_POINTS, ASTEROID3_POINTS, ASTEROID4_POINTS]),scale=[0.5,0.8,1.5][size-1],appearance_delay=appearance_delay)

        self.direction = direction
        self.size = size
        self.hitpoints = self.size*self.size
        self.speed = [1500,1000,500][size-1]

        self.setVelocity()
        self.reward = 30 * self.size
        self.self_rotation_speed = float(random.randrange(-10/size,10/size))

    def setVelocity(self):
        self.vx = int(math.cos(math.radians(self.direction))*self.speed)
        self.vy = int(math.sin(math.radians(self.direction))*self.speed)

    def update(self):
        Enemy.update(self)
        self.turn(self.self_rotation_speed)


    def isActive(self):
        return True




    def hit(self):
        self.hitpoints-=1
        if self.hitpoints==0:
            self.kill()
            if self.size==3:
                Asteroid((self.sx-4000, self.sy-4000), direction=random.randrange(210, 330),size=2,appearance_delay=0)
                Asteroid((self.sx+4000, self.sy+4000), direction = random.randrange(30, 150),size=2,appearance_delay=0)
            elif self.size==2:
                    Asteroid((self.sx, self.sy-3000), direction=random.randrange(210, 330),size=1,appearance_delay=0)
                    Asteroid((self.sx+3000, self.sy+3000), direction=random.randrange(0, 90),size=1,appearance_delay=0)
                    Asteroid((self.sx-3000, self.sy+3000), direction=random.randrange(90, 180),size=1,appearance_delay=0)
            else:
                for i in range(15):
                    Particle((self.sx,self.sy))

class DirectionalEnemy(Enemy):
    def __init__(self,pos,points,scale=1,color=Colors.COLOR_LIGHT_BLUE,update_speed=False,appearance_delay=APPEARANCE_DELAY):
        Enemy.__init__(self,pos,points,scale,color,appearance_delay)

        self.refresh_time=251
        
        self.speed = 1
        self.target_speed = 1        
        self.rotation_speed=75
        self.acceleration=150
        self.target_direction = 0
        self.direction = 0

        self.update_speed = update_speed
        self.stopped = False
        
        self.refreshing_timer=Timer.Timer()

    def update(self):
        Enemy.update(self)
        self.direction = angle_approach(self.direction,self.target_direction,self.rotation_speed*   GLOBAL_SPEED * Timer.get_frame_time() / 1000)
        
        if self.update_speed:
            self.speed = approach(self.speed,self.target_speed,self.acceleration *   GLOBAL_SPEED * Timer.get_frame_time() / 1000)

        if self.stopped==True:
            self.vx = 0
            self.vy = 0
        else:
            self.vx = int(math.cos(math.radians(self.direction))*self.speed)
            self.vy = int(math.sin(math.radians(self.direction))*self.speed)

        if self.refreshing_timer.get_timer()>self.refresh_time:
            self.update_target()
            self.refreshing_timer.reset_timer()


    def _bounce_x(self):
        self.direction = 180 - self.direction

    def _bounce_y(self):
        self.direction = - self.direction

    def update_target(self):
        raise TypeError("Please overload update_target")
    
    def stop(self):
        self.stopped = True;
        
    def run(self):
        self.stopped = False;

class PathFollowerEnemy(DirectionalEnemy):
    def __init__(self,pos,path,random_target=False):
        DirectionalEnemy.__init__(self,pos,BULL_POINTS,color=Colors.COLOR_YELLOW)
        self.path=path
        
        self.random_target = random_target
        if random_target:
            self.num_target = random.randint(0,len(self.path)-1)
        else:
            self.num_target=0
        self.target=self.path[self.num_target]        
    
    def update(self):
        DirectionalEnemy.update(self)
    
    def update_target(self):
        if abs(self.sx-self.target[0])+abs(self.sy-self.target[1])<4000:
            if self.random_target:
                self.num_target = random.randint(0,len(self.path)-1)
            else:
                self.num_target=(self.num_target+1)%len(self.path)
            self.target=self.path[self.num_target]
        self.target_direction=angle_to_target((self.sx,self.sy), self.target)
        
class Miner(PathFollowerEnemy):
    def __init__(self,pos,path=[(WORLD_WIDTH/5,WORLD_HEIGHT/5),(WORLD_WIDTH/5*4,WORLD_HEIGHT/5),(WORLD_WIDTH/5*4,WORLD_HEIGHT/5*4),(WORLD_WIDTH/5,WORLD_HEIGHT/5*4),]):
        PathFollowerEnemy.__init__(self,pos,path,random_target=True)
        self.speed=400
        self.reward = 200
        self.mining_timer=Timer.Timer()
        
    def update(self):
        PathFollowerEnemy.update(self)
        if self.mining_timer.get_timer()>1000:
            Mine((self.sx,self.sy))
            self.mining_timer.reset_timer()
        

class BullType:
    def __init__(self,name,speed,rotation_speed,color):
        self.name=name
        self.speed=speed
        self.rotation_speed=rotation_speed
        self.color=color

class Bull(DirectionalEnemy):
    BASIC=BullType("basic",400,75,Colors.COLOR_LIGHT_BLUE)
    BERZERKER=BullType("berzerker",1000,8,Colors.COLOR_LIGHT_RED)

    
    def __init__(self,pos,bulltype=BASIC,speed_factor=100):
        DirectionalEnemy.__init__(self,pos,BULL_POINTS,color=bulltype.color,update_speed=False)

        self.bulltype = bulltype
        self.speed_factor = speed_factor 
        self.speed = bulltype.speed * speed_factor/100 
        self.rotation_speed = bulltype.rotation_speed * speed_factor/100 

        self.type = bulltype.name
        
        self.is_merging = False
        self.partner = None
        
        if (bulltype==self.BASIC):
            self.reward = 10
        else:
            self.reward = 50

    def change_type(self,bulltype):
        self.bulltype= bulltype

        self.speed = bulltype.speed  * self.speed_factor/100 
        self.rotation_speed = bulltype.rotation_speed * self.speed_factor/100 
        
        self.change_color(bulltype.color)
        
        if (bulltype==self.BASIC):
            self.reward = 10
        else:
            self.reward = 50


    def update(self):
        DirectionalEnemy.update(self)
        self.angle=self.angle + 3.0  *   GLOBAL_SPEED * Timer.get_frame_time() / 1000
        if self.is_merging:
            if self.distance(self.partner)<self.speed+self.partner.speed or not self.partner.alive():
                self.hitpoints+=self.partner.hitpoints
                self.sx=(self.sx+self.partner.sx)/2
                self.sy=(self.sy+self.partner.sy)/2
                Sprite.kill(self.partner)
                self.is_merging=False
                self.rotation_speed=self.standard_rotation_speed 
                self.speed=self.standard_speed                


    def update_target(self):
        if self.is_merging:
            self.target_direction = angle_to_target((self.sx,self.sy), (self.partner.sx,self.partner.sy))
        else:
            self.target_direction = angle_to_target((self.sx,self.sy), (Game.Game().ship.sx,Game.Game().ship.sy))

    def merge(self,partner):
        self.is_merging = True   
        self.partner=partner     
        self.standard_rotation_speed=self.rotation_speed        
        self.standard_speed=self.speed
        self.rotation_speed=20
        self.speed=250

#keep the zone given as argument
class CornerKeeper(DirectionalEnemy):
    
    def __init__(self,pos,((sx1,sy1),(sx2,sy2))):
        DirectionalEnemy.__init__(self,pos,CORNERKEEPER_POINTS,color=Colors.COLOR_WHITE,update_speed=True)

        self.attack_speed = 150
        self.retreat_speed = 100 
        self.attack_mode = False
        
        self.rotation_speed = 999
        
        self.sx1 = sx1
        self.sy1 = sy1
        self.sx2 = sx2
        self.sy2 = sy2
        self.initial_pos = pos

        self.hitpoints=999999;
        
        
    def update(self):
        if self.attack_mode == False and distance((self.sx,self.sy),self.initial_pos)<=self.retreat_speed*2:
            self.stop()  
        else:
            self.run()        
        DirectionalEnemy.update(self)        
          

    def update_target(self):
        if Game.Game().ship.sx>self.sx1 and Game.Game().ship.sy>self.sy1 and Game.Game().ship.sx<self.sx2 and Game.Game().ship.sy<self.sy2:
            self.attack_mode = True
            self.target_direction = angle_to_target((self.sx,self.sy), (Game.Game().ship.sx,Game.Game().ship.sy))
            self.target_speed = self.attack_speed
        else:
            self.attack_mode = False
            if distance((self.sx,self.sy),self.initial_pos)>self.retreat_speed*2:          
                self.target_direction = angle_to_target((self.sx,self.sy), self.initial_pos)
                self.target_speed = self.retreat_speed

        
        
class MissileLauncher(DirectionalEnemy):
    def __init__(self,pos):
        DirectionalEnemy.__init__(self,pos,COWARD_POINTS,color=Colors.COLOR_LIGHT_YELLOW,update_speed=False) 
        self.speed = 0
        self.rotation_speed=50
        self.reload_time=750

        self.last_shoot_time=0
        
        self.reward = 400
        self.shooting_timer=Timer.Timer()


    def update_target(self):
        self.target_direction = angle_to_target((self.sx,self.sy), (Game.Game().ship.sx,Game.Game().ship.sy))

    def update(self):
        DirectionalEnemy.update(self)
        self.angle=self.direction
        if self.shooting_timer.get_timer()>self.reload_time:
            if angle_diff(self.target_direction,self.direction)<5:
                Missile((self.sx,self.sy),self.direction)
                self.shooting_timer.reset_timer()
                
class Missile(DirectionalEnemy):
    def __init__(self,pos,angle):
        DirectionalEnemy.__init__(self,pos,MISSILE_POINTS,color=Colors.COLOR_LIGHT_YELLOW,update_speed=False,appearance_delay=0)

        self.angle = angle
        self.direction = angle
        self.speed = 1500
        self.rotation_speed=0.5
        
        self.reward = 200        
         

    def update_target(self):
        self.target_direction = angle_to_target((self.sx,self.sy), (Game.Game().ship.sx,Game.Game().ship.sy))

    def update(self):
        DirectionalEnemy.update(self)
        for i in range(0,3):
            Particle((self.sx+random.randint(-500,500),self.sy+random.randint(-500,500)),(-self.vx/8+random.randint(-2,2),-self.vy/8+random.randint(-2,2)),life=120)
        self.angle=self.direction

    def _bounce_x(self):
        self.kill()

    def _bounce_y(self):
        self.kill()



#
#class Berzerker(DirectionalEnemy):
#    def __init__(self,pos):
#        DirectionalEnemy.__init__(self,pos,BULL_POINTS,color=(255,128,128),update_speed=False)
#        self.speed = 1000
#        self.rotation_speed=1    
#
#    def update_target(self):
#        self.target_direction = angle_to_target((self.sx,self.sy), (Game.Game().ship.sx,Game.Game().ship.sy))
#
#    def update(self):
#        DirectionalEnemy.update(self)
#        self.angle=self.angle+5


class Turner(Enemy):
    def __init__(self,pos,speed_factor=100):
        Enemy.__init__(self,pos,BULL_POINTS,color=Colors.COLOR_LIGHT_RED)
        self.speed = 1000 * speed_factor / 100
        self.speed_trans = 400 * speed_factor / 100
        self.rotation_speed = 5  * speed_factor / 100 * GLOBAL_SPEED * Timer.get_frame_time() / 1000
        self.refresh_time=251
        self.direction = 0

        
        self.vx_trans=0
        self.vy_trans=0
        
        self.reward = 50
        self.refreshing_timer= Timer.Timer()

    def update(self):
        Enemy.update(self)
        self.direction += self.rotation_speed
        self.angle=self.angle+5  *   GLOBAL_SPEED * Timer.get_frame_time() / 1000


        self.vx = int(math.cos(math.radians(self.direction))*self.speed)+self.vx_trans
        self.vy = int(math.sin(math.radians(self.direction))*self.speed)+self.vy_trans

        if self.refreshing_timer.get_timer()>self.refresh_time:
            att = angle_to_target((self.sx,self.sy), (Game.Game().ship.sx,Game.Game().ship.sy))
            self.vx_trans = int(math.cos(math.radians(att))*self.speed_trans)
            self.vy_trans = int(math.sin(math.radians(att))*self.speed_trans)
            self.refreshing_timer.reset_timer()
            


    def _bounce_x(self):
        self.direction = 180 - self.direction

    def _bounce_y(self):
        self.direction = - self.direction


class Coward(DirectionalEnemy):
    def __init__(self,pos):
        DirectionalEnemy.__init__(self,pos,COWARD_POINTS,color = Colors.COLOR_GREEN,update_speed=False)


        self.standard_speed = 800.0
        self.evasion_speed = 2000.0
        self.detection_distance = 150.0
        self.rotation_speed = 10
        
        self.speed = self.standard_speed
        
        self.reward = 20;        

    def update(self):
        DirectionalEnemy.update(self)
        self.angle=self.direction


    def update_target(self):
        self.target_direction = angle_to_target((self.sx,self.sy), (Game.Game().ship.sx,Game.Game().ship.sy))
#        att = angle_to_target((self.sx,self.sy), (Game.Game().ship.sx,Game.Game().ship.sy))
        self.speed = self.standard_speed
        if Game.Game().playershots:
            closest_bullet = min(Game.Game().playershots,key=lambda shot : self.manhattan_distance(shot))
            d = self.manhattan_distance(closest_bullet)
            if d<self.detection_distance*256:
                speed_factor = 1-float(d)/(self.detection_distance*256)
                self.speed = self.evasion_speed * speed_factor +  self.standard_speed * (1-speed_factor)  
                if angle_diff(closest_bullet.direction,angle_to_target((closest_bullet.sx,closest_bullet.sy),(self.sx,self.sy)))>0:
                    self.target_direction = closest_bullet.direction + 90 #angle_to_target((closest_bullet.sx,closest_bullet.sy),(self.sx,self.sy))
                else:
                    self.target_direction = closest_bullet.direction - 90 #angle_to_target((closest_bullet.sx,closest_bullet.sy),(self.sx,self.sy))

class Particle(pygame.sprite.Sprite):
    def __init__(self, (sx,sy),direction=None,life_length=500):
        pygame.sprite.Sprite.__init__(self,self.containers)

        if direction==None:
            if random.random()>0.5:
                (vx,vy)=(random.randint(-800,800),random.randint(-1200,1200))
            else:
                (vx,vy)=(random.randint(-1200,1200),random.randint(-800,800))            
            
                
        else:
            (vx,vy)=direction

        self.vx = vx
        self.vy = vy
        
        self.vx_tail = self.vx*8/10
        self.vy_tail = self.vy*8/10
        
        
        self.sx=sx
        self.sy=sy
        
        self.sx_tail = self.sx
        self.sy_tail = self.sy

        self.remaining_life = 1.0
        self.light=255
        
        self.color=Colors.COLOR_LIGHT_YELLOW
        
        self.life_step = float(Timer.get_frame_time()) / life_length
        
        self.image=pygame.surface.Surface((1,1))
        self.rect=Rect(0,0,1,1)

    def update(self):
#        Sprite.update(self)

        self.sx += self.vx  * GLOBAL_SPEED * Timer.get_frame_time() / 1000
        self.sy += self.vy  * GLOBAL_SPEED * Timer.get_frame_time() / 1000
     
        
        self.sx_tail += self.vx_tail * GLOBAL_SPEED * Timer.get_frame_time() / 1000
        self.sy_tail += self.vy_tail * GLOBAL_SPEED * Timer.get_frame_time() / 1000

        self.remaining_life -= self.life_step
        self.light =int(256*self.remaining_life)
        
        if self.light <= 50:
            self.kill()

        if self.sx > WORLD_WIDTH:
            self.kill()
        if self.sx < 0:
            self.kill()
        if self.sy > WORLD_HEIGHT:
            self.kill()
        if self.sy < 0:
            self.kill()

    def get_color(self):
        return Colors.explode_color(self.light)
  
        

    def draw(self, surface):
        if Game.USE_ANTIALIAS:
            pygame.draw.aaline(surface,self.get_color(),(screen_reduction(self.sx),screen_reduction(self.sy)),(screen_reduction(self.sx_tail),screen_reduction(self.sy_tail)),DRAW_WIDTH)
        else:
            pygame.draw.line(surface,self.get_color(),(screen_reduction(self.sx),screen_reduction(self.sy)),(screen_reduction(self.sx_tail),screen_reduction(self.sy_tail)),DRAW_WIDTH)            

