"""
Concatenate the processed update data files with their matching historical filtered data files and output to csv.
Iterate over the pairs of update data and corresponding historical filtered data, concatenate them into a
single resource, and write that resource to csv for upload to open data platform as staging assets. The process
is sensitive to a partial update. Process expects four files so a partial update requires temporary manipulation of
the variables.

Author: CJuice
Created: 20200617
Revisions:
    20210112, CJuice, Refactored variables to allow easier editing each year. Also redesigned to work with output
        of previous step to enable step to step running without reconfiguring variables.
    20210201, CJuice, Filter out budget values equal to zero before writing csv.
"""


def main():

    # IMPORTS
    import datetime
    import os
    import pandas as pd
    import doit_centralizedvariables as myvars

    # VARIABLES
    today_str = datetime.datetime.today().strftime("%Y%m%d")
    processed_files_list = None
    filtered_files_list = None

    for directory, sub_folders, files in os.walk(myvars.processed_data_folder):
        processed_files_list = files
    for directory, sub_folders, files in os.walk(myvars.filtered_data_folder):
        filtered_files_list = files

    # TODO: Refactor below to function when have time to consider
    cur_cr_filtered, funding_filtered, budget_filtered, fte_filtered = None, None, None, None
    cur_cr_processed, funding_processed, budget_processed, fte_processed = None, None, None, None
    for name in processed_files_list:
        if myvars.cur_cr_data_type in name:
            cur_cr_processed = name
        elif myvars.funding_data_type in name:
            funding_processed = name
        elif myvars.fte_data_type in name:
            fte_processed = name
        elif myvars.budget_data_type in name:
            budget_processed = name
        else:
            print("Issue while assigning files to variables")
            exit()
    for name in filtered_files_list:
        if myvars.cur_cr_data_type in name:
            cur_cr_filtered = name
        elif myvars.funding_data_type in name:
            funding_filtered = name
        elif myvars.fte_data_type in name:
            fte_filtered = name
        elif myvars.budget_data_type in name:
            budget_filtered = name
        else:
            print("Issue while assigning files to variables")
            exit()

    # This var is intentionally formatted to multi-line to enable commenting out files if update doesn't include all
    historical_to_update_files_mapping = {
        myvars.cur_cr_data_type: (cur_cr_filtered, cur_cr_processed),
        myvars.funding_data_type: (funding_filtered, funding_processed),
        myvars.budget_data_type: (budget_filtered, budget_processed),
        myvars.fte_data_type: (fte_filtered, fte_processed)
    }

    historical_to_update_paths_mapping = {style: (os.path.join(myvars.filtered_data_folder, values[0]), os.path.join(myvars.processed_data_folder, values[1])) for style, values in historical_to_update_files_mapping.items()}
    print(historical_to_update_paths_mapping)
    assert os.path.exists(myvars.filtered_data_folder)
    assert os.path.exists(myvars.processed_data_folder)
    assert os.path.exists(myvars.combined_data_folder)
    for key, value in historical_to_update_paths_mapping.items():
        filtered, processed = value
        assert os.path.exists(filtered)
        assert os.path.exists(processed)

    # FUNCTIONALITY
    for style, paths_tup in historical_to_update_paths_mapping.items():
        filtered, processed = paths_tup
        new_concatenated_file = os.path.join(myvars.combined_data_folder, f"{today_str}_{style}_COMBINED.csv")
        common_column_dtypes_dict = {header: str for header in myvars.data_type_header_map_dict.get(style)}
        common_column_dtypes_dict[myvars.fiscal_year_header_str] = int
        filtered_df = pd.read_csv(filtered, dtype=common_column_dtypes_dict, low_memory=False)
        processed_df = pd.read_csv(processed, dtype=common_column_dtypes_dict, low_memory=False)
        print(f"\n{style}\n\tFiltered")
        print(filtered_df.info())
        print(f"\n{style}\n\tProcessed")
        print(processed_df.info())

        new_df = pd.concat(objs=[filtered_df, processed_df], ignore_index=True, sort=True, copy=False)
        print(f"\n{style}\n\tCombined")
        print(new_df.info())

        print("Removing Budget values equal to 0.")
        no_zero_df = new_df[(new_df["Budget"] < 0) | (0 < new_df["Budget"])]
        print(no_zero_df.info())

        no_zero_df.to_csv(path_or_buf=new_concatenated_file, index=False)

    return


if __name__ == "__main__":
    main()
