"""
TODO
Replaces FME process for Funding Source data.

Author: CJuice
Created: 20200612
Revisions:
"""


def main():

    # IMPORTS
    import pandas as pd
    import os

    # VARIABLES
    _root_project_path = os.path.dirname(__file__)
    transformed_data_file = fr"../20200601_Update/20200609_TransformedData/FY2020through2021 - Funding - Data Only_TRANSFORMED.xlsx"
    state_program_descriptions_file = fr"../20200601_Update/20200609_ExtraRequiredFiles/20200127_StateProgramDescriptions.xlsx"
    agency_categories_file = fr"../20200601_Update/20200609_ExtraRequiredFiles/20200127_AgencyCategories_CJuiceCleaned.xlsx"

    # ASSERTS
    assert os.path.exists(transformed_data_file)

    # FUNCTIONS

    # CLASSES

    # FUNCTIONALITY
    data_df = pd.read_excel(io=transformed_data_file)
    state_programs_df = pd.read_excel(io=state_program_descriptions_file)
    agency_categories_df = pd.read_excel(io=agency_categories_file)
    

    return


if __name__ == "__main__":
    main()
