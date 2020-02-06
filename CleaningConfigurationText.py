"""

"""


def main():

    # IMPORTS
    import re
    import pandas as pd

    # VARIABLES
    data_file = r"FilesForWebAppRevisions\drill_down_annotations_operating_CURCR20200205Revision.csv"
    output_data_file = r"FilesForWebAppRevisions\drill_down_annotations_operating_CURCR20200205Revision_PyTweaked.csv"
    example_text = """<h4><b>Full Time Equivalents: 0</b></h4>Section 16-501 of the Local Government Article authorizes 
    disparity grants to address the differences in the capacities of Baltimore City and certain 
    counties to raise revenue from the local income tax. In general, the grants are the lesser of an 
    amount to raise the jurisdiction's per capita income tax revenues to 75% of the state average or the 
    fiscal year 2010 cap. The formula was modified during the 2013 legislative session to add a minimum grant
     amount based on the local tax effort of eligible counties and raises from 2.4% to 2.6% the local income tax
      rate required to be eligible to receive a grant."""

    # FUNCTIONS
    def remove_fte_count(string):
        """
        Use the re module to search for the pattern text, substitute replacement text, and return modified html string
        string: the string value to be inspected
        """
        pattern = "<h4><b>Full Time Equivalents: ([0-9.]+)</b>"
        replacement = "<h4><b>Full Time Equivalents: </b>"

        # For testing the pattern
        # match_obj = re.match(pattern=pattern, string=html_string)
        # print(match_obj)

        # Once pattern is proven to work, use sub to replace the desired text
        modified_html_string = re.sub(pattern=pattern, repl=replacement, string=string)
        # print(f"\t{modified_html_string}")
        return modified_html_string

    # FUNCTIONALITY
    # create dataframe from configuration file content
    df = pd.read_csv(data_file)

    # use custom function to search for pattern and replace with desired text
    df["text"] = df["text"].apply(lambda x: remove_fte_count(string=x))

    # output to csv
    df.to_csv(output_data_file, index=False)

    return


if __name__ == "__main__":
    main()