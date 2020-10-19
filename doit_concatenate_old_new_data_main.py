"""
Concatenate the processed update data files with their matching historical data files and output to csv.
Iterate over the pairs of update data and corresponding historical data, concatenate them into a single resource,
and write that resource to csv for upload to open data platform as staging assets.

Author: CJuice
Created: 20200617
Revisions:
"""


def main():

    # IMPORTS
    import datetime
    import os
    import pandas as pd

    # VARIABLES
    _root_project_path = os.path.dirname(__file__)
    today_str = datetime.datetime.today().strftime("%Y%m%d")
    historical_data_folder = r"..\20200601_Update\20200609_FilteredFYProductionData"
    updates_data_folder = r"..\20200601_Update\20200615_PythonResults"
    concatenated_data_folder = r"..\20200601_Update\20200617_ConcatenatedDataProduct"
    full_pandas_df_printing = True

    # TODO: WIth some forethought on naming conventions for outputs a hard coded mapping could be abandoned.
    historical_to_update_files_mapping = {"CUR_CR": ("Maryland_Operating_Budget__CUR_and_CR_FILTERED_FYs.csv", "20200617_CUR-CR_pythonoutput.csv"),
                                       "Funding": ("Maryland_Operating_Budget_-_Funding_Source_FILTERED_FYs.csv", "20200615_Funding_pythonoutput.csv"),
                                       "Budget": ("Maryland_Operating_Budget_FILTERED_FYs.csv", "20200616_Budget_pythonoutput.csv"),
                                       "FTE": ("State_of_Maryland_Full_Time_Equivalents_FILTERED_FYs.csv", "20200617_FTE_pythonoutput.csv")}
    historical_to_update_paths_mapping = {style: (os.path.join(historical_data_folder, values[0]), os.path.join(updates_data_folder, values[1])) for style, values in historical_to_update_files_mapping.items()}
    print(historical_to_update_paths_mapping)

    # ASSERTS
    assert os.path.exists(historical_data_folder)
    assert os.path.exists(updates_data_folder)
    assert os.path.exists(concatenated_data_folder)
    for key, value in historical_to_update_paths_mapping.items():
        historical, update = value
        assert os.path.exists(historical)
        assert os.path.exists(update)

    # FUNCTIONALITY
    if full_pandas_df_printing:
        # pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        # pd.set_option('display.max_colwidth', -1)

    for style, paths_tup in historical_to_update_paths_mapping.items():
        historical, update = paths_tup
        new_concatenated_file = os.path.join(concatenated_data_folder, f"{today_str}_UPDATED_{style}.csv")
        hist_df = pd.read_csv(historical, low_memory=False)
        update_df = pd.read_csv(update, low_memory=False)
        print(f"\n{style}\n\tHistorical\n{hist_df.info()}")
        print(f"\tUpdate\n{update_df.info()}")
        new_df = pd.concat(objs=[hist_df, update_df], ignore_index=True, sort=True, copy=False)
        new_df.info()
        new_df.to_csv(path_or_buf=new_concatenated_file, index=False)

    return


if __name__ == "__main__":
    main()
