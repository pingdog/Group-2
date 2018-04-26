from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import sys, os, traceback
import gl_util, objects
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.init()
pygame.font.init()

screen_size = [800,600]
multisample = 16 #Set to 0 to disable
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("3D World - Ian Mallett - v.2.0.2 - 2012") #And patch help by Jason Marshall
if multisample:
    pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS,1)
    pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES,multisample)
pygame.display.set_mode(screen_size,OPENGL|DOUBLEBUF)

gl_util.init_gl(screen_size)

camera_rot = [90,0]
camera_radius = 5.0
camera_center = [0,0,0]
def get_input():
    global camera_rot, camera_radius
    key = pygame.key.get_pressed()
    mpress = pygame.mouse.get_pressed()
    mrel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
        elif event.type == MOUSEBUTTONDOWN:
            if   event.button == 4: camera_radius -= 0.5
            elif event.button == 5: camera_radius += 0.5
            camera_radius = max([min([camera_radius,10.0]),1.2])
    if mpress[0]:
        camera_rot[0] += mrel[0]
        camera_rot[1] += mrel[1]
    return True
    
def draw():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    gl_util.set_view_3D(45)

    gl_util.set_camera_spherical(camera_center, camera_radius, camera_rot[0],camera_rot[1])

    objects.draw_earth()
    objects.draw_points()
    
    pygame.display.flip()
def main():
    objects.load_points()
    objects.load_earth()
    
    clock = pygame.time.Clock()
    while True:
        if not get_input(): break
        draw()
        clock.tick(60)

    objects.unload_earth()
    
    pygame.quit(); sys.exit()
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_exception(e.__class__, e, tb)
        pygame.quit()
        input()
        sys.exit()
