"""
Filter the existing production data by FY to isolate historical records not involved in the newest update.
Iterate over production asset files, turning each one into a dataframe. Filter based on the Fiscal Year value.
Write the filtered results to csv files that will be used later with the latest update data.
Example: If 2025 data was being added and all years prior to that are not to be touched then this script would filter
for years less than 2025 and dump that data out to a csv.
Author: CJuice
Created: ~20200101
Revisions: 20200601, CJuice, revised variables for latest update
"""


def main():

    # IMPORTS
    import os
    import pandas as pd

    # VARIABLES
    _root_proj_path = os.path.dirname(__file__)
    fiscal_year = "Fiscal Year"
    max_year_of_historical_fy_data = 2019
    output_filtered_data_folder = r"..\20200601_Update\20200609_FilteredFYProductionData"
    prod_downloaded_data_folder = r"..\20200601_Update\20200609_ProductionSocrataVersion_Downloads"

    # ASSERTS
    assert os.path.exists(prod_downloaded_data_folder)
    assert os.path.exists(output_filtered_data_folder)

    # FUNCTIONS

    # FUNCTIONALITY
    # try walking through folder and making df of each excel file
    for directory, sub_folders, files in os.walk(prod_downloaded_data_folder):
        for file in files:
            full_path = os.path.join(directory, file)
            assert os.path.exists(full_path)
            file_name, extension = file.split(".")
            new_file_name = f"{file_name}_FILTERED_FYs.csv"
            full_path_new = os.path.join(output_filtered_data_folder, new_file_name)

            # print(file_name, directory, sub_folders)
            # print(new_file_name)
            df = pd.read_csv(filepath_or_buffer=full_path)
            # print(df.info())

            try:
                print(f"Unique Fiscal Year values in {file} dataframe are \n{df[fiscal_year].unique()}")
            except KeyError:
                print(f"KEYERROR: Dataframe for file {file} does not contain {fiscal_year} column.")

            # filter data in Fiscal Year column to only years of interest
            filtered_df = df[(df[fiscal_year] <= max_year_of_historical_fy_data)]
            # print(df.info())
            # print(filtered_df.info())

            # output df to csv for appending to newest data from DBM
            filtered_df.to_csv(path_or_buf=full_path_new, index=False)

    print("Process Complete")
    return


if __name__ == "__main__":
    main()