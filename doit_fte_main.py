"""
Process the update data for FTE and output the processed data to csv.
Replaces FME process for FTE data.

Author: CJuice
Created: 20200612
Revisions:
    20210112, CJuice, Refactored to use more centralized variables. Added print statements for insights.

"""


def main():

    # IMPORTS
    import datetime
    import doit_centralizedvariables as myvars
    import os
    import pandas as pd

    # VARIABLES
    today_str = datetime.datetime.today().strftime("%Y%m%d")
    budget_column_dtype = {"Budget": "float"}
    column_headers = myvars.funding_common_headers
    data_category = "FTE"
    drop_fields = ["AgencyCode", "UnitCode", "ProgramCode", "Description"]
    full_pandas_df_printing = True
    org_code_str = "Organization Code"
    output_result_csv = fr"{myvars.python_results_folder}/{today_str}_{data_category}_pythonoutput.csv"
    rename_stateprog_names = {"AgencyName": "Agency Name", "UnitName": "Unit Name", "ProgramName": "Program Name"}
    transformed_data_file = fr"{myvars.transformed_data_folder}/FY{myvars.first}_{myvars.third}_{data_category}_TRANSFORMED.xlsx"

    # ASSERTS
    assert os.path.exists(myvars.agency_categories_file)
    assert os.path.exists(myvars.state_program_descriptions_file)
    assert os.path.exists(transformed_data_file)

    # FUNCTIONALITY
    if full_pandas_df_printing:
        # pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        # pd.set_option('display.max_colwidth', -1)

    # Need to control the dtypes to avoid conversion of strings like 'Program Code' to integers (stripping leading zero)
    master_dtypes = {**budget_column_dtype, **{header: str for header in column_headers}}

    # Need the data with appropriate dtypes as df
    data_df = pd.read_excel(io=transformed_data_file, dtype=master_dtypes)
    print(f"Transformed Data: \n{data_df.info()}")

    # Excel versions - Sometimes doesn't work do to encoding issue. Fallback to csv's in that situation.
    state_programs_df = pd.read_excel(io=myvars.state_program_descriptions_file, dtype={"ProgramCode": str})
    print(f"State Program Descriptions: \n{state_programs_df.info()}")

    # CSV versions - This method does not convert '05' into an integer but leaves it as string, without using dtypes
    #   In addition, could provide encoding to bypass issue with bytes
    # state_programs_df = pd.read_csv(filepath_or_buffer=myvars.state_program_descriptions_file, encoding="Windows-1252")

    # Need to create the Organization Code column and populate in the data dataframe
    data_df[org_code_str] = data_df.apply(
        lambda row: str(f"{row['Agency Code']}_{row['Unit Code']}_{row['Program Code']}"), axis=1)
    data_df.info()

    # Need to create the Organization Code column and populate in the State Programs Descriptions dataframe
    state_programs_df[org_code_str] = state_programs_df.apply(
        lambda row: str(f"{row['AgencyCode']}_{row['UnitCode']}_{row['ProgramCode']}"), axis=1)

    # Only need the 'AgencyName', 'UnitName', 'ProgramName' fields joined to data table, drop all others
    state_programs_df.drop(columns=drop_fields, inplace=True)

    # Need to join the state programs data to the data_df on Organization Code using left join
    state_programs_df.set_index(keys=org_code_str, inplace=True, drop=True)
    first_join_df = data_df.join(other=state_programs_df, on=org_code_str)
    print(f"First Join:")
    # print(first_join_df)
    first_join_df.info()

    # Need to rename certain columns, from state program descriptions file, to match schema expected in website
    first_join_df.rename(columns=rename_stateprog_names, inplace=True)
    first_join_df.info()

    print("Outputting CSV...")
    first_join_df.to_csv(path_or_buf=output_result_csv, index=False)
    return


if __name__ == "__main__":
    main()
