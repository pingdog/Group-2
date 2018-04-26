from OpenGL.GL import *
from OpenGL.GLU import *
import gl_util

def load_earth():
    global dl_earth, texture_earth
    
    texture_earth = gl_util.Texture2D("data/earth.jpg")
    texture_earth.set_nicest()
    
    dl_earth = glGenLists(1)
    glNewList(dl_earth,GL_COMPILE)

    glPushMatrix()
    glRotatef(-90, 1,0,0)
    sphere = gluNewQuadric()
    texture_earth.bind()
    gluQuadricTexture(sphere,GL_TRUE)
    gluSphere(sphere, 1.0, 80,80)
    gluDeleteQuadric(sphere)
    glPopMatrix()
    
    glEndList()
def unload_earth():
    global dl_earth, texture_earth
    glDeleteLists(1,dl_earth)
    del dl_earth
    del texture_earth
def draw_earth():
    glCallList(dl_earth)

coordinates = []
def load_points():
    file = open("data/PointList.txt","r")
    point_data = file.read()
    file.close()
    
    #Data format is some lines of the form "(#W,#N)"
    for line in point_data.split("\n"):
        line.strip()
        if line == "" or line.startswith("#"): continue

        line = list(map(lambda x:x.strip(),line.split(",")))
        line = list(map(lambda x:x.strip(),[line[0][1:],line[1][:-1]]))
        
        coordinate = list(map(float,[line[0][:-1],line[1][:-1]]))
        if line[0][-1] == "E": coordinate[0] *= -1
        if line[1][-1] == "S": coordinate[1] *= -1

        coordinates.append(coordinate)
def draw_points():
    r = 1.5
    glBegin(GL_LINES)
    for coordinate in coordinates:
        glVertex3f(0,0,0)
        glVertex3fv(gl_util.spherical_to_rectangular([0,0,0], r, coordinate[0]+90,coordinate[1]))
    glEnd()
