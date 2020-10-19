"""
Combine the new FY dataset with the existing production asset for vendor data and output a csv
You have to download the existing production asset first, and have the new FY data in the correct format.

Author: CJuice
Created: 20201019
Revisions:
"""


def main():

    # IMPORTS
    import os
    import pandas as pd
    import numpy as np

    # VARIABLES
    existing_prod_data = r"../20200923_Update/Data/20201019_BACKUP_State_of_Maryland_Payments_Data__FY2008_to_FY2019.csv"
    fy20_data = r"../20200923_Update/Data/HB358 20201005_update20201013_revised.csv"
    output_data = r"../20200923_Update/Data/20201019_combined_forprod.csv"

    # ASSERTS
    assert os.path.exists(existing_prod_data)
    assert os.path.exists(fy20_data)

    # FUNCTIONS

    # CLASSES

    # FUNCTIONALITY
    fy_20_columns = ['fiscal_year', 'category', 'vendor_name', 'vendor_zip', 'agency_name', 'amount']
    fy_20_types = [np.int, np.str, np.str, np.str, np.str, np.float]
    fy_dtype_dict = dict(zip(fy_20_columns, fy_20_types))
    renamed_columns = ['Fiscal Year', 'Category', 'Vendor Name', 'Vendor Zip', 'Agency Name', 'Amount']
    fy_column_names_dict = dict(zip(fy_20_columns, renamed_columns))
    fy_20_df = pd.read_csv(filepath_or_buffer=fy20_data, usecols=fy_20_columns, dtype=fy_dtype_dict)
    fy_20_df.rename(columns=fy_column_names_dict, inplace=True)
    fy_20_df["Fiscal Period"] = 1
    fy_20_df["Date"] = "01/01/2020 12:00:00 AM"
    fy_20_df.info()

    existing_data_df = pd.read_csv(filepath_or_buffer=existing_prod_data)
    existing_data_df.info()

    master_df = pd.concat([fy_20_df, existing_data_df])
    master_df = master_df[['Fiscal Year', 'Agency Name', 'Vendor Name', 'Vendor Zip', 'Amount', 'Fiscal Period', 'Date', 'Category']]
    master_df.info()
    master_df.to_csv(path_or_buf=output_data, index=False)



    return


if __name__ == "__main__":
    main()
