"""
TODO
Replaces FME process for FTE data.

Author: CJuice
Created: 20200612
Revisions:
"""


def main():

    # IMPORTS
    import datetime
    import doit_centralizedvariables as myvars
    import os
    import pandas as pd

    # VARIABLES
    _root_project_path = os.path.dirname(__file__)
    today_str = datetime.datetime.today().strftime("%Y%m%d")

    agency_categories_file = myvars.agency_categories_file
    data_category = "FTE"
    full_pandas_df_printing = True
    output_result_csv = fr"../20200601_Update/20200615_PythonResults/{today_str}_{data_category}_pythonoutput.csv"
    state_program_descriptions_file = myvars.state_program_descriptions_file
    transformed_data_file = fr"../20200601_Update/20200609_TransformedData/FY2020through2021 - {data_category} - Data Only_TRANSFORMED.xlsx"

    # ASSERTS
    assert os.path.exists(transformed_data_file)
    assert os.path.exists(state_program_descriptions_file)
    assert os.path.exists(agency_categories_file)

    # FUNCTIONALITY
    if full_pandas_df_printing:
        # pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        # pd.set_option('display.max_colwidth', -1)

    # Need to control the dtypes to avoid conversion of strings like 'Program Code' to integers (stripping leading zero)
    column_headers = myvars.funding_common_headers
    budget_dtype = {"Budget": "float"}
    master_dtypes = {**budget_dtype, **{header: str for header in column_headers}}

    # Need the data with appropriate dtypes as df
    data_df = pd.read_excel(io=transformed_data_file, dtype=master_dtypes)

    # CSV versions - This method does not convert '05' into an integer but leaves it as string, without using dtypes
    #   In addition, could provide encoding to bypass issue with bytes
    state_programs_df = pd.read_csv(filepath_or_buffer=state_program_descriptions_file, encoding="Windows-1252")
    agency_categories_df = pd.read_csv(filepath_or_buffer=agency_categories_file)

    # Need to create the Organization Code column and populate in the data dataframe
    data_df["Organization Code"] = data_df.apply(
        lambda row: str(f"{row['Agency Code']}_{row['Unit Code']}_{row['Program Code']}"), axis=1)
    print(data_df.info())
    exit()



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

    second_join_df.to_csv(path_or_buf=output_result_csv, index=False)
    return


if __name__ == "__main__":
    main()
