This is a Mathematica file used to convert the raw SQL data into clean data like what we show in the CleanedData folder.

What you need:

ImportDataFile: the code assumes this is a .xslx file. This is the
                file taken directly from the SQL server. Very minor
                changes can allow for one to read, e.g., a .csv file.

BatchFile:      this is the batch data from Mechanical Turk. 
                We need this file to determine which survey codes 
                are associated with which Mechanical Turk workers.
                
ExportFile:     This is the output file.
