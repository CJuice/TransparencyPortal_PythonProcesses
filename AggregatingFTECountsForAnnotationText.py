"""

"""


def main():

    # IMPORTS
    import pandas as pd
    import numpy as np

    # VARIABLES
    data_file = r"FilesForFTEAggregationProcess\FTE_Preview_includedhistorical.csv"  # Downloaded approved data

    # FUNCTIONS

    # FUNCTIONALITY
    df = pd.read_csv(data_file)
    print(df.info())
    df_2020 = df[(df["Fiscal Year"] == 2020)]
    df_pvt = pd.pivot_table(data=df_2020, values="Count", index="Agency Name", aggfunc=np.sum)
    print(df_pvt)
    df_pvt.to_csv(r"FilesForFTEAggregationProcess\2020FTECounts_SummedbyAgencyName.csv")


if __name__ == "__main__":
    main()
