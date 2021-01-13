"""
Filter the existing production data by FY to isolate historical records not involved in the newest update.
Iterate over production asset files, turning each one into a dataframe. Filter based on the Fiscal Year value.
Write the filtered results to csv files that will be used later with the latest update data.
Example: If 2025 data was being added and all years prior to that are not to be touched then this script would filter
for years less than or equal to 2024 and dump that data out to a csv.
Author: CJuice
Created: ~20200101
Revisions:
    20200601, CJuice, revised variables for latest update
    20210113, CJuice, altered output naming convention to be consistent with other processes and to generate a name
    that the concatenation step will recognize. All to eliminate manual editing of variables from year to year.
"""


def main():

    # IMPORTS
    import os
    import pandas as pd
    import doit_centralizedvariables as myvars

    # VARIABLES
    is_output = True
    max_year_of_historical_fy_data = 2019

    # ASSERTS
    assert os.path.exists(myvars.production_data_backups_folder)
    assert os.path.exists(myvars.filtered_data_folder)

    # FUNCTIONS
    def determine_data_type(filename: str) -> str:
        """
        Search the filename for each key and return the value if found to influence the filtered dataset output name
        NOTE: The below type_dict keys are based off of the file name from the production asset downloaded from the
        open data portal. If those names change then this will need to be edited.
        :param filename: str with file name plus "." plus file type
        :return: str
        """
        type_dict = {"Full_Time_Equivalents": myvars.fte_data_type, "CUR_and_CR": myvars.cur_cr_data_type,
                     "Funding_Source": myvars.funding_data_type, "Budget.csv": myvars.budget_data_type}
        for key, value in type_dict.items():
            if key in filename:
                return value
            else:
                continue
        return "ERROR"

    # FUNCTIONALITY
    # try walking through folder and making df of each excel file
    for directory, sub_folders, files in os.walk(myvars.production_data_backups_folder):
        for file in files:
            full_path = os.path.join(directory, file)
            assert os.path.exists(full_path)
            data_type = determine_data_type(filename=file)
            new_file_name = f"{data_type}_FILTERED_FYs.csv"
            full_path_new = os.path.join(myvars.filtered_data_folder, new_file_name)
            df = pd.read_csv(filepath_or_buffer=full_path)
            # print(df.info())

            try:
                print(f"Unique Fiscal Year values in {file} dataframe are \n{df[myvars.fiscal_year_header_str].unique()}")
            except KeyError:
                print(f"KEYERROR: Dataframe for file {file} does not contain {myvars.fiscal_year_header_str} column.")

            # filter data in Fiscal Year column to only years of interest
            filtered_df = df[(df[myvars.fiscal_year_header_str] <= max_year_of_historical_fy_data)]
            # print(df.info())
            print(filtered_df.info())

            print(f"Output to csv: {is_output}")
            if is_output:
                # output df to csv for appending to newest data from DBM
                filtered_df.to_csv(path_or_buf=full_path_new, index=False)

    print("Process Complete")
    return


if __name__ == "__main__":
    main()