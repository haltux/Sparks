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


from GameObjects import *



import random


#to create a level:
# - create a new class inheriting from Level (see existing levels)
# -- Take LevelBullRectangle as template 
# -- use _add_pattern_sequence method to add different type of enemy waves
# -- pay attention to difficulty settings. arguments of _add_pattern_sequence should depend on diff (integer between  and 14).
# - add level to CUSTOM_LEVEL sequence (defined at the end of this file)

class Level(object):
    base_diff=0
    def __init__(self,diff):
        self.difficulty = diff + self.base_diff
        self.events={}
        self.wait_points={}
        self.date=0

    def _add_pattern(self,start_date,period,nb_iter,obj_and_args,(pattern,pattern_args)):
        date=start_date
        if type(obj_and_args)==type((0,)):
            obj=obj_and_args[0]
            args=obj_and_args[1]
        else:
            obj=obj_and_args
            args=()
        for index in range(nb_iter):
            if date in self.events:
                self.events[date].append(((obj,args),pattern(pattern_args,index,nb_iter)))
            else:
                self.events[date]=[((obj,args),pattern(pattern_args,index,nb_iter))]
            date+=period

# dates : sequence of date (in frame from the beginning of the level) for each enemy wave
# nbs_iter : sequence (typically one element) of number of enemy per wave.
# objs : sequence (typically one element) of type of enemy for each wave
# patterns: pattern fct for enemy appearance. see examples in existing levels.
    def _add_pattern_sequence(self,dates,nbs_iter,objs,patterns):
        for i,date in enumerate(dates):
            self._add_pattern(date,1,nbs_iter[i%len(nbs_iter)],objs[i%len(objs)],patterns[i%len(patterns)])

    def _add_wait_point(self,date,nb_bulls,nb_other_enemies):
        self.wait_points[date]=(nb_bulls,nb_other_enemies)
        
    def _add_corner_keepers(self):
        event = ((CornerKeeper,(((0,0),(WORLD_WIDTH/6,WORLD_HEIGHT/6)),)),(WORLD_WIDTH/6,WORLD_HEIGHT/6))
        self.events.setdefault(0,[]).append(event)
        
        event = ((CornerKeeper,(((WORLD_WIDTH*5/6,0),(WORLD_WIDTH,WORLD_HEIGHT/6)),)),(WORLD_WIDTH*5/6,WORLD_HEIGHT/6))
        self.events[0].append(event)
        
        event = ((CornerKeeper,(((0,WORLD_HEIGHT*5/6),(WORLD_WIDTH/6,WORLD_HEIGHT)),)),(WORLD_WIDTH/6,WORLD_HEIGHT*5/6))
        self.events[0].append(event)
        
        event = ((CornerKeeper,(((WORLD_WIDTH*5/6,WORLD_HEIGHT*5/6),(WORLD_WIDTH,WORLD_HEIGHT)),)),(WORLD_WIDTH*5/6,WORLD_HEIGHT*5/6))
        self.events[0].append(event)

#    def add_group(self,date,nb_items,obj,pos_generator):
#        for index in range(nb_items):
#            self.events[date]=self.events.setdefault(date,[]).add((obj,pos_generator(index,nb_items)))

    def is_finished(self):
        return self.date>max(self.events.keys())

    def process(self,game):

        if self.date in self.wait_points:
            conditions=self.wait_points[self.date]
            if len(game.bulls)>conditions[0] or len(game.destroyables)-len(game.bulls)>conditions[1]:
                return
        
        if len(game.bulls)>MAX_BULL:
            return

        events=self.events[self.date] if self.date in self.events else []
        for event in events:
            (obj,args)=event[0]
            (x,y)=event[1]
            obj([x,y],*args)
            
        self.date+=1            

