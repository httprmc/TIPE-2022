import sys,os

from PIL import Image
from scipy.spatial import Delaunay

from balloon import get_contours

### CONSTANTES ###
niterations = 1000
npoints = 50
initial_guess_radius = 20
dh = 1
##################

def main(fichier_in):
    os.chdir(fichier_in)
    hauteur = 0
    points = []
    for img in os.listdir():
        try:
            contour = get_contours(
                Image.open(img),
                niterations,
                npoints,
                initial_guess_radius,
            )
            points += [(x,y,hauteur) for (x,y) in contour]
        except:
            pass
        hauteur += dh

    tri = Delaunay(points)
    os.chdir("..")
    save(tri, points)

def save(tri, points):
    with open("out.tri","w") as out:
        for tetra in tri.simplicies:
            for triangle in tetra:
                for pt in triangle:
                    out.write(str(points[pt]) + " ")
                out.write("\n")

if __name__ == "__main__":
    args = sys.argv
    assert len(args) > 1, "Pas assez d'arguments, il doit y avoir 1 argument"
    main(args[1])