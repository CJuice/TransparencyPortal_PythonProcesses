# Maryland Transparency Portal
## Yearly Budget Data Updates

### Step 1 - Administrative Setup
* Create a ticket from the request for data processing and website update
    * The request is typically in email format and sent directly to CJuice
    * The ticket system is not engaged by DBM or upper DoIT management so it falls on the data processor to create 
    the ticket
* Create the expected folder structure on your computer where the python processes will be run
    * The expected folders are as follows
        * OfficialData
            * Will contain the source files from the DBM SME
        * OfficialData > ExtraRequiredFiles
            * There are two expected/needed extra files and they are as follows
                * State Program Descriptions
                * Agency Categories
        * TransformedData
            * Will contain transformed source files that are ready for further processing
        * ProductionAssetBackups
            * Storage location for the existing production assets in the Open Data Portal. This is a backup action 
            prior to performing updates to the cloud
        * ProcessedData
            * Will contain processed datasets for upsert to open data platform for SME review
        * FilteredProdData
            * filtered FY data that precedes mashing of historical and current round data ***
        * Notebooks
            * Any jupyter notebooks necessary for processing data
        * Scratch
            * Space for programmatic testing and devlopment, including fixes to assets.
            * The contents of this folder and the Notebooks folder may overlap
        * AnnotationData
            * Files related to annotation values
        
### Step 2 - High Level Data Quality Inspection
* Initial Data Inspection
    * Initial Assessment of Data Files - Jupyter Notebook
        * Use this notebook to gain immediate high level insights into the datasets provided by the DBM SME
        * Look at the field names in each file
        * Look at the data types in each field
        * Look at the number of total records
        * Look at the number of records in each FY column
        * Look for columns with null records, other than the FY since they are split across three columns, and bring
         to the attention of the DBM SME
        * Look to see that the total number of non-null records in the three FY columns sums to the total number of 
        records in the dataframe
        
### Step 3 - Prepare/Transform Original Data for Subsequent Processing
* Transform Source Data
    * Script - doit_transform_original_data_main.py
        * Inspect the variables in the script prior to running. Edit FY year references and check that the expected field
        names from the script match the field names provided in the source data. One cannot count on the DBM SME preserving 
        source data file schema from year to year. Expect to make tweaks!
        * Toggle the boolean controls on the dataset of focus.
        * Process outputs to the TransformedData folder
        
### Step 4 - Process Transformed Datasets
* Script - doit_operatingBudget_main.py
* Script - doit_fundingsource_main.py
* Script - doit_fte_main.py
* Script - doit_cur_cr_main.py

### Step 5 - Upload Processed Datasets to Open Data Portal as Development Assets for DBM SME Review
* Create development level assets of the most recent update data only, for customer review
* Create a data lens for the asset to help the SME
* Minimal metadata needed
* Work with SME if issues are discovered and reprocess and restage data as needed

### Step 6 - Filter Existing Production Data for Historical (not being updated) Data Only
* Script - doit_filter_historical_fiscalyears_data_main.py

### Step 7 - Combine Historical and Updated Data to Create Complete Dataset
* Script - doit_concatenate_old_new_data_main.py

### Step 8 - Upload Combined Datasets to Open Data Portal as Staging Assets for DBM SME Review
* Create staging level assets of the combined historical and update data, for customer review
* Create a data lens for the asset to help the SME
* Minimal metadata needed
* Work with SME if issues are discovered and reprocess and restage data as needed

### Step 9 - Web Page - Backups Sites
* Create four new sites and name them the same as the production sites excepting a "BACKUP" indicator
* Import the configurations from the production web assets into the backup sites 
* These backups are for roll back during failed production push

### Step 10 - Web Page - Staging Sites
* Create four new sites and name them the same as the production sites excepting a "STAGING" indicator
* Import the configurations from the production web assets into the staging sites 
* Switch the staging sites off of the existing production asset 4x4 and onto the staging data asset 4x4
* The staging sites are for redesign/update efforts
* The staging site configurations are imported into the production sites on production deploy of the new/update design

### Step 11 - Final Data Preparations
* If using the staging data assets and discontinuing the existing production data assets
    * Fill out metadata for data assets and get SME review of language
* If using existing production data assets
    * Metadata references to fiscal years will need to be revised during deploy

### Step 12 - Deploy
* Switch staging data assets from private to public OR replace existing production data with new data and revise metadata
* Import the configurations from the approved staging sites into the existing production sites
* Notify DBM SME

### Step 13 - Testing
* After notifying SME of production push, perform testing

## Notes on the Extra Required Files
### State Program Descriptions & Agency Categories
* These two files are raw files from DBM SME. To work in our process they need to be manipulated.
* Agency Categories
    * The Agency Categories file has historically needed editing. 
    * It was necessary to to copy the data and headers (Agency Code, Agency Name, Category, Title->Category Title) 
    and paste "values only" in a new sheet. 
    * It was then necessary to rename "Title" to "Category Title" to match the expected schema. 
    * Then it was necessary to rename the sheet to AgencyCategory. 
    * That product was then saved as CJuiceCleaned and then the original sheet was deleted from the file. 
* State Program Descriptions
    * The State Program Descriptions file had a filter on that needed to be turned off. 
    * The sheet name was already correct to match the original FME process expectation. 
    * Otherwise the data was acceptable so a new version was not saved.
* When a new batch of data is run, two fresh versions of these files should be sent by DBM SME.
        
