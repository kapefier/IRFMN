import csv
import os
import pandas as pd

df = pd.read_csv("01_Temperatura.csv")
df.head()
 
t38df = df[(df['VALORE'] >= 38) & (df['DATASTART'] < 1440)]['UID'].drop_duplicates()
  for uid in t38df:
     print(uid)

print("\nCount:", t38df.nunique())
df['t38df'] = df.groupby('UID').apply(lambda x: ((x['VALORE'] >= 38) & (x['DATASTART'] < 1440)).any()).astype(int).values
t38df = df.drop_duplicates(subset='UID', keep='first').copy
print( t38df[t38df['t38in24h'] == 1)

# Create the new column 't38df' which contains True if VALORE for every single UID is at least one time >= 38 and DATASTART is < 1440
df['t38df'] = df.groupby('UID').apply(lambda x: ((x['VALORE'] >= 38) & (x['DATASTART'] < 1440)).any()).reset_index(drop=True)

# Create a new DataFrame without the 'VALORE' and 'DATASTART' columns, and with unique UIDs
new_df = df.drop(columns=['VALORE', 'DATASTART']).drop_duplicates(subset='UID')

# Display the first few rows of the new DataFrame
print(new_df.head())
