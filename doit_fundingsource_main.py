"""
Process the update data for Funding Source and output the processed data to csv.
Replaces FME process for Funding Source data.

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
    agency_categories_drop = ["Agency Name"]
    agency_code_str = "Agency Code"
    budget_column_dtype = {"Budget": "float"}
    column_headers = myvars.funding_common_headers
    data_category = "Funding"
    full_pandas_df_printing = True
    drop_fields = ["AgencyCode", "UnitCode", "ProgramCode", "AgencyName", "UnitName", "ProgramName"]
    org_code_str = "Organization Code"
    output_result_csv = fr"{myvars.python_results_folder}/{today_str}_{data_category}_pythonoutput.csv"
    transformed_data_file = fr"{myvars.transformed_data_folder}/FY{myvars.first}_{myvars.third}_{data_category}_TRANSFORMED.xlsx"

    # ASSERTS
    assert os.path.exists(myvars.agency_categories_file)
    assert os.path.exists(myvars.state_program_descriptions_file)
    assert os.path.exists(transformed_data_file)

    # FUNCTIONALITY
    # _______________
    # KEEP: found this on a blog at https://medium.com/datadriveninvestor/data-cleaning-character-encoding-b4e0e9c65b2a
    # Used this code to discover the encoding of the state programs descriptions b/c it was failing to read as csv or
    # as excel. Ran it, grabbed the encoding, passed it to pd.read_csv and it worked.
    # import chardet
    # with open(state_program_descriptions_file, 'rb') as handler:
    #     result = chardet.detect(handler.read())
    # print(result)
    # exit()
    # _______________

    if full_pandas_df_printing:
        # pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        # pd.set_option('display.max_colwidth', None)

    # Need to control the dtypes to avoid conversion of strings like 'Program Code' to integers (stripping leading zero)
    master_dtypes = {**budget_column_dtype, **{header: str for header in column_headers}}

    # Need the data with appropriate dtypes as df
    data_df = pd.read_excel(io=transformed_data_file, dtype=master_dtypes)
    print(f"Transformed Data: \n{data_df.info()}")

    # Excel versions - Sometimes doesn't work do to encoding issue. Fallback to csv's in that situation.
    state_programs_df = pd.read_excel(io=myvars.state_program_descriptions_file, dtype={"ProgramCode": str})
    print(f"State Program Descriptions: \n{state_programs_df.info()}")

    agency_categories_df = pd.read_excel(io=myvars.agency_categories_file)
    print(f"Agency Categories: \n{agency_categories_df.info()}")

    # CSV versions - This method does not convert '05' into an integer but leaves it as string, without using dtypes
    #   In addition, could provide encoding to bypass issue with bytes
    # state_programs_df = pd.read_csv(filepath_or_buffer=myvars.state_program_descriptions_file, encoding="Windows-1252")
    # agency_categories_df = pd.read_csv(filepath_or_buffer=myvars.agency_categories_file)

    # Need to create the Organization Code column and populate in the data dataframe
    data_df[org_code_str] = data_df.apply(
        lambda row: str(f"{row['Agency Code']}_{row['Unit Code']}_{row['Program Code']}"), axis=1)

    # Need to create the Organization Code column and populate in the State Programs Descriptions dataframe
    state_programs_df[org_code_str] = state_programs_df.apply(
        lambda row: str(f"{row['AgencyCode']}_{row['UnitCode']}_{row['ProgramCode']}"), axis=1)

    # Only need the 'Description' field joined to data table, drop all others
    state_programs_df.drop(columns=drop_fields, inplace=True)

    # Need to join the state programs data to the data_df on Organization Code using left join
    # data_df.set_index(keys="Organization Code", inplace=True, drop=True)
    state_programs_df.set_index(keys=org_code_str, inplace=True, drop=True)

    first_join_df = data_df.join(other=state_programs_df, on=org_code_str)
    print(f"First Join:")
    # print(first_join_df)
    first_join_df.info()

    # Need to join the agency categories data to the first join df on Agency Code using left join
    agency_categories_df.drop(columns=agency_categories_drop, inplace=True)
    agency_categories_df.set_index(keys=agency_code_str, drop=True, inplace=True)
    second_join_df = first_join_df.join(other=agency_categories_df, on="Agency Code")
    print(f"Second Join:")
    # print(second_join_df)
    second_join_df.info()

    print("Outputting CSV...")
    second_join_df.to_csv(path_or_buf=output_result_csv, index=False)
    return


if __name__ == "__main__":
    main()
