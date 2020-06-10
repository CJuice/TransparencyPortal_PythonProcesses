"""
Main purpose is an emergency fix to populate the Type column in the Budget data.
The values for FY that nathan gave me were strings, not integers.
The FME job was set up to map integers to its values so it failed to populate anything for the entire column.
The upfront python processes now strip FY from the source data and convert the year to an integer.
As a result, the FME job should now populate the values. The 20200101 update required an emergency fix
with this script.

Author: CJuice
Created: ~20200101
"""


def main():

    # IMPORTS
    import pandas as pd

    # VARIABLES
    data_file_to_fix_csv = r"C:\Users\Conrad.Schaefer\Documents\DoIT_TransparencyWebsiteDataUpdate\FME_Workbench\TestOutput\budget_test\budget_test_manuallyeditedtoremoveextracolumns_noFYtext.csv"
    data_file_to_fix_csv_revised = r"C:\Users\Conrad.Schaefer\Documents\DoIT_TransparencyWebsiteDataUpdate\FME_Workbench\TestOutput\budget_test\budget_test_manuallyeditedtoremoveextracolumns_noFYtext_TypeFixed.csv"
    data_file_to_fix_xlsx = r"C:\Users\Conrad.Schaefer\Documents\DoIT_TransparencyWebsiteDataUpdate\FME_Workbench\TestOutput\budget_test\budget_test_manuallyeditedtoremoveextracolumns_noFYtext.xlsx"
    budget_actual = "Budget - Actual"
    budget_working = "Budget - Working"
    budget_allowance = "Budget - Allowance"

    # NOTE: This dictionary will likely change with each update.
    year_to_value_dict = {2017: budget_actual, 2018: budget_actual, 2019: budget_actual, 2020: budget_working, 2021: budget_allowance}

    # FUNCTIONS

    # FUNCTIONALITY
    # Create the dataframe from the data file
    # df = pd.read_csv(filepath_or_buffer=data_file_to_fix_csv)
    df = pd.read_excel(data_file_to_fix_xlsx)
    print(df.info())

    # Calculate the values in the Type field based on the fiscal year values
    df["Type"] = df["Fiscal Year"].apply(lambda x: year_to_value_dict.get(x))
    print(df.info())

    # Output the revised data
    df.to_csv(path_or_buf=data_file_to_fix_csv_revised, index=False)
    print("Process Complete")


if __name__ == "__main__":
    main()