import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("01_Temperatura.csv")
df.head()
 
# filter early hypertemic patients
uids=pd.read_csv('../UID.csv', usecols=[1])
df = pd.read_csv("01_Temperatura.csv")
t38in24_uids = df[(df['VALORE'] >= 38) & (df['DATASTART'] < 1440)]['UID'].tolist()
uids['t38in24h'] = uids.UID.map(lambda x: x in t38in24_uids)

# Print the results
print(f"N of pts with temp recorded: {uids.shape[0]}")
print(f"Early hyperthermia (temp >= 38 °C within the first 24 hours)")
print(f"N of pts: {uids['t38in24h'].sum()} ")
print(f"Percentage of pts: {((uids['t38in24h'].sum() / uids.shape[0]) * 100):.2f}%")

# Set Plot
labels = ['True', 'False']
sizes = [total_true, total_uids - total_true]
colors = ['red', 'lightgreen']
explode = (0.1, 0)  # explode the 1st slice (True)

# Plot
uids_sorted = uids.sort_values(by='UID')
plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Early Hypertermia')
plt.show()
