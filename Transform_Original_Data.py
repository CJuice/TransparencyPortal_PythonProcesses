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
"""


def main():

    # IMPORTS
    import pandas as pd
    import os

    # VARIABLES
    _root_proj_path = os.path.dirname(__file__)
    aggregation_field_name = "Budget"
    csv_out = False
    dataframes_list = []
    excel_out = True
    fiscal_year_header_str = "Fiscal Year"
    fiscal_years_dict = {"FY 2020": "FY 2020 Working", "FY 2021": "FY 2021 Legislative Appropriation"}
    fy_lead_string = "FY "
    original_data_files_path = r"..\20200601_Update\OriginalData"
    transformed_data_files_path = r"..\20200601_Update\TransformedData"
    assert os.path.exists(original_data_files_path)
    assert os.path.exists(transformed_data_files_path)

    # CONTROL: Toggle data type of focus. Process is same for each but headers vary. The headers must be verified first!
    #   Only highest True will execute
    budget = False
    funding = False
    fte = False
    cur_cr = False

    if budget:

        # Budget Files
        source_data_file = fr"{original_data_files_path}/FY 2020 and FY 2021 Post Session for Open Data Portal - Exp Data.xlsx"
        assert os.path.exists(source_data_file)
        data_type = "Budget"
        transformed_data_file = fr"{transformed_data_files_path}/FY2020through2021 - {data_type} - Data Only_TRANSFORMED.xlsx"

        # Need to verify these each round of updates to make sure these column headers are in the source data file
        common_headers = ["Fiscal Year", "Agency Code", "Agency Name", "Unit Code", "Unit Name", "Program Code",
                          "Program Name", "Subprogram Code", "Subprogram Name", "Object Code", "Object Name",
                          "Comptroller Subobject Code", "Comptroller Subobject Name", "Agency Subobject Code",
                          "Agency Subobject Name", "Fund Type Name"]
    elif funding:

        # Funding Files
        source_data_file = fr"{original_data_files_path}/FY 2020 and FY 2021 Post Session for Open Data Portal - Funds Data.xlsx"
        assert os.path.exists(source_data_file)
        data_type = "Funding"
        transformed_data_file = fr"{transformed_data_files_path}/FY2020through2021 - {data_type} - Data Only_TRANSFORMED.xlsx"

        # Need to verify these each round of updates to make sure these column headers are in the source data file
        common_headers = ['Fiscal Year', 'Agency Code', 'Agency Name', 'Unit Code', 'Unit Name',
                          'Program Code', 'Program Name', 'Fund Type Name', 'Fund Source Code',
                          'Fund Source Name']
    elif fte:

        # FTE Files - The source file does not contain a 'Fiscal Year' field
        source_data_file = fr"{original_data_files_path}/FY 2020 and FY 2021 Post Session for Open Data Portal - FTE Data.xlsx"
        assert os.path.exists(source_data_file)
        data_type = "FTE"
        aggregation_field_name = "Count"  # UNIQUE
        transformed_data_file = fr"{transformed_data_files_path}/FY2020through2021 - {data_type} - Data Only_TRANSFORMED.xlsx"

        # Need to verify these each round of updates to make sure these column headers are in the source data file
        common_headers = ["Agency Code", "Unit Code", "Program Code"]
    elif cur_cr:

        # CUR/CR Files
        source_data_file = fr"{original_data_files_path}/FY 2020 and FY 2021 Post Session for Open Data Portal - Exp Higher Ed Data.xlsx"
        data_type = "CUR-CR"
        transformed_data_file = fr"{transformed_data_files_path}/FY2020through2021 - {data_type} - Data Only_TRANSFORMED.xlsx"

        # Need to verify these each round of updates to make sure these column headers are in the source data file
        common_headers = ["Fiscal Year", "Agency Code", "Agency Name", "Unit Code", "Unit Name", "Program Code",
                          "Program Name", "Subprogram Code", "Subprogram Name", "Object Code", "Object Name",
                          "Comptroller Subobject Code", "Comptroller Subobject Name", "Agency Subobject Code",
                          "Agency Subobject Name", "Fund Type Name"]
    else:
        column_headers = None
        source_data_file = None
        transformed_data_file = None
        print("All categories are False. Exiting")
        exit()

    assert os.path.exists(source_data_file)

    # FUNCTIONALITY
    # Read data file
    print(f"Processing {source_data_file}")
    orig_df = pd.read_excel(source_data_file)

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
        new_master_df.to_excel(transformed_data_file, index=False)

    # CSV OUTPUT
    if csv_out:
        new_master_df.to_csv(path_or_buf=transformed_data_file, index=False)

    print("Process Complete")
    return


if __name__ == "__main__":
    main()
