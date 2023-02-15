import pandas as pd
import os
from IPython.display import display

print(os.getcwd())
df1 =  pd.read_csv("blabla.csv")
df2 =  pd.read_csv("blabla.csv")




df1.columns = pd.MultiIndex.from_product([["2020"], df1.columns])
df2.columns = pd.MultiIndex.from_product([["2021"], df2.columns])

df = pd.concat([df1, df2], axis=1)


display(df)

df.to_csv("ttt.csv", encoding="cp949", index=False)
df.to_excel("ttt.xlsx", encoding="cp949")