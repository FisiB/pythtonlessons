import numpy as np

array_2d= np.array([[1,2,3,4,5],[6,7,8,9,10]])

print(array_2d)

element= array_2d[1,2]
print(element)

dim=array_2d.ndim
print(dim)

size=array_2d.size
print(size)

total_sum=np.sum(array_2d)
print(total_sum)

sum_coloum=np.sum(array_2d, axis=0)
print(sum_coloum)

sum_row=np.sum(array_2d, axis=1)
print(sum_row)