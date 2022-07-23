

# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt

# def equation_plane(x, y, z):
#     a1 = x[1] - x[0]
#     b1 = y[1] - y[0]
#     c1 = z[1] - z[0]
#     a2 = x[2] - x[0]
#     b2 = y[2] - y[0]
#     c2 = z[2] - z[0]
#     a = b1 * c2 - b2 * c1
#     b = a2 * c1 - a1 * c2
#     c = a1 * b2 - b1 * a2
#     d = (- a * x[0] - b * y[0] - c * z[0])
#     return a, b, c, d
# def equation_z(a,b,c,d, x):
#     return float(-(a*x[0] + b*x[1] + d))/float(c)

# x = [0, 1, 0]
# y = [3,2,0]
# z = [0,4,8]

# a, b, c, d = equation_plane(x, y, z)
# # print(a, b, c, d)
# # for i in range(1, 10):
# #     print(i)
# #     print(equation_z(a,b,c,d, [i,i]))


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# x =[1,2,3,4,5,6,7,8,9,10]
# y =[5,6,2,3,13,4,1,2,4,8]
# z =[equation_z(a,b,c,d, [x[i],y[i]]) for i in range(len(x))]



# ax.scatter(x, y, z, c='r', marker='o')

# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

# plt.show()

# # from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# # fig = plt.figure()

# # ax = fig.add_subplot(111, projection='3d')

# # x = [1, 0, 3, 4]

# # y = [0, 5, 5, 1]

# # z = [1, 3, 4, 0]

# # vertices = [list(zip(x,y,z))]

# # poly = Poly3DCollection(vertices, alpha=0.8)

# # ax.add_collection3d(poly)

# # ax.set_xlim(0,5)

# # ax.set_ylim(0,5)

# # ax.set_zlim(0,5)    
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

point  = np.array([1, 2, 3])
normal = np.array([1, 1, 2])

# a plane is a*x+b*y+c*z+d=0
# [a,b,c] is the normal. Thus, we have to calculate
# d and we're set
d = -point.dot(normal)

# create x,y
xx, yy = np.meshgrid(range(10), range(10))

# calculate corresponding z
z = (-normal[0] * xx - normal[1] * yy - d) * 1. /normal[2]

# plot the surface
plt3d = plt.figure().gca(projection='3d')
plt3d.plot_surface(xx, yy, z)
plt3d.set_xlabel('X Label')
plt3d.set_ylabel('Y Label')
plt3d.set_zlabel('Z Label')
plt.show()