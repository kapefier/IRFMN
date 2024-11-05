# data_filter.py

# Usage example: 
#   filter_data("../Devices.csv",  "../UID.csv", 
#   "ECMO-a-24h.csv", 
#   "NOMEPRESIDIO", "=", "ECMO", 
#   "DATAINIZIO", "<=", 1440,
#    show=True)
       



import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

def filter_data(csv_path, uid_path, output_csv, filter_variable, filter_operator, filter_value, data_variable, data_operator, data_value, show=True):
    
    # Load data
    df = pd.read_csv(csv_path)
    uids = pd.read_csv(uid_path, usecols=[1])
    
    # Define filter function based on operator
    if filter_operator == '=':
        filter_condition = df[filter_variable] == filter_value
    elif filter_operator == '>':
       filter_condition = df[filter_variable] > filter_value
    elif filter_operator == '<':
        filter_condition = df[filter_variable] < filter_value
    elif filter_operator == '>=':
        filter_condition = df[filter_variable] >= filter_value
    elif filter_operator == '<=':
        filter_condition = df[filter_variable] <= filter_value
    else:
        raise ValueError("Invalid operator. Use one of '=', '>', '<', '>=', '<='.")
        
    # Define data function based on operator
    if data_operator == '=':
        data_ondition = df[data_variable] == data_value
    elif data_operator  == '>':
        data_condition = df[data_variable] > data_value
    elif data_operator  == '<':
        data_condition = df[data_variable] < data_value
    elif data_operator  == '>=':
        data_condition = df[data_variable] >= data_value
    elif data_operator  == '<=':
        data_condition = df[data_variable] <= data_value
    else:
        raise ValueError("Invalid operator. Use one of '=', '>', '<', '>=', '<='.")
    
    # Apply filter
    filtered_uids = df[filter_condition & data_condition]['UID'].tolist()
    uids[filter_value] = uids.UID.map(lambda x: x in filtered_uids)
    
    # Sort uids by UID
    uids_sorted = uids.sort_values(by='UID')
    
    # Save the sorted DataFrame to a CSV file
    uids_sorted.to_csv(output_csv, index=False)

    if show:
        # Print the results
        total_uids = uids.shape[0]
        total_true = uids[filter_value].sum()
        percentage_true = (total_true / total_uids) * 100
    
        print(f"N of pts with {filter_variable} recorded: {total_uids}")
        print(f"Filter applied: {filter_variable} {filter_operator} {filter_value} AND {data_variable} {data_operator} {data_value} minutes")
        print(f"N of pts: {total_true} ")
        print(f"Percentage of pts: {percentage_true:.2f}%")

        # Set Plot
        labels = ['True', 'False']
        sizes = [total_true, total_uids - total_true]
        colors = ['red', 'lightgreen']
        explode = (0.1, 0)
    
        # Plot
        plt.figure(figsize=(4, 4))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.title(filter_value+" "+data_operator+" "+str(data_value)+" minuti")
        plt.show()
        
 
       
       
       
