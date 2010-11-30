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


import math
import Game

from Sound import *
from GameObjects import *

class Collider:



    def __init__(self):
        self.BIN_SIZE = 40

    def PointCollision(self,asteroid, point):
        x = point[0]
        y = point[1]
        Lines = []




        index = 0
        for index in xrange(len(asteroid.drawpoints)):
            p0 = asteroid.drawpoints[index]
            try: p1 = asteroid.drawpoints[index + 1]
            except: p1 = asteroid.drawpoints[0]
            Lines.append([p0, p1])
        for l in Lines:
            p0 = l[0]
            p1 = l[1]
            x0 = p0[0]; y0 = p0[1]
            x1 = p1[0]; y1 = p1[1]
            test = (y - y0) * (x1 - x0) - (x - x0) * (y1 - y0)
            if test > 0: return False
        return True

    def __lineCollision(self,a, b):
        s1 = a[0]
        s2 = b[0]
        e1 = a[1]
        e2 = b[1]
        A = e1[0] - s1[0]
        B = e1[1] - s1[1]
        C = e2[0] - s2[0]
        D = e2[1] - s2[1]
        E = s1[1] - s2[1]
        F = s1[0] - s2[0]

        denom = (D * A) - (C * B)
        if denom == 0:
            return False
        numA = C * E - D * F
        numB = A * E - B * F

        Ta = numA / float(denom)
        Tb = numB / float(denom)
        if (Ta >= 0 and Ta <= 1) and (Tb >= 0 and Tb <= 1):
            return True
        return False

    def __Exact_Collision(self,sprite1, sprite2):
        sprite1.compute_drawpoints()
        sprite2.compute_drawpoints()
        
        lines1 = []
        lines2 = []
        for n in xrange(len(sprite1.drawpoints)):
            lines1.append([sprite1.drawpoints[n - 1], sprite1.drawpoints[n]])
        for n in xrange(len(sprite2.drawpoints)):
            lines2.append([sprite2.drawpoints[n - 1], sprite2.drawpoints[n]])
        for line1 in lines1:
            for line2 in lines2:
                if self.__lineCollision(line1, line2):
                    return True
        return False

    def __Exact_Line_Collision(self,shot, sprite):
        sprite.compute_drawpoints()

        
        sprite_lines = []

        for n in xrange(len(sprite.drawpoints)):
            sprite_lines.append([sprite.drawpoints[n - 1], sprite.drawpoints[n]])
 
        for sprite_line in sprite_lines:
            if self.__lineCollision([(shot.x,shot.y),(shot.old2_x,shot.old2_y)], sprite_line):
                return True
            
        return False


    def __Collision(self,sprite1, sprite2):
#        distance = math.sqrt((sprite1.pos[0] - sprite2.pos[0]) * (sprite1.pos[0] - sprite2.pos[0])\
#            + (sprite1.pos[1] - sprite2.pos[1]) * (sprite1.pos[1] - sprite2.pos[1]))
        if pygame.sprite.collide_rect(sprite1,sprite2):
            return self.__Exact_Collision(sprite1, sprite2)
        else:
            return False

    

    def __ShotCollision(self,shot, sprite):
#        distance = math.sqrt((sprite1.pos[0] - sprite2.pos[0]) * (sprite1.pos[0] - sprite2.pos[0])\
#            + (sprite1.pos[1] - sprite2.pos[1]) * (sprite1.pos[1] - sprite2.pos[1]))
        if generate_rect((shot.x,shot.y),(shot.old2_x,shot.old2_y)).colliderect(sprite):
            return self.__Exact_Line_Collision(shot, sprite)
        else:
            return False

    def __computeCells(self, sprite):
            x1 = int(math.floor(sprite.rect.left / self.BIN_SIZE))
            x2 = int(math.floor(sprite.rect.right / self.BIN_SIZE))
            y1 = int(math.floor(sprite.rect.top / self.BIN_SIZE))
            y2 = int(math.floor(sprite.rect.bottom / self.BIN_SIZE))



            coords = []

            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    coords.append((x, y))

            return coords

    def __computeShotCells(self, shot):
      
        x1 = int(math.floor(min(shot.x,shot.old2_x) / self.BIN_SIZE))
        y1 = int(math.floor(min(shot.y,shot.old2_y)   / self.BIN_SIZE))
        x2 = int(math.floor(max(shot.x,shot.old2_x)    / self.BIN_SIZE))
        y2 = int(math.floor(max(shot.y,shot.old2_y)   / self.BIN_SIZE))

        coords = []

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                coords.append((x, y))

        return coords

    def __computeGrid(self, group):
            collisionGrid = {}

            for s in group:
                for (x, y) in self.__computeCells(s):
                    spriteList = collisionGrid.setdefault((x, y), [])
                    spriteList.append(s)
                    collisionGrid[(x, y)] = spriteList
            return collisionGrid

    def __getCollisionSpriteGrid(self, sprite, grid):
            setElts = set()
            cells = self.__computeCells(sprite)
            for c in cells:
                if c in grid:
                    for s in grid[c]:
                        setElts.add(s)
            return setElts
        
    def __getCollisionShotGrid(self, shot, grid):
            setElts = set()
            cells = self.__computeShotCells(shot)
            for c in cells:
                if c in grid:
                    for s in grid[c]:
                        setElts.add(s)
            return setElts        

    def __getCollisionGridGrid(self, grid1, grid2):
            setEltPairs = set()
            for (coord, listElt1) in grid1.iteritems():
                if coord in grid2:
                    listElt2 = grid2[coord]
                    for elt1 in listElt1:
                        for elt2 in listElt2:
                            setEltPairs.add((elt1, elt2))
            return setEltPairs



    def DetectCollisions(self):

            game=Game.Game()
            self.enemyGrid = self.__computeGrid(game.enemies)

            for shot in game.playershots:
                for enemy in self.__getCollisionShotGrid(shot, self.enemyGrid):
                    if self.__ShotCollision(shot,enemy):
                        enemy.hit()
                        shot.kill()
                        play_boom()


            for enemy in self.__getCollisionSpriteGrid(game.ship, self.enemyGrid):
                if enemy.isActive():
                    if self.__Collision(enemy, game.ship):
                        if game.ship.alive() and not game.ship.is_invincible():
                            enemy.hit()
                            game.ship.kill()
                            play_boom()


            for s in game.enemyshots:
                if self.__Collision(s, game.ship):
                    if game.ship.alive()  and not game.ship.is_invincible():
                        game.ship.kill()
                        play_boom()

    def merge_enemies(self):
        select_bull = lambda enemies:[enemy for enemy in enemies if isinstance(enemy,Bull)]
        distance = lambda (e1,e2):e1.mahattan_distance(e2)

        sorted_cells=self.enemyGrid.values() #sorted(self.enemyGrid.values(),key=lambda k:-len(select_bull(k)))
        
        for cell in sorted_cells:
            if len(Game.Game().enemies)<=MAX_BULL:
                return
            candidates=select_bull(cell)
            if len(candidates)>1:
                selected_candidates=(candidates[0],candidates[1])
    
                if len(candidates)>2:
                    min_distance=distance(selected_candidates)
                    for i,e1 in enumerate(candidates[0:min(3,len(candidates))]):
                        for e2 in candidates[i+1:len(candidates)]:
                            if not e2.partner==e1 and distance((e1,e2))<min_distance:
                                selected_candidates=(e1,e2)
    
                selected_candidates[0].merge(selected_candidates[1])





