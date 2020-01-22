"""
Transform the budget data from the delivered format to the format expected by the FME process.
The delivered data contains muttiple columns that must be condensed into a single common column. The three columns
are budget values for different fiscal years. The multiple years must be collapsed into a single column. This
process makes a dataframe for each of the fiscal year columns. Each dataframe is identical except for the year of
data that is kept. The other two are dropped. Each new dataframe has a new column added named Budget. This is the
single column into which each years worth of budget data is collapsed. The multiple data frames are then concatenated
to gain a single dataframe for output. Pat M., the original staff member to process the data, performed these moves
manually in excel.
"""


def main():

    # IMPORTS
    import pandas as pd

    # VARIABLES
    # original_headers = ['Fiscal Year', 'Agency Code', 'Agency Name', 'Unit Code', 'Unit Name',
    #    'Program Code', 'Program Name', 'Fund Type Name', 'Fund Source Code',
    #    'Fund Source Name', 'FY 2019 Budget Book Actuals',
    #    'FY 2020 Budget Book Working', 'FY 2021 Governors Allowance']
    common_headers = ['Fiscal Year', 'Agency Code', 'Agency Name', 'Unit Code', 'Unit Name',
       'Program Code', 'Program Name', 'Fund Type Name', 'Fund Source Code',
       'Fund Source Name']
    fy_19_headers = common_headers + ["FY 2019 Budget Book Actuals"]
    fy_20_headers = common_headers + ["FY 2020 Budget Book Working"]
    fy_21_headers = common_headers + ["FY 2021 Governors Allowance"]
    source_data_file = r"OfficialData/FY 2019 Actuals through FY 2021 Allowance for Open Data Portal - Funds - Data Only.xlsx"
    source_data_file_transformed_xlsx = r"TransformedData/FY 2019 Actuals through FY 2021 Allowance for Open Data Portal - Funds - Data Only_TRANSFORMED.xlsx"
    source_data_file_transformed_csv = r"TransformedData/FY 2019 Actuals through FY 2021 Allowance for Open Data Portal - Funds - Data Only_TRANSFORMED.csv"
    aggregation_field_name = "Budget"
    fiscal_year = "Fiscal Year"

    # FUNCTIONS

    # FUNCTIONALITY
    # Read data file
    orig_df = pd.read_excel(source_data_file)

    # For each of the three FY's, perform the following actions.
    # Create a dataframe for each fiscal year, only including budget data relevant to that year.
    # Data provided by the SME included the text "FY " in front of the year value. Integer is desired, remove strings
    # First FY
    fy_19_only_df = orig_df[fy_19_headers]
    fy_19_only_df = fy_19_only_df.rename(columns={"FY 2019 Budget Book Actuals": aggregation_field_name})
    fy_19_only_df[fiscal_year] = fy_19_only_df[fiscal_year].apply(lambda x: int(x.strip("FY ")))
    # print(fy_19_only_df.info())

    # Second FY
    fy_20_only_df = orig_df[fy_20_headers]
    fy_20_only_df = fy_20_only_df.rename(columns={"FY 2020 Budget Book Working": aggregation_field_name})
    fy_20_only_df[fiscal_year] = fy_20_only_df[fiscal_year].apply(lambda x: int(x.strip("FY ")))
    # print(fy_20_only_df.info())

    # Third FY
    fy_21_only_df = orig_df[fy_21_headers]
    fy_21_only_df = fy_21_only_df.rename(columns={"FY 2021 Governors Allowance": aggregation_field_name})
    fy_21_only_df[fiscal_year] = fy_21_only_df[fiscal_year].apply(lambda x: int(x.strip("FY ")))
    # print(fy_21_only_df.info())

    # Aggregate the dataframes and concatenate into a single dataframe for output.
    dataframes_list = [fy_19_only_df, fy_20_only_df, fy_21_only_df]
    new_master_df = pd.concat(dataframes_list)

    # print out some stats as a sanity check
    orig_shape = orig_df.shape
    new_shape = new_master_df.shape
    orig_col_count = orig_shape[0]
    new_col_count = new_shape[0]
    print(f"Original dataset was shape: {orig_df.shape}") # The new output will be 3 times the size of this output
    print(f"Transformed dataset is shape: {new_master_df.shape}")
    print(f"\nNew dataset record count is 3 times the original column count: {orig_col_count*3 == new_col_count}\n")
    new_master_df.info()

    # EXCEL OUTPUT
    new_master_df.to_excel(source_data_file_transformed_xlsx, index=False)

    # CSV OUTPUT
    # new_master_df.to_csv(path_or_buf=fund_source_data_file_transformed_csv, index=False)
    print("Process Complete")
    return


if __name__ == "__main__":
    main()
