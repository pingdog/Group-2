from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.EXT.texture_filter_anisotropic import *
import pygame
from math import *

def init_gl(new_screen_size):
    global screen_size #So that we can use screen_size in other functions
    screen_size = list(new_screen_size)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
    glTexEnvi(GL_POINT_SPRITE,GL_COORD_REPLACE,GL_TRUE)

    glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST)
    glEnable(GL_DEPTH_TEST)

def set_view_3D(angle):
    glViewport(0,0,screen_size[0],screen_size[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(angle,float(screen_size[0])/float(screen_size[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

#Converts from spherical coordinates to rectangular coordinates
def spherical_to_rectangular(center_offset, radius, rot_y,rot_xz):
    return [ #rot_y is rotation about the y axis, rot_xz is elevation above or below the horizontal plane
        center_offset[0] + radius*cos(radians(rot_y))*cos(radians(rot_xz)),
        center_offset[1] + radius                    *sin(radians(rot_xz)),
        center_offset[2] + radius*sin(radians(rot_y))*cos(radians(rot_xz))
    ]

def set_camera_spherical(camera_center, camera_radius, rot_y,rot_xz):
    camera_pos = spherical_to_rectangular(camera_center, camera_radius, rot_y,rot_xz)
    gluLookAt(
        camera_pos[0],camera_pos[1],camera_pos[2],
        camera_center[0],camera_center[1],camera_center[2],
        0,1,0
    )
    
class Texture2D:
    def __init__(self,path):
        surf = pygame.image.load(path)
        data = pygame.image.tostring(surf,"RGBA",1)

        self.texture = glGenTextures(1)
        self.bind()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surf.get_width(),surf.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    def __del__(self):
        glDeleteTextures(self.texture)

    def bind(self):
        glBindTexture(GL_TEXTURE_2D,self.texture)
    def set_nicest(self):
        self.bind()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        #Anisotropic Filtering - Makes textures look nice at an angle, but optional
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAX_ANISOTROPY_EXT,glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT))
        #Mipmapping - Makes textures look nice when minified, but optional
        glGenerateMipmap(GL_TEXTURE_2D)
