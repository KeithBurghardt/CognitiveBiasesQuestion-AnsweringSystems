# CognitiveBiasesQuestion-AnsweringSystems

This is the code and data used for the paper: 
K. Burghardt, T. Hogg, & K. Lerman. "Quantifying the Impact of Cognitive Biases in Question-Answering Systems" ICWSM (2018)

This repository contains 4 folders:

- CleanedData:                  Cleaned experiment data
- Empirical Data Parsing Code:  Code used to compare Stack Exchange data to experiment data
- Experiment Data Parsing Code: Code to convert raw experiment data to cleaned data
- Experiment PHP Code:          Code to create experiment

To run experiment:
- Set up MySQL server and Apache server, following the guidelines of the "Experiment PHP Code" README
- Set up a Human Intelligence Task (HIT) via Amazon Mechanical Turk
- Have workers access server via a URL
- Collect raw data (SQL server data) and batch files (from Amazon Mechanical Turk)
- Process raw data using "Empirical Data Parsing Code" folder
