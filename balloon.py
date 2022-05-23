# IMPORTS #
from PIL import Image, ImageOps, ImageDraw, ImageFilter
import numpy as np
from math import cos, sin, pi

import matplotlib.pyplot as plt

import os, glob

# CONSTANTES #
k = .9
k1 = .8

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

def fusion(v):
    newv = [v[0]]
    for i in range(1, len(v)):
        if v[i] != newv[-1]:
            newv.append(v[i])
    return newv


def get_contours(
image : Image.Image,
niteration : int,
npoints : int,
initial_guess_radius : float) -> 'list[tuple[int, int]]':
    image = ImageOps.grayscale(image)

    center = (image.size[0]//2, image.size[1]//2)

    imagearr = np.asarray(image)

    gradx,grady = np.gradient(imagearr)

    potentiel = -(gradx**2 + grady**2)

    forcey, forcex = np.gradient(potentiel)

    for i in range(len(forcex)):
        for j in range(len(forcex[0])):
            l = (forcex[i,j]**2 + forcey[i,j]**2)**.5
            if l != 0:
                forcex[i,j] *= k/l
                forcey[i,j] *= k/l

    v = [
        ((center[0]+initial_guess_radius*cos(theta)),
        (center[1]+initial_guess_radius*sin(theta))) 
        for theta in np.linspace(0, 2*pi, npoints+1)
    ]

    for _ in range(niteration):
        v = fusion(v)
        v = inflate(v, forcex, forcey)

    return [(int(x), int(y)) for x,y in v]