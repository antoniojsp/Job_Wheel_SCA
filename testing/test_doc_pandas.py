import pandas as pd
url = ("https://docs.google.com/spreadsheets/d/11trob6GMCskw1qbvILMPKBeJlKxTh_b_PfG9Iy80uVo/export?format=csv&gid"
       "=1847066599")
df = pd.read_csv(url)

lista = df.values.tolist()

for i in lista:
    print(i[:6])