# Maryland Transparency Portal
## Yearly Budget Data Updates

### Step 1
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
        * PythonResults
            * I believe these are polished outputs for upsert to cloud but not sure ***
        * FYFilteredProdData
            * filtered FY data that precedes mashing of historical and current round data ***
* doit_transform_original_data_main.py
    * Inspect the variables in the script prior to running. Edit FY year references and check that the expected field
    names from the script match the field names provided in the source data. One cannot count on the DBM SME preserving 
    source data file schema from year to year. Expect to make tweaks!
    * Toggle the boolean controls on the dataset of focus.
    * Process outputs to the TransformedData folder
* ? 
        
