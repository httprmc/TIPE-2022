# IMPORTS #
from PIL import Image, ImageOps
import numpy as np
from math import cos, sin, pi

# CONSTANTES #
k = 1
k1 = .8

# PARAMETRES #
niteration = 2000
npoints = 30
r = 30

# PRECALCULS #
img = Image.open("img.jpg")
img = ImageOps.grayscale(img)

imgarr = np.asarray(img)

gradx,grady = np.gradient(imgarr)

potentiel = -(gradx**2 + grady**2)

forcex, forcey = np.gradient(potentiel)

for i in range(len(forcex)):
    for j in range(len(forcex[0])):
        l = (forcex[i,j]**2 + forcey[i,j]**2)**.5
        if l != 0:
            forcex[i,j] *= -k/l
            forcey[i,j] *= -k/l

#Courbe initiale
v = [(round(r*cos(theta)), round(r*sin(theta))) for theta in np.linspace(0, 2*pi, npoints+1)][:-1]

def inflate(v, forcex, forcey):
    "Applique la force de gonflement à chaque point de la courbe"
    l = len(v)
    newv = l*[(0,0)]
    for s,(x,y) in enumerate(v):
        fx, fy = forcex[y,x], forcey[y,x]

        #Calcul du vecteur normal
        ny = v[(s+1)%l][0] - v[(s-1)%l][0]
        nx = v[(s+1)%l][1] - v[(s-1)%l][1]
        module = (nx**2 + ny**2)**.5
        if module==0 :
            newv[s] = v[s]
            continue
        ny /= module
        nx /= module

        #Calcul du nouveau point
        dx, dy = k1*nx + fx, k1*ny + fy
        newv[s] = (round(x+dx), round(y+dy))

    return newv


for _ in range(niteration):
    print(v)
    v = inflate(v, forcex, forcey)