def random_pattern(_,i,n):
    rand1 = random.random() * math.sqrt(WORLD_WIDTH/2)
    rand1 *= rand1
    rand2 = random.random() * math.sqrt(WORLD_HEIGHT/2)
    rand2 *= rand2
    return (random.choice([int(rand1),WORLD_WIDTH-int(rand1)]),random.choice([int(rand2),WORLD_HEIGHT-int(rand2)]))

def uniform_random_pattern(_,i,n):
    rand1 = random.random() * WORLD_WIDTH
    rand2 = random.random() * WORLD_HEIGHT    
    return (int(rand1),int(rand2))

def circle_pattern((x,y,r),i,n):
    angle=2*math.pi/n*i
    return (int(x+r*math.cos(angle)),int(y+r*math.sin(angle)))

def poly_line_pattern((x1,y1,x2,y2),i,n):
    return (x1+(x2-x1)*i/n,y1+(y2-y1)*i/n)

def split(distances,nb_sprites):
    total = 0.0
    for d in distances:
        total += d


    splits=[]
    rem_steps=nb_sprites
    rem_distance=total

    for d in distances:
        if rem_steps>0:
            step_size=rem_distance/rem_steps
            nb_steps = math.floor(d/step_size+0.5)
            rem_steps-=nb_steps
            rem_distance-=d
            splits.append(nb_steps)

    return splits


def rectangle_pattern((x1,y1,x2,y2),i,n):
    lines=[(x1,y1,x2,y1),(x2,y1,x2,y2),(x2,y2,x1,y2),(x1,y2,x1,y1)]
    distances=map(lambda (x1,y1,x2,y2):math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)),lines)
    splits=split(distances,n)

    j=0
    while i>=splits[j]:
        i-=splits[j]
        j+=1

    return poly_line_pattern(lines[j],i,splits[j])

def grid_pattern((x1,y1,x2,y2),i,n):
    ratio = float(x2-x1)/(y2-y1)
    nb_lines = max(2,int(math.ceil(math.sqrt(n/ratio))))
    lines=[(x1,y1+k*(y2-y1)/(nb_lines-1),x2,y1+k*(y2-y1)/(nb_lines-1)) for k in range(0,nb_lines)]
    distances=[x2-x1 for _ in range(0,nb_lines)]
    splits=split(distances,n)

    j=0
    while i>=splits[j]:
        i-=splits[j]
        j+=1

    return line_pattern(lines[j],i,splits[j])



def line_pattern((x1,y1,x2,y2),i,n):
    if i==n-1:
        return (x2,y2)
    else:
        return poly_line_pattern((x1,y1,x2,y2),i,n-1)

class SublevelManager:
        def __init__(self,level,length):
            self.start = 0
            self.end=length-1
            self.sublevel=0
            self.level = level
            self.length = length
        
        def next(self): 
            self.level._add_wait_point(self.end, 10, 1)            
            self.start += self.length
            self.end += self.length
            self.sublevel += 1

def RaiseDifficulty(level,base_diff):
    return type(level.__name__+"_diff_"+str(base_diff),(level,),{"base_diff":base_diff})

class LevelArcade1(Level):
    name = "Arcade Mode"
    def __init__(self,diff):
        Level.__init__(self,diff)
        
        self._add_corner_keepers()
        
        sm = SublevelManager(self,1000)
    
        interval=70-self.difficulty*5
    
        for i in range(0,2):
            self._add_pattern_sequence(range(sm.start,sm.end,interval),[i*2+3],[(Bull,(Bull.BASIC,))],[(random_pattern,())])
            sm.next()
            
