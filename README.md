# IRFMN
Code used for data extraction/transformation/loading from M3DB in preparation for the presentation entitled **"Neuroprognostication after cardiac arrest: Working hypothesis with a multistate Markov model"**, GiVITI Meeting 2024.

## - data_filter.py
Contains the function below:
**filter_data**(csv_path, uid_path, output_csv, filter_variable, filter_operator, filter_value, date_variable, date_operator, date_value, show=True)

Arguments:
- csv_path= path to input dataset
- uid_path= path to UID mapper
- output_csv = path to output dataset 
- filter_variable = Drugs? Devices?
- filter_operator = >, <, ...
- filter_value = you choose
- date_variable = which date?
- date_operator = >, <, ...
- date_value = you choose
- show = boolean, plot a graph.

## - giviti.scripts_new.py
Contains the functions below:
- **extract**(csv_path, uid_path, output_csv, filter_variable, filter_operator, filter_value, date_variable, date_operator, date_value, show=True)
- **csvmerge**(files, output_file)

## - t3824h.py
Deprecated extraction function.
