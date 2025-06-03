import numpy as np
import pandas as pd

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

produce=["apples","grapes","bananas","lemons"]
prices=[100,200,180,60]

sale_produce=pd.Series(prices,index=produce)
print(sale_produce)

print(sale_produce["grapes"])

total_sales=sale_produce.sum()
print(total_sales)

best_seller=sale_produce.idxmax()
print(f"Best seller is:{best_seller}")

data={
    "Name" :["leon","dion","edin"],
    "Age":[16,18,17],
    "City":["Prishtina","Prizren","Gjakova"]
}

df=pd.DataFrame(data)
print(df)

df=pd.read_csv(cs.csv)
df.to_csv("dion", index= False)