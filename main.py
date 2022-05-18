# IMPORTS #
from PIL import Image, ImageOps, ImageDraw, ImageFilter
import numpy as np
from math import cos, sin, pi

import os

# CONSTANTES #
k = .8
k1 = .9

# PARAMETRES #
niteration = 75
npoints = 100
r = 50

# PRECALCULS #
img = Image.open("img.jpg")
img = ImageOps.grayscale(img)
#img = img.filter(ImageFilter.BLUR)

img.save("gray.jpg")

center = (img.size[0]//2, img.size[1]//2)

imgarr = np.asarray(img)

gradx,grady = np.gradient(imgarr)

potentiel = -(gradx**2 + grady**2)

forcex, forcey = np.gradient(potentiel)

for i in range(len(forcex)):
    for j in range(len(forcex[0])):
        l = (forcex[i,j]**2 + forcey[i,j]**2)**.5
        if l != 0:
            forcex[i,j] *= k/l
            forcey[i,j] *= k/l

#Courbe initiale
v = [(center[0]+r*cos(theta), center[1]+r*sin(theta)) for theta in np.linspace(0, 2*pi, npoints+1)][:-1]

def inflate(v, forcex, forcey):
    "Applique la force de gonflement à chaque point de la courbe"
    l = len(v)
    newv = l*[(0,0)]
    for s,(x,y) in enumerate(v):
        fx, fy = forcex[round(y),round(x)], forcey[round(y),round(x)]

        #Calcul du vecteur normal
        ny = -(v[(s+1)%l][0] - v[(s-1)%l][0])
        nx = v[(s+1)%l][1] - v[(s-1)%l][1]
        module = (nx**2 + ny**2)**.5
        if module==0 :
            newv[s] = v[s]
            continue
        ny /= module
        nx /= module

        #Calcul du nouveau point
        dx, dy = k1*nx + fx, k1*ny + fy
        newv[s] = (x+dx, y+dy)

    return newv

def show(v,n):
    img = Image.open("img.jpg")
    draw = ImageDraw.Draw(img)
    for i in range(len(v)-1):
        draw.line(v[i] + v[i+1], fill = "red", width = 1)
    
    img.save("outs/res{}.jpg".format(n))

def fuse(v):
    newv = [v[0]]
    for i in range(1, len(v)):
        if v[i] != newv[-1]:
            newv.append(v[i])
    return newv

os.system("rm outs/*")

saved = 0

for n in range(niteration):
    if n%1 == 0:
        show(v,saved)
        saved+=1
    v = fuse(v)
    v = inflate(v, forcex, forcey)

show(v,saved)