'''
Created on 24 nov. 2010

@author: Julien
'''

import pygame


COLOR_EXPLODE=-1
                        
COLOR_BLACK = 0
COLOR_WHITE = 1
COLOR_LIGHT_BLUE = 2
COLOR_ORANGE = 3
COLOR_YELLOW = 4
COLOR_LIGHT_RED = 5
COLOR_LIGHT_YELLOW = 6
COLOR_GREEN = 7
COLOR_GREY = 8  

LAST_COLOR = 8

COLOR_DEF={}

COLOR_DEF[COLOR_BLACK]=(0,0,0)
COLOR_DEF[COLOR_WHITE]=(255,255,255)
COLOR_DEF[COLOR_LIGHT_BLUE]=(128,255,255)
COLOR_DEF[COLOR_ORANGE]=(192,128,0)
COLOR_DEF[COLOR_YELLOW]=(255,255,0)
COLOR_DEF[COLOR_LIGHT_RED]=(255,128,128)
COLOR_DEF[COLOR_LIGHT_YELLOW]=(255,255,128)
COLOR_DEF[COLOR_GREEN]=(0,255,128)
COLOR_DEF[COLOR_GREY]=(175,175,175)

COLOR_DEF[COLOR_EXPLODE]=(0,0,0) #used only  in 8bits, to store index of shade values in palette




COLOR_DEPTH=0
FIRST_EXPLODE_COLOR=0


SHADE_LENGTH = 16
SHADES_FIRST={}

def explode_color_24bits(light):
    if light<64:
        return (light*2,0,0)
    elif light<128:
        return ((light-64)*2+128,(light-64)*4,0)
    else:
        return (255,255,(light-128)*2)

def explode_color(light):   
    global COLOR_DEPTH
    if COLOR_DEPTH>8: 
        return explode_color_24bits(light)
    else:
        return SHADES_FIRST[COLOR_EXPLODE]+min(light,255)*SHADE_LENGTH/256

def generate_shade_24bits((r,g,b),light):
    return (r*light/256,g*light/256,b*light/256)

def generate_shade(color,light):
    global COLOR_DEPTH
    if COLOR_DEPTH>8: 
        if light<255:
            return generate_shade_24bits(COLOR_DEF[color],light)
        else:
            return COLOR_DEF[color]
    else:
        if light<255:
            return SHADES_FIRST[color]+min(light,255)*SHADE_LENGTH/256
        else:
            return color
        
def get_color_def(color):
    global COLOR_DEPTH
    if COLOR_DEPTH>8: 
        return COLOR_DEF[color]
    else:
        return color            
            
    
def init_colors():
    global COLOR_DEPTH
    COLOR_DEPTH = pygame.display.get_surface().get_bitsize()
    if (COLOR_DEPTH==8):  
        palette = [COLOR_DEF[i] for i in range(0,LAST_COLOR)]
        

        for i in [COLOR_EXPLODE] + range(0,LAST_COLOR+1):
            SHADES_FIRST[i] = len(palette)
            if i==COLOR_EXPLODE:
                palette += [explode_color_24bits(x*256/SHADE_LENGTH) for x in range(0,SHADE_LENGTH)]
            else:
                palette += [generate_shade_24bits(COLOR_DEF[i],x*256/SHADE_LENGTH) for x in range(0,SHADE_LENGTH)]
                                         
                  
        pygame.display.get_surface().set_palette(palette)      
    
    
