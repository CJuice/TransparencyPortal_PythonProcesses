"""
Centralized variables serving all of the MTP data ETL processes
Author: CJuice
Created: ~20200101
Revisions:
"""

##########
# Will/May change with each update
root_update_folder_path = r"..\20210520_Update"
budget_source_filename = "FY 2021 through FY 2022 Appropriation for Open Data Portal - Expenditure Data.xlsx"
cur_cr_source_filename = "FY 2021 through FY 2022 Appropriation for Open Data Portal - Higher Ed Exp Data.xlsx"
fte_source_filename = "FY 2021 through FY 2022 Legislative Appropriation for Open Data Portal - FTE Data.xlsx"
funds_source_filename = "FY 2021 through FY 2022 Legislative Appropriation for Open Data - Funds Data.xlsx"
# budget_source_filename = "FY 2021 - FY 2022 Gov Allowance for Open Data - Expenditure Data 1-22-21.xlsx"
# funds_source_filename = "FY 2021 - FY 2022 Gov Allowance for Open Data - Funds Data Only 1-22-21.xlsx"
first, second, third = (2020, 2021, 2022)

#   Dependent
combined_data_folder = f"{root_update_folder_path}/CombinedData"
filtered_data_folder = f"{root_update_folder_path}/FilteredData"
official_data_folder = f"{root_update_folder_path}/OfficialData"
processed_data_folder = f"{root_update_folder_path}/ProcessedData"
production_data_backups_folder = f"{root_update_folder_path}/ProductionAssetBackups"
transformed_data_folder = f"{root_update_folder_path}/TransformedData"
extra_required_files = f"{official_data_folder}/ExtraRequiredFiles"
first_header = f"FY {first} Budget Book Actuals"
second_header = f"FY {second} Budget Book Working"
third_header = f"FY {third} Governors Allowance"
fiscal_years_dict = {f"FY {first}": first_header, f"FY {second}": second_header, f"FY {third}": third_header}

# Excel versions have presented encoding issues in past. Fall back is to use csv versions
agency_categories_file = fr"{extra_required_files}/AgencyCategories_CJuiceCleaned.xlsx"
state_program_descriptions_file = fr"{extra_required_files}/StateProgramDescriptions.xlsx"

# CSV versions
# agency_categories_file = fr"{extra_required_files}/AgencyCategories_CJuiceCleaned.csv"
# state_program_descriptions_file = fr"{extra_required_files}/StateProgramDescriptions.csv"
##########

budget_data_type = "Budget"
cur_cr_data_type = "CUR-CR"
fte_data_type = "FTE"
funding_data_type = "Funding"
fiscal_year_header_str = "Fiscal Year"
budget_common_headers = ["Fiscal Year", "Agency Code", "Agency Name", "Unit Code", "Unit Name", "Program Code",
                         "Program Name", "Subprogram Code", "Subprogram Name", "Object Code", "Object Name",
                         "Comptroller Subobject Code", "Comptroller Subobject Name", "Agency Subobject Code",
                         "Agency Subobject Name", "Fund Type Name"]
cur_cr_common_headers = ["Fiscal Year", "Agency Code", "Agency Name", "Unit Code", "Unit Name", "Program Code",
                         "Program Name", "Subprogram Code", "Subprogram Name", "Object Code", "Object Name",
                         "Comptroller Subobject Code", "Comptroller Subobject Name", "Agency Subobject Code",
                         "Agency Subobject Name", "Fund Type Name"]
fte_common_headers = ["Agency Code", "Unit Code", "Program Code"]
funding_common_headers = ['Fiscal Year', 'Agency Code', 'Agency Name', 'Unit Code', 'Unit Name',
                          'Program Code', 'Program Name', 'Fund Type Name', 'Fund Source Code',
                          'Fund Source Name']
data_type_header_map_dict = {budget_data_type: budget_common_headers, cur_cr_data_type: cur_cr_common_headers,
                             fte_data_type: fte_common_headers, funding_data_type: funding_common_headers}