class LevelArcade2(Level):
    name = "Arcade Mode"
    def __init__(self,diff):
        Level.__init__(self,diff)
        
        sm = SublevelManager(self,1000)

        interval=70-self.difficulty*5
    
        for i in range(0,3):
            self._add_pattern_sequence(range(sm.start,sm.end,interval),[3],[Bull],[(random_pattern,())])
            self._add_pattern_sequence(range(sm.start,sm.end,interval*2),[i+1],[(Bull,(Bull.BERZERKER,))],[(random_pattern,())])            
            sm.next()
            
        self._add_pattern_sequence(range(sm.start,sm.end,300),[5+self.difficulty*2],[(Bull,(Bull.BERZERKER,))],\
                                   [(rectangle_pattern,(WORLD_WIDTH/20,WORLD_HEIGHT/20,WORLD_WIDTH/20*19,WORLD_HEIGHT/20*19))])                    
        sm.next()             

class LevelArcade3(Level):
    name = "Arcade Mode"
    def __init__(self,diff):
        Level.__init__(self,diff)
        
        sm = SublevelManager(self,1000)

        interval=70-self.difficulty*5
    
        for i in range(0,3):
            self._add_pattern_sequence(range(sm.start,sm.end,interval),[3],[Bull],[(random_pattern,())])
            self._add_pattern_sequence(range(sm.start,sm.end,interval),[i+1],[Turner],[(random_pattern,())])            
            sm.next()
            
        self._add_pattern_sequence(range(sm.start,sm.end,300),[8+self.difficulty*3],[Turner],\
                                   [(rectangle_pattern,(WORLD_WIDTH/20,WORLD_HEIGHT/20,WORLD_WIDTH/20*19,WORLD_HEIGHT/20*19))])               
        sm.next()             

class LevelArcade4(Level):
    name = "Arcade Mode"
    def __init__(self,diff):
        Level.__init__(self,diff)
        
        sm = SublevelManager(self,1000)

        interval=70-self.difficulty*5
    
        for i in range(0,3):
            self._add_pattern_sequence(range(sm.start,sm.end,interval),[3],[Bull],[(random_pattern,())])
            self._add_pattern_sequence(range(sm.start,sm.end,interval*2),[i+2],[Turner],[(random_pattern,())])  
            self._add_pattern_sequence(range(sm.start,sm.end,interval*4),[i+2],[(Bull,(Bull.BERZERKER,))],[(random_pattern,())])                       
            sm.next()
            
        
        self._add_pattern_sequence(range(sm.start,sm.end,interval),[3],[Bull],[(random_pattern,())])  
        self._add_pattern_sequence(range(sm.start,sm.end,300),[1+self.difficulty/3],[MissileLauncher],[(random_pattern,())])                        
        sm.next()             

        self._add_pattern_sequence(range(sm.start,sm.end,300),[3+self.difficulty],[MissileLauncher],\
                                  [(rectangle_pattern,(WORLD_WIDTH/20,WORLD_HEIGHT/20,WORLD_WIDTH/20*19,WORLD_HEIGHT/20*19))])                          
        sm.next()             



class LevelBullRectangles(Level):
    name = "Bulls Rectangles"
    def __init__(self,diff):
        Level.__init__(self,diff)
        self._add_pattern_sequence(range(1,1000,200),[20+self.difficulty*4],[Bull],[(rectangle_pattern,(0,0,WORLD_WIDTH,WORLD_HEIGHT))])
        
class LevelRandomBulls(Level):
    name = "Random Bulls"
    def __init__(self,diff):
        Level.__init__(self,diff)
        self._add_corner_keepers()        
        self._add_pattern_sequence(range(1,1000,33),[min(self.difficulty+1,5)],[Bull],[(random_pattern,())])
        if self.difficulty>5:
            self._add_pattern_sequence(range(1,1000,100/(self.difficulty-5)),[1],[(Bull,(Bull.BERZERKER,))],[(random_pattern,())])

class LevelRandomBulls2(Level):
    name = "Random Bulls 2"
    def __init__(self,diff):
        Level.__init__(self,diff)
        self._add_corner_keepers()        
        self._add_pattern_sequence(range(1,1000,100),[min(self.difficulty*3+3,15)],[Bull],[(random_pattern,())])
        if self.difficulty>5:
            self._add_pattern_sequence(range(1,1000,100/(self.difficulty-5)),[1],[(Bull,(Bull.BERZERKER,))],[(random_pattern,())])

