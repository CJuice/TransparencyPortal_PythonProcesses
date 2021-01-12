"""
Transform the finance data from the delivered format to the format expected by the FME process.
The delivered data contains multiple columns that must be condensed into a single common column. The columns
to be condensed vary update to update. The multiple columns of FY specific data must be collapsed into a single
column. This process makes a dataframe for each of the fiscal year columns. Each dataframe is identical
except for the year of data that is kept. The other two are dropped. Each new dataframe has a new column
added, which is the aggregation field. This is the single column into which each years worth of data is collapsed.
The multiple data frames are then concatenated to gain a single dataframe for output.
Pat M., the original staff member to process the data, performed these moves manually in excel.
NOTE: There are controlling boolean variables that determine the dataset on which the process operates. This script
is a tool to be applied to one of the four datasets it was designed to transform. Switch False to True to run on
a particular dataset and then switch it back after successful completion. Check the column headers match those in the
data files and change the data files path variables to operate on the most recent data.

Author: CJuice
Created: ~20200101
Revisions: 20200601, CJuice, Collapsed the four independent scripts for budget, funding, fte, and cur/cr into a
    single script.
    20200615, CJuice, Process was convert "Program Code" from string like number to integer. Revised to include dtypes
"""


def main():

    # IMPORTS
    import os
    import pandas as pd
    import doit_centralizedvariables as myvars

    # VARIABLES
    # _root_proj_path = os.path.dirname(__file__)
    ##########
    # Will change with each update
    _root_update_folder_path = r"..\20210111_Budget_Update"
    budget_source_filename = "FY 2020 through FY 2022 Gov Allowance for Open Data Portal - Expenditure Data.xlsx"
    fte_source_filename = "FY 2020 through FY 2022 Gov Allowance for Open Data Portal - FTE Data.xlsx"
    funds_source_filename = "FY 2020 through FY 2022 Gov Allowance for Open Data Portal - Funds Data Only.xlsx"
    cur_cr_source_filename = "FY 2020 through FY 2022 Gov Allowance for Open Data Portal - Higher Ed Exp Data.xlsx"
    official_data_folder = f"{_root_update_folder_path}\OfficialData"
    transformed_data_folder = f"{_root_update_folder_path}\TransformedData"
    # source_budget_data_file = "FY 2020 through FY 2022 Gov Allowance for Open Data Portal - Expenditure Data.xlsx"
    # transformed_budget_data_file = source_budget_data_file.replace(".xlsx", "_TRANSFORMED.xlsx")
    # source_data_file = f"{official_data_folder}/{source_budget_data_file}"
    # source_data_file_transformed_xlsx = f"{transformed_data_folder}/{transformed_budget_data_file}"
    first, second, third = (2020, 2021, 2022)
    first_header = f"FY {first} Budget Book Actuals"
    second_header = f"FY {second} Budget Book Working"
    third_header = f"FY {third} Governors Allowance"

    ##########

    aggregation_field_name = "Budget"
    csv_out = False
    dataframes_list = []
    excel_out = True
    fiscal_year_header_str = "Fiscal Year"
    fiscal_years_dict = {f"FY {first}": first_header, f"FY {second}": second_header, f"FY {third}": third_header}
    fy_lead_string = "FY "
    assert os.path.exists(official_data_folder)
    assert os.path.exists(transformed_data_folder)

    # FUNCTIONS
    def name_transformed(filename: str) -> str:
        excel_ending = ".xlsx"
        return filename.replace(excel_ending, f"_TRANSFORMED{excel_ending}")

    # FUNCTIONALITY

    # CONTROL: Toggle data type of focus. Process is same for each but headers vary. The headers must be verified first!
    #   Only highest True will execute
    budget = True
    funding = False
    fte = False
    cur_cr = False

    if budget:

        # Budget Files
        source_data_file = fr"{official_data_folder}/{budget_source_filename}"
        assert os.path.exists(source_data_file)
        # data_type = "Budget"
        transformed_data_file = fr"{transformed_data_folder}/{name_transformed(budget_source_filename)}"

        # Need to verify these each round of updates to make sure these column headers are in the source data file
        common_headers = myvars.budget_common_headers
    elif funding:

        # Funding Files
        source_data_file = fr"{official_data_folder}/{funds_source_filename}"
        assert os.path.exists(source_data_file)
        # data_type = "Funding"
        transformed_data_file = fr"{transformed_data_folder}/{name_transformed(funds_source_filename)}"

        # Need to verify these each round of updates to make sure these column headers are in the source data file
        common_headers = myvars.funding_common_headers
    elif fte:

        # FTE Files - The source file does not contain a 'Fiscal Year' field
        source_data_file = fr"{official_data_folder}/{fte_source_filename}"
        assert os.path.exists(source_data_file)
        data_type = "FTE"
        aggregation_field_name = "Count"  # UNIQUE
        transformed_data_file = fr"{transformed_data_folder}/{name_transformed(fte_source_filename)}"

        # Need to verify these each round of updates to make sure these column headers are in the source data file
        common_headers = myvars.fte_common_headers
    elif cur_cr:

        # CUR/CR Files
        source_data_file = fr"{official_data_folder}/{cur_cr_source_filename}"
        data_type = "CUR-CR"
        transformed_data_file = fr"{transformed_data_folder}/{name_transformed(cur_cr_source_filename)}"

        # Need to verify these each round of updates to make sure these column headers are in the source data file
        common_headers = myvars.cur_cr_common_headers
    else:
        common_headers = None
        source_data_file = None
        transformed_data_file = None
        print("All categories are False. Exiting")
        exit()

    assert os.path.exists(source_data_file)

    # Read data file
    print(f"Processing {source_data_file}")
    common_column_dtypes_dict = {header: str for header in common_headers}
    fiscal_year_columns_dtypes_dict = {header: "float" for header in fiscal_years_dict.values()}
    master_dtypes = {**common_column_dtypes_dict, **fiscal_year_columns_dtypes_dict}
    orig_df = pd.read_excel(io=source_data_file, dtype=master_dtypes)
    print(f"Initial data load...\n{orig_df.info()}\n")

    # For each of the FY's, perform the following actions.
    # Need to create a dataframe for each fiscal year, only including budget data relevant to that year.
    # NOTE: Data provided by DBM included the text "FY " in front of the year value. Integer desired, remove strings.
    #   FTE data is unique, doesn't contain a Fiscal Year column so creation and assignment must occur
    for fy_str, column_name in fiscal_years_dict.items():
        print(f"\nProcessing {fy_str} column '{column_name}'")
        fy_focus = int(fy_str.replace(fy_lead_string, ""))
        fy_headers = common_headers + [column_name]

        # Need to isolate the columns of interest for the fy of focus. Pass a list of columns to a copy of the orig df
        fy_df = orig_df.copy()[fy_headers]

        # Need to rename the fy specific column to the common name for later concatenation of dataframes
        fy_df.rename(columns={column_name: aggregation_field_name}, inplace=True)

        # Need to remove the 'FY ' from the fiscal year values, except if FTE data
        if fte:

            # Special handing for FTE because source data does not contain a 'Fiscal Year' column
            fy_df[fiscal_year_header_str] = fy_focus
        else:

            # Could potentially be straight assignment of fy_focus value but seemed safer to work with provided values.
            fy_df[fiscal_year_header_str] = fy_df[fiscal_year_header_str].apply(
                lambda x: int(x.replace(fy_lead_string, "")))

        # Remnant Note, may be valuable on future rounds
        # fy_df["Type"] = "Budget-[Working/Allowance]"  # Completed in FME, would be either of the terms in brackets []

        dataframes_list.append(fy_df)

        print(fy_df.info())

    # Concatenate into a single dataframe for output.
    new_master_df = pd.concat(dataframes_list)

    # Print out some stats as a sanity check
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
    if excel_out:
        print("Outputing to Excel...")
        new_master_df.to_excel(transformed_data_file, index=False)

    # CSV OUTPUT
    if csv_out:
        print("Outputing to CSV...")
        new_master_df.to_csv(path_or_buf=transformed_data_file, index=False)

    print("Process Complete")
    return


if __name__ == "__main__":
    main()
