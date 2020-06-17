"""
TODO
Author: CJuice
Created: 20200617
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
    historical_data_folder = r"..\20200601_Update\20200609_FilteredFYProductionData"
    updates_data_folder = r"..\20200601_Update\20200615_PythonResults"
    full_pandas_df_printing = True

    # TODO: WIth some forethought on naming conventions for outputs a hard coded mapping could be abandoned.
    historical_to_update_files_mapping = {"Maryland_Operating_Budget__CUR_and_CR_FILTERED_FYs.csv": "20200616_CUR-CR_pythonoutput.csv",
                                       "Maryland_Operating_Budget_-_Funding_Source_FILTERED_FYs.csv": "20200615_Funding_pythonoutput.csv",
                                       "Maryland_Operating_Budget_FILTERED_FYs.csv": "20200616_Budget_pythonoutput.csv",
                                       "State_of_Maryland_Full_Time_Equivalents_FILTERED_FYs.csv": "20200617_FTE_pythonoutput.csv"}
    historical_to_update_paths_mapping = {os.path.join(historical_data_folder, key): os.path.join(updates_data_folder, value) for key, value in historical_to_update_files_mapping.items()}

    # ASSERTS
    assert os.path.exists(historical_data_folder)
    assert os.path.exists(updates_data_folder)
    for key, value in historical_to_update_paths_mapping.items():
        assert os.path.exists(key)
        assert os.path.exists(value)

    # FUNCTIONS

    # CLASSES

    # FUNCTIONALITY
    if full_pandas_df_printing:
        # pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        # pd.set_option('display.max_colwidth', -1)


    return


if __name__ == "__main__":
    main()
