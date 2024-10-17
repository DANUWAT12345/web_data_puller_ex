# Call the data_check function to obtain valid_folders and invalid_folders
from data_check import data_check
valid_folders, invalid_folders_no_WO, invalid_folders_AB, invalid_folders_errorsearch, invalid_folders_Unknow, invalid_folders_storage = data_check()

#Call the combine_html function to process valid_folders
from combinator import combine_html
combine_html(valid_folders)

#Call the data_extract function to process data extraction
from data_extract import data_extract
data_extract(valid_folders,invalid_folders_storage)

#Call the CSV writer
from csv_summary import csv_summary
csv_summary()