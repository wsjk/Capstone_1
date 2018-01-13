import pandas as pd
import numpy as np
import glob
import os
import csv
import re


def import_clean_csv():
	current_file_path = os.path.abspath(os.path.join("__file__" ,"../.."))
	raw_data_path = os.path.join(current_file_path,'data','raw')
	proc_data_path = os.path.join(current_file_path,'data','processed')
	data_files = glob.glob(os.path.join(proc_data_path, '*.csv'), recursive=False)

	import re
	import ntpath
	pattern = r'(.+)_cleaned.csv$'  #extract filenames of cleaned files for dict keys

	#dict to contain all dataframes
	data = {}
	for file in data_files:
	    matchobj = re.search(pattern, ntpath.basename(file))
	    data[matchobj.group(1)] = pd.read_csv(file, index_col = ['movie_id', 'title'], parse_dates=True)    

	data['tmdb_movie_main'].release_date = pd.to_datetime(data['tmdb_movie_main'].release_date, infer_datetime_format=True)
	
	return data

if __name__ == "__main__":
	data = import_clean_csv()
