from PIL import Image, ImageOps
import numpy as np

# CONSTANTES #
k = 1
k1 = 1
##############


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

