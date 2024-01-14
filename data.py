import pandas as pd
# https://docs.google.com/spreadsheets/d/11trob6GMCskw1qbvILMPKBeJlKxTh_b_PfG9Iy80uVo/edit?usp=sharing
SHEET_ID = '11trob6GMCskw1qbvILMPKBeJlKxTh_b_PfG9Iy80uVo'
SHEET_NAME = 'WINTER_2024'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
df = pd.read_csv(url)
print(df.head())