import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d

v = np.array([[0,0,0], [1,0,0], [1,1,0], [0,1,0], 
              [0,0,1], [1,0,1], [1,1,1], [0,1,1]])

f = np.array([[0,2,1], [0,3,2], [1,2,6], [1,6,5],
              [0,5,4], [0,1,5], [4,5,6], [6,7,4],
              [3,7,6], [6,2,3], [0,4,7], [7,3,0]])

C = np.array([1,2,3,4,5,6,7,8,2,3,4,5])


fig = plt.figure()
ax = fig.add_subplot(projection="3d")

norm = plt.Normalize(C.min(), C.max())
colors = plt.cm.viridis(norm(C))

pc = art3d.Poly3DCollection(v[f], facecolors=colors, edgecolor="black")
ax.add_collection(pc)

plt.show()
