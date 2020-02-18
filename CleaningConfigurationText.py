"""

"""


def main():

    # IMPORTS
    import re
    import pandas as pd

    # VARIABLES

    # CUR/CR data
    # data_file = r"FilesForWebAppRevisions\drill_down_annotations_operating_CURCR20200205Revision.csv"
    # output_data_file = r"FilesForWebAppRevisions\drill_down_annotations_operating_CURCR20200205Revision_PyTweaked.csv"
    # pattern = "<h4><b>Full Time Equivalents: ([0-9.]+)</b></h4>"
    # # replacement = "<h4><b>Full Time Equivalents: </b></h4>" # Before realizing this lacked the FTE hyperlink present in Budget version
    # replacement = """<h4><b><a href="https://fte.maryland.gov/#!/year/2020/operating/0/agency_name?vis=barChart" target="_blank">Full Time Equivalents (FTEs):</a> Click link for data regarding FTE state employee counts for this unit of government.</b></h4>"""
    #
    # example_text = """<h4><b>Full Time Equivalents: 0</b></h4>Section 16-501 of the Local Government Article authorizes
    # disparity grants to address the differences in the capacities of Baltimore City and certain
    # counties to raise revenue from the local income tax. In general, the grants are the lesser of an
    # amount to raise the jurisdiction's per capita income tax revenues to 75% of the state average or the
    # fiscal year 2010 cap. The formula was modified during the 2013 legislative session to add a minimum grant
    #  amount based on the local tax effort of eligible counties and raises from 2.4% to 2.6% the local income tax
    #   rate required to be eligible to receive a grant."""

    # Budget data
    data_file = r"FilesForWebAppRevisions\drill_down_annotations_operating_Budget20200206Revision.csv"
    output_data_file = r"FilesForWebAppRevisions\drill_down_annotations_operating_Budget20200206Revision_PyTweaked.csv"
    pattern = """Full Time Equivalents:</a> ([0-9.]+)</b></h4>"""
    replacement = """Full Time Equivalents (FTEs):</a> Click link for data regarding FTE state employee counts for this unit of government.</b></h4>"""

    # FUNCTIONS
    def remove_fte_count(pattern, string, replacement=None):
        """
        Use the re module to search for the pattern text, substitute replacement text, and return modified html string
        patter: re pattern for matching/searching
        string: the string value to be inspected
        """
        # For testing the pattern
        match_obj = re.search(pattern=pattern, string=string)
        print(match_obj)
        # return

        # Once pattern is proven to work, use sub to replace the desired text
        modified_html_string = re.sub(pattern=pattern, repl=replacement, string=string)
        print(f"\t{modified_html_string}")
        return modified_html_string

    # FUNCTIONALITY
    # create dataframe from configuration file content
    df = pd.read_csv(data_file)
    # print(df.info())

    # use custom function to search for pattern and replace with desired text
    df["text"] = df["text"].apply(lambda x: remove_fte_count(pattern=pattern, string=x, replacement=replacement))

    # output to csv
    df.to_csv(output_data_file, index=False)

    return


if __name__ == "__main__":
    main()