class LevelCowards(Level):
    name = "Cowards"
    def __init__(self,diff):
        Level.__init__(self,diff)
        self._add_corner_keepers()        
        self._add_pattern_sequence(range(1,1000,200),[10+self.difficulty*2],[Coward],[(random_pattern,())])

class LevelTurners(Level):
    name = "Turners"
    def __init__(self,diff):
        Level.__init__(self,diff)
        self._add_corner_keepers()
        self._add_pattern_sequence(range(1,1000,200),[5+self.difficulty],[Turner],[(random_pattern,())])

class LevelBerzerkers(Level):
    name = "Berzerkers"
    def __init__(self,diff):
        Level.__init__(self,diff)
        self._add_corner_keepers()        
        self._add_pattern_sequence(range(1,1000,200),[5+self.difficulty],[(Bull,(Bull.BERZERKER,))],[(random_pattern,())])

class LevelMissileLaunchers(Level):
    name = "MissileLaunchers"
    def __init__(self,diff):
        Level.__init__(self,diff)
        self._add_pattern_sequence([1],[3+self.difficulty],[MissileLauncher],\
                                  [(rectangle_pattern,(WORLD_WIDTH/20,WORLD_HEIGHT/20,WORLD_WIDTH/20*19,WORLD_HEIGHT/20*19))])     
#        self._add_pattern_sequence(range(1,1000,200-10*self.difficulty),[0],[1+self.difficulty/2],[Coward],[random_pattern])


class LevelMiners(Level):
    name = "Miners"
    def __init__(self,diff):  
        Level.__init__(self,diff) 
        self._add_corner_keepers()
        self._add_pattern_sequence(range(1,1000,50),[min(self.difficulty+1,5)],[Bull],[(random_pattern,())])   
        self._add_pattern_sequence(range(1,1000,300),[min(self.difficulty/2+1,5)],[Miner],[(random_pattern,())])   

class LevelAsteroids(Level):
    name = "Asteroids"
    def __init__(self,diff):  
        Level.__init__(self,diff) 
        self._add_corner_keepers() 
        self._add_pattern_sequence(range(1,1000,50),[min(self.difficulty+1,5)],[Bull],[(random_pattern,())])          
        self._add_pattern_sequence(range(1,1000,300),[self.difficulty/3+1],[Asteroid],[(random_pattern,())])   

class LevelMines(Level):
    name = "Mines"
    def __init__(self,diff):
        Level.__init__(self,diff)
        self._add_corner_keepers()        
        self._add_pattern_sequence(range(1,1000,33),[min(self.difficulty+1,5)],[Mine],[(uniform_random_pattern,())])



class LevelTest(Level):
    name = "Test"
    
    def __init__(self,diff):
        Level.__init__(self,diff)
        self._add_corner_keepers()
        self._add_pattern_sequence([1000],[1],[Bull],[(rectangle_pattern,(WORLD_WIDTH/10,WORLD_HEIGHT/10,WORLD_WIDTH*9/10,WORLD_HEIGHT*9/10))])

LEVEL_MAIN_SEQUENCE=[LevelArcade1,LevelArcade2,LevelArcade3,LevelArcade4]

CUSTOM_LEVELS=[LevelBullRectangles,LevelRandomBulls,LevelRandomBulls2,LevelCowards,LevelTurners,LevelBerzerkers,LevelMissileLaunchers,LevelMiners,LevelMines,LevelAsteroids,LevelArcade1,LevelArcade2,LevelArcade3,LevelArcade4,LevelTest]

def get_next_level(num_level,diff):
    level=LEVEL_MAIN_SEQUENCE[num_level%len(LEVEL_MAIN_SEQUENCE)]
    level_diff=num_level/len(LEVEL_MAIN_SEQUENCE)*3
    return level(diff+level_diff)
