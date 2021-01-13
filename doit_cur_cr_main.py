"""
Process the update data for CUR/CR and output the processed data to csv.
Replaces FME process for CUR/CR data.

Author: CJuice
Created: 20200616
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
    agency_code_str = "Agency Code"
    budget_column_dtype = {"Budget": "float"}
    column_headers = myvars.cur_cr_common_headers
    data_category = "CUR-CR"
    agency_categories_drop = ["Agency Name"]
    full_pandas_df_printing = True
    org_code_str = "Organization Code"
    output_result_csv = fr"{myvars.processed_data_folder}/{today_str}_{data_category}_PROCESSED.csv"
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
    agency_categories_df = pd.read_excel(io=myvars.agency_categories_file)
    print(f"Agency Categories: \n{agency_categories_df.info()}")

    # CSV versions - This method does not convert '05' into an integer but leaves it as string, without using dtypes
    #   In addition, could provide encoding to bypass issue with bytes
    # agency_categories_df = pd.read_csv(filepath_or_buffer=myvars.agency_categories_file)

    # Need to create the Organization Code column and populate in the data dataframe
    data_df[org_code_str] = data_df.apply(
        lambda row: str(f"{row['Agency Code']}_{row['Unit Code']}_{row['Program Code']}"), axis=1)

    # NOTE: The Description field from the State Programs is a hidden field in the final product on open data portal.
    #   The State Program Descriptions file does not seem to need to be joined at all. To stay consistent with prior
    #   process it will be included in this py version too, but commented out. When update data is to be concatenated
    #   with historical data downloaded from Open Data Portal the Description field is not present in historical.

    # Need to create the Organization Code column and populate in the State Programs Descriptions dataframe
    # state_programs_df["Organization Code"] = state_programs_df.apply(
    #     lambda row: str(f"{row['AgencyCode']}_{row['UnitCode']}_{row['ProgramCode']}"), axis=1)

    # # Only need the 'Description' field joined to data table, drop all others
    # org_code_parts = ["AgencyCode", "AgencyName", "UnitCode", "UnitName", "ProgramCode", "ProgramName", "Description"]
    # state_programs_df.drop(columns=org_code_parts, inplace=True)

    # Need to join the state programs data to the data_df on Organization Code using left join
    # data_df.set_index(keys="Organization Code", inplace=True, drop=True)
    # state_programs_df.set_index(keys="Organization Code", inplace=True, drop=True)

    # first_join_df = data_df.join(other=state_programs_df, on="Organization Code")
    # print(first_join_df)

    # Need to join the agency categories data to the first join df on Agency Code using left join
    agency_categories_df.drop(columns=agency_categories_drop, inplace=True)
    agency_categories_df.set_index(keys=agency_code_str, drop=True, inplace=True)

    # Without the second join, this step could be omitted and replaced by a direct join to data_df
    # second_join_df = first_join_df.join(other=agency_categories_df, on="Agency Code")
    second_join_df = data_df.join(other=agency_categories_df, on=agency_code_str)
    print(f"Second Join:")
    # print(second_join_df)
    second_join_df.info()

    print("Outputting CSV...")
    second_join_df.to_csv(path_or_buf=output_result_csv, index=False)
    return


if __name__ == "__main__":
    main()
