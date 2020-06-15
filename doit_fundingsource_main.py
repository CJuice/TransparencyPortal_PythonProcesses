"""
TODO
Replaces FME process for Funding Source data.

Author: CJuice
Created: 20200612
Revisions:
"""


def main():

    # IMPORTS
    import pandas as pd
    import os

    # VARIABLES
    _root_project_path = os.path.dirname(__file__)
    transformed_data_file = fr"../20200601_Update/20200609_TransformedData/FY2020through2021 - Funding - Data Only_TRANSFORMED.xlsx"
    # state_program_descriptions_file = fr"../20200601_Update/20200609_ExtraRequiredFiles/20200127_StateProgramDescriptions.xlsx"
    state_program_descriptions_file = fr"../20200601_Update/20200609_ExtraRequiredFiles/20200127_StateProgramDescriptions.csv"
    # agency_categories_file = fr"../20200601_Update/20200609_ExtraRequiredFiles/20200127_AgencyCategories_CJuiceCleaned.xlsx"
    agency_categories_file = fr"../20200601_Update/20200609_ExtraRequiredFiles/20200127_AgencyCategories_CJuiceCleaned.csv"
    full_pandas_df_printing = True

    # ASSERTS
    assert os.path.exists(transformed_data_file)
    assert os.path.exists(state_program_descriptions_file)
    assert os.path.exists(agency_categories_file)

    # FUNCTIONS

    # CLASSES

    # FUNCTIONALITY

    # _______________
    # GOLD: found this on a blog at https://medium.com/datadriveninvestor/data-cleaning-character-encoding-b4e0e9c65b2a
    # Used this code to discover the encoding of the state programs descriptions b/c it was failing to read as csv or
    # as excel. Ran it, grabbed the encoding, passed it to pd.read_csv and it worked.
    # import chardet
    # with open(state_program_descriptions_file, 'rb') as handler:
    #     result = chardet.detect(handler.read())
    #
    # print(result)
    # exit()
    # _______________

    if full_pandas_df_printing:
        # pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        # pd.set_option('display.max_colwidth', -1)

    # Need to control the dtypes to avoid conversion of strings like 'Program Code' to integers (stripping leading zero)
    column_dtypes = ['Fiscal Year', 'Agency Code', 'Agency Name', 'Unit Code', 'Unit Name',
                     'Program Code', 'Program Name', 'Fund Type Name', 'Fund Source Code',
                     'Fund Source Name']
    budget_dtype = {"Budget": "float"}
    master_dtypes = {**budget_dtype, **{header: str for header in column_dtypes}}

    # Need the data with appropriate dtypes as df
    data_df = pd.read_excel(io=transformed_data_file, dtype=master_dtypes)

    # Excel versions - Won't work do to encoding issue
    # state_programs_df = pd.read_excel(io=state_program_descriptions_file)
    # agency_categories_df = pd.read_excel(io=agency_categories_file)

    # CSV versions - This method does not convert '05' into an integer but leaves it as string, without using dtypes
    #   In addition, could provide encoding to bypass issue with bytes
    state_programs_df = pd.read_csv(filepath_or_buffer=state_program_descriptions_file, encoding="Windows-1252")
    agency_categories_df = pd.read_csv(filepath_or_buffer=agency_categories_file)

    # Need to create the Organization Code column and populate in the data dataframe
    data_df["Organization Code"] = data_df.apply(
        lambda row: str(f"{row['Agency Code']}_{row['Unit Code']}_{row['Program Code']}"), axis=1)

    # Need to create the Organization Code column and populate in the State Programs Descriptions dataframe
    state_programs_df["Organization Code"] = state_programs_df.apply(
        lambda row: str(f"{row['AgencyCode']}_{row['UnitCode']}_{row['ProgramCode']}"), axis=1)

    # Only need the 'Description' field joined to data table, drop all others
    org_code_parts = ["AgencyCode", "UnitCode", "ProgramCode", "AgencyName", "UnitName", "ProgramName"]
    state_programs_df.drop(columns=org_code_parts, inplace=True)

    # Need to join the state programs data to the data_df on Organization Code using left join
    # data_df.set_index(keys="Organization Code", inplace=True, drop=True)
    state_programs_df.set_index(keys="Organization Code", inplace=True, drop=True)

    first_join_df = data_df.join(other=state_programs_df, on="Organization Code")
    print(first_join_df)

    # Need to join the agency categories data to the first join df on Agency Code using left join
    first_join_df.info()
    agency_categories_drop = ["Agency Name"]
    agency_categories_df.drop(columns=agency_categories_drop, inplace=True)
    agency_categories_df.set_index(keys="Agency Code", drop=True, inplace=True)
    second_join_df = first_join_df.join(other=agency_categories_df, on="Agency Code")
    print(second_join_df)


    return


if __name__ == "__main__":
    main()
