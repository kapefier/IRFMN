# givithon_scripts_new.py

# Usage example:
#  
#  extractor = Extractor("../Devices.csv",  "../UID.csv",
#   "NOMEPRESIDIO", "=", "ECMO",
#   "DATAINIZIO", "<=", 1440)
#   extractor.save("output.csv", show=True)
#
#   merge(['file1', 'file2', 'file3'], 'merged_output')
#   filenames with no suffix... appending .csv

#   combine('combined_output', [extractor1, extractor2, extractor3])

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class Extractor:
    operators = {
        '=': lambda x, y: x == y,
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '>=': lambda x, y: x >= y,
        '<=': lambda x, y: x <= y
    }

    def __init__(self, csv_path: str, uid_path, filter_variable, filter_operator, filter_value, data_variable, data_operator, data_value):
        self.csv_path = csv_path
        self.uid_path = uid_path
        self.filter_variable = filter_variable
        self.filter_operator = filter_operator
        self.filter_value = filter_value
        self.data_variable = data_variable
        self.data_operator = data_operator
        self.data_value = data_value
        self.uids_sorted = None

    def save(self, output, show=True):
        if (self.filter_operator not in self.operators or self.data_operator not in self.operators):
            raise ValueError(
                "Invalid operator. Use one of '=', '>', '<', '>=', '<='.")
        if output[-4:] != '.csv': 
            output = output + '.csv'    

        # side effect : leggere dal csv
        df = pd.read_csv(self.csv_path)
        uids = pd.read_csv(self.uid_path, usecols=[1])

        # logica
        uids_sorted = self.extract(df, uids)

        # side effect : scrivere su csv
        uids_sorted.to_csv(output, index=False)

        # side effect : mostrare il plot
        if show:
            self.__plot(uids_sorted)

    def extract(self, df, uids):
        # Ensure the filter value and column values are of the same type
        filter_value = self.filter_value
        data_value = self.data_value

        # Convert to appropriate types if necessary
        if df[self.filter_variable].dtype != type(filter_value):
            filter_value = df[self.filter_variable].dtype.type(filter_value)
        if df[self.data_variable].dtype != type(data_value):
            data_value = df[self.data_variable].dtype.type(data_value)

        # Apply filter and data conditions
        filter_condition = self.operators[self.filter_operator](df[self.filter_variable], filter_value)
        data_condition = self.operators[self.data_operator](df[self.data_variable], data_value)
    
        # Apply combined condition
        filtered_uids = df[filter_condition & data_condition]['UID'].tolist()
        uids[filter_value] = uids.UID.map(set(filtered_uids).__contains__)
    
         # Sort uids by UID
        uids_sorted = uids.sort_values(by='UID')

        return uids_sorted
    
  
   
    def __plot(self, uids):
        # Print the results
        total_uids = len(uids)
        total_true = uids[self.filter_value].sum()
        percentage_true = (total_true / total_uids) * 100

        print(f"N of pts with {self.filter_variable} recorded: {total_uids}")
        print(f"Filter applied: {self.filter_variable} {self.filter_operator} {self.filter_value} AND {self.data_variable} {self.data_operator} {self.data_value} minutes")
        print(f"N of pts: {total_true} ")
        print(f"Percentage of pts: {percentage_true:.2f}%")

        # Set Plot
        labels = ['True', 'False']
        sizes = [total_true, total_uids - total_true]

        # Plot using Seaborn
        sns.set(style='whitegrid')
        plt.figure(figsize=(4, 4))
        plt.pie(sizes, explode=[0.1, 0], labels=labels, colors=['#1E90FF', 'white'], autopct='%1.1f%%', shadow=True, startangle=140, textprops={'fontsize': 9})
        plt.title(f"{self.filter_value} {self.data_operator} {str(self.data_value)} minutes", fontsize=12, fontweight='bold')
        plt.show()
    


def merge(files, output, filetype='csv'):
    if filetype == 'csv':
        files = [f"{file}.csv" for file in files]
        merged_df = pd.DataFrame()
        for file in files:
            df = pd.read_csv(file)
            if 'UID' not in df.columns:
                raise ValueError(f"File {file} does not contain 'UID' column.")
            if merged_df.empty:
                merged_df = df
            else:
                merged_df = pd.merge(merged_df, df, on='UID', suffixes=('', f'_{files.index(file)}'))
        merged_df.to_csv(f'{output}.csv', index=False)
    else: 
        raise ValueError("Invalid filetype. Use 'csv'.")

def combine(combined_col, extractors):
    if not extractors:
        raise ValueError("At least one extractor must be provided.")

    combined_uids = pd.DataFrame()

    for extractor in extractors:
        df = pd.read_csv(extractor.csv_path)
        uids = pd.read_csv(extractor.uid_path, usecols=[1])
        extracted_uids = extractor.extract(df, uids).copy()
        if combined_uids.empty:
            combined_uids = extracted_uids
        else:
            combined_uids = pd.concat([combined_uids, extracted_uids]).drop_duplicates().reset_index(drop=True)

    # Create a combined DataFrame where each row assumes value True if it is True in one or more datasets
    combined_uids['UID'] = combined_uids['UID'].astype(str)
    combined_uids['Value'] = combined_uids.drop(columns=['UID']).any(axis=1)
    combined_df = combined_uids.groupby('UID').max().reset_index()

    # Keep only UID and Value columns
    combined_df = combined_df[['UID', 'Value']]

    # Rename Value column to output_csv
    combined_df.rename(columns={'Value': combined_col}, inplace=True)

    
    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(combined_col, index=False)
    
    
    # Plot using extractor's plot method
    #__plot(combined_df[[output_csv]])
    # Print the results
    total_uids = len(combined_df)
    total_true = combined_df[combined_col].sum()
    percentage_true = (total_true / total_uids) * 100

    #print(f"N of pts with {self.filter_variable} recorded: {total_uids}")
    #print(f"Filter applied: {self.filter_variable} {self.filter_operator} {self.filter_value} AND {self.data_variable} {self.data_operator} {self.data_value} minutes")
    #print(f"N of pts: {total_true} ")
    #print(f"Percentage of pts: {percentage_true:.2f}%")

    # Set Plot
    labels = ['True', 'False']
    sizes = [total_true, total_uids - total_true]

    # Plot using Seaborn
    sns.set(style='whitegrid')
    plt.figure(figsize=(4, 4))
    plt.pie(sizes, explode=[0.1, 0], labels=labels, colors=['#1E90FF', 'white'], autopct='%1.1f%%', shadow=True, startangle=140, textprops={'fontsize': 9})
    #plt.title(f"{self.filter_value} {self.data_operator} {str(self.data_value)} minutes", fontsize=12, fontweight='bold')
    plt.show()

    return combined_df