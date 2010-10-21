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


import pygame
import os

sounds = {}
def load_sound(file, volume=1.0):
    sound = pygame.mixer.Sound(os.path.join("data", "sounds", file))
    sound.set_volume(volume)
    return sound

def load_sounds():
    pass
    #sounds["shoot"]=load_sound("shoot.wav")
    #sounds["boom"]=load_sound("boom.wav")    

def play_shoot():
    pass    
    #sounds["shoot"].play()

    
def play_boom():
    pass
    #sounds["boom"].play()
