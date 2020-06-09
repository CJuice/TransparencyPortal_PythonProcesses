"""
Transform the budget data from the delivered format to the format expected by the FME process.
The delivered data contains multiple columns that must be condensed into a single common column. The three columns
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
    import os

    # VARIABLES
    _root_proj_path = os.path.dirname(__file__)
    original_data_files_path = r"..\2020001_Update\OriginalData"
    transformed_data_files_path = r"..\2020001_Update\TransformedData"
    assert os.path.exists(original_data_files_path)
    assert os.path.exists(transformed_data_files_path)

    source_data_file = fr"{original_data_files_path}/FY 2020 and FY 2021 Post Session for Open Data Portal - Exp Data.xlsx"
    assert os.path.exists(source_data_file)
    transformed_data_file = fr"{transformed_data_files_path}/FY2020through2021 - Budget - Data Only_TRANSFORMED.xlsx"

    # Need to verify these each round of updates to make sure these column headers are in the source data file
    common_headers = ["Fiscal Year", "Agency Code", "Agency Name", "Unit Code", "Unit Name", "Program Code",
                      "Program Name", "Subprogram Code", "Subprogram Name", "Object Code", "Object Name",
                      "Comptroller Subobject Code", "Comptroller Subobject Name", "Agency Subobject Code",
                      "Agency Subobject Name", "Fund Type Name"]

    # header_working = "FY 2020 Working"
    # header_legislative = "FY 2021 Legislative Appropriation"
    # fy_20_headers = common_headers + [header_working]
    # fy_21_headers = common_headers + [header_legislative]

    aggregation_field_name = "Budget"
    fiscal_year_header_str = "Fiscal Year"
    fy_lead_string = "FY "

    # FUNCTIONS

    # FUNCTIONALITY
    # Read data file
    orig_df = pd.read_excel(source_data_file)

    # For each of the three FY's, perform the following actions.
    # Need to create a dataframe for each fiscal year, only including budget data relevant to that year.
    # NOTE: Data provided by the SME included the text "FY " in front of the year value. Integer desired, remove strings
    dataframes_list = []
    fiscal_years_dict = {"FY 2020": "FY 2020 Working", "FY 2021": "FY 2021 Legislative Appropriation"}

    for fy_str, column_name in fiscal_years_dict.items():
        print(f"\nProcessing {fy_str} column '{column_name}'")
        fy_headers = common_headers + [column_name]

        # Need to isolate the columns of interest for the fy of focus. Pass a list of columns to a copy of the orig df
        fy_df = orig_df.copy()[fy_headers]

        # Need to rename the fy specific column to the common name for later concatenation
        fy_df.rename(columns={column_name: aggregation_field_name}, inplace=True)

        # Need to remove the 'FY ' from the fiscal year values
        fy_df[fiscal_year_header_str] = fy_df[fiscal_year_header_str].apply(lambda x: int(x.replace(fy_lead_string, "")))

        # Remnant Note, may be valuable on future rounds
        # fy_df["Type"] = "Budget-[Working/Allowance]"  # Completed in FME, would be either of the terms in brackets []

        dataframes_list.append(fy_df)

    # Aggregate the dataframes and concatenate into a single dataframe for output.
    new_master_df = pd.concat(dataframes_list)

    # print out some stats as a sanity check
    orig_shape = orig_df.shape
    new_shape = new_master_df.shape
    orig_col_count = orig_shape[0]
    new_col_count = new_shape[0]
    number_of_years_this_round = len(fiscal_years_dict)

    print(f"\nOriginal dataset was shape: {orig_df.shape}")  # New output will be multiple times the size of this output
    print(f"\nTransformed dataset is shape: {new_master_df.shape}")
    print(f"\nNew dataset record count is {number_of_years_this_round} times the original column count: {orig_col_count*number_of_years_this_round == new_col_count}\n")
    new_master_df.info()

    # EXCEL OUTPUT
    new_master_df.to_excel(transformed_data_file, index=False)

    # CSV OUTPUT
    # new_master_df.to_csv(path_or_buf=fund_source_data_file_transformed_csv, index=False)
    print("Process Complete")
    return


if __name__ == "__main__":
    main()
