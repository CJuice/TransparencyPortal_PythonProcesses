"""
Filter the existing production data by FY to isolate historical records not involved in the newest update.
Iterate over production asset files, turning each one into a dataframe. Filter based on the Fiscal Year value.
Write the filtered results to csv files that will be used later with the latest update data.
Example: If 2025 data was being added and all years prior to that are not to be touched then this script would filter
for years less than or equal to 2024 and dump that data out to a csv.
Author: CJuice
Created: ~20200101
Revisions: 20200601, CJuice, revised variables for latest update
"""


def main():

    # IMPORTS
    import os
    import pandas as pd
    import doit_centralizedvariables as myvars

    # VARIABLES
    is_output = False
    max_year_of_historical_fy_data = 2019

    # ASSERTS
    assert os.path.exists(myvars.production_data_backups_folder)
    assert os.path.exists(myvars.filtered_data_folder)

    # FUNCTIONS

    # FUNCTIONALITY
    # try walking through folder and making df of each excel file
    for directory, sub_folders, files in os.walk(myvars.production_data_backups_folder):
        for file in files:
            full_path = os.path.join(directory, file)
            assert os.path.exists(full_path)
            file_name, extension = file.split(".")
            new_file_name = f"{file_name}_FILTERED_FYs.csv"
            full_path_new = os.path.join(myvars.filtered_data_folder, new_file_name)

            # print(file_name, directory, sub_folders)
            # print(new_file_name)
            df = pd.read_csv(filepath_or_buffer=full_path)
            # print(df.info())

            try:
                print(f"Unique Fiscal Year values in {file} dataframe are \n{df[myvars.fiscal_year_header_str].unique()}")
            except KeyError:
                print(f"KEYERROR: Dataframe for file {file} does not contain {myvars.fiscal_year_header_str} column.")

            # filter data in Fiscal Year column to only years of interest
            filtered_df = df[(df[myvars.fiscal_year_header_str] <= max_year_of_historical_fy_data)]
            # print(df.info())
            # print(filtered_df.info())
            print(f"Output to csv: {is_output}")
            if is_output:
                # output df to csv for appending to newest data from DBM
                filtered_df.to_csv(path_or_buf=full_path_new, index=False)

    print("Process Complete")
    return


if __name__ == "__main__":
    main()