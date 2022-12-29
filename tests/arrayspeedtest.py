import numpy as np

a = np.random.rand(200,200)
b = np.random.rand(200,200)
#print(a)
# for i in range(100):
#     for x in range(a.shape[0]):
#         for y in range(a.shape[1]):
#             a[x,y] = a[x,y] * 0.9 + a[(x+1)%a.shape[0], y]*0.1 + \
#                      a[(x+2)%a.shape[0], y]*0.1 + a[(x+3)%a.shape[0], y]*0.1

# for i in range(100):
#      for x in range(a.shape[0]):
#          for y in range(a.shape[1]):
#              a[x,y] = a[x,y] * 1.02 - b[x,y] * 0.02
#for i in range(10000):
#    a = a * 1.02 - b * 0.02

# for i in range(100):
#     new_a = np.array([[a[x,y] * 0.9 + a[(x+1)%a.shape[0], y]*0.1 + \
#             a[(x+2)%a.shape[0], y]*0.1 + a[(x+3)%a.shape[0], y]*0.1 \
#              for x in range(a.shape[0])] for y in range(a.shape[1])])
#a = np.random.rand(2,3)
print(a)
for i in range(100):
    new_a = np.empty_like(a)
    new_a[:,1:] = a[:,1:] * 0.9 + a[:,:-1] * 0.1
    new_a[:,:1] = a[:,:1]
    a = new_a
print(new_a)
