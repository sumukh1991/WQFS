#!/usr/bin/env python
'''
Authors:
Craig West
Sheifali Khare
Sumukh Hallymysore Ravindra

Validating the uploaded files and sanity of its contents
(C) Purdue University 2015
'''
from datetime import datetime, timedelta
import os
import io
import sys
import json
import csv
import itertools

outputOverall = {
	'isValid':'false'
	}

previous_file_date = ''

# List to hold all the uploaded files
all_files = []

#Dictionary to store rows which have been deleted corresponding to the Hut
rows_modified_dict = dict()
rows_delete_dict = dict()
# Dictionary for hut columns variable
def create_column_hut_dict():
	hcol_dict = dict()
	hcol_dict['A'] = 64
	hcol_dict['B'] = 65
	hcol_dict['C'] = 65
	hcol_dict['D'] = 65
	hcol_dict['E'] = 65
	hcol_dict['F'] = 65
	hcol_dict['G'] = 63
	hcol_dict['H'] = 65
	hcol_dict['I'] = 23
	hcol_dict['J'] = 22
	hcol_dict['K'] = 22
	hcol_dict['L'] = 23
	return hcol_dict

# Dictionary for hut columns variable
def create_tile_hut_dict():
	htile_dict = dict()
	htile_dict['A'] = 6
	htile_dict['B'] = 6
	htile_dict['C'] = 6
	htile_dict['D'] = 6
	htile_dict['E'] = 6
	htile_dict['F'] = 6
	htile_dict['G'] = 6
	htile_dict['H'] = 6
	htile_dict['I'] = 2
	htile_dict['J'] = 1
	htile_dict['K'] = 1
	htile_dict['L'] = 2
	return htile_dict

# Dictionary for hut columns variable
def create_vwc_temp_count_dict():
	h_count = dict()
	h_count['A'] = 24
	h_count['B'] = 24
	h_count['C'] = 24
	h_count['D'] = 24
	h_count['E'] = 24
	h_count['F'] = 24
	h_count['G'] = 24
	h_count['H'] = 24
	h_count['I'] = 4
	h_count['J'] = 4
	h_count['K'] = 4
	h_count['L'] = 4
	return h_count


# Dictionary for tile names in a hut
def create_tile_name_dict():
	htile_names = dict()
	htile_names['A'] = ['TB1','TB2','TB3','TB4','TB5','TB6']
	htile_names['B'] = ['TB1','TB2','TB3','TB4','TB5','TB6']
	htile_names['C'] = ['TB1','TB2','TB3','TB4','TB5','TB6']
	htile_names['D'] = ['TB1','TB2','TB3','TB4','TB5','TB6']
	htile_names['E'] = ['TB1','TB2','TB3','TB4','TB5','TB6']
	htile_names['F'] = ['TB1','TB2','TB3','TB4','TB5','TB6']
	htile_names['G'] = ['TB1','TB2','TB3','TB4','TB5','TB6']
	htile_names['H'] = ['TB1','TB2','TB3','TB4','TB5','TB6']
	htile_names['I'] = ['TB1','TB2']
	htile_names['J'] = ['TB1']
	htile_names['K'] = ['TB1']
	htile_names['L'] = ['TB1','TB2']
	return htile_names


# Dictionary for VWC or Temp column Names in a Hut
def create_vwctemp_col_dict():
	hcol_names = dict()
	hcol_names['A'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1','P2A.S1','P2A.S1','P2B.S1','P2B.S1','P3A.S1','P3A.S1','P3B.S1','P3B.S1','P4A.S1','P4A.S1','P4B.S1','P4B.S1','P5A.S1','P5A.S1','P5B.S1','P5B.S1','P6A.S1','P6A.S1','P6B.S1','P6B.S1']
	hcol_names['B'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1','P2A.S1','P2A.S1','P2B.S1','P2B.S1','P3A.S1','P3A.S1','P3B.S1','P3B.S1','P4A.S1','P4A.S1','P4B.S1','P4B.S1','P5A.S1','P5A.S1','P5B.S1','P5B.S1','P6A.S1','P6A.S1','P6B.S1','P6B.S1']
	hcol_names['C'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1','P2A.S1','P2A.S1','P2B.S1','P2B.S1','P3A.S1','P3A.S1','P3B.S1','P3B.S1','P4A.S1','P4A.S1','P4B.S1','P4B.S1','P5A.S1','P5A.S1','P5B.S1','P5B.S1','P6A.S1','P6A.S1','P6B.S1','P6B.S1']
	hcol_names['D'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1','P2A.S1','P2A.S1','P2B.S1','P2B.S1','P3A.S1','P3A.S1','P3B.S1','P3B.S1','P4A.S1','P4A.S1','P4B.S1','P4B.S1','P5A.S1','P5A.S1','P5B.S1','P5B.S1','P6A.S1','P6A.S1','P6B.S1','P6B.S1']
	hcol_names['E'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1','P2A.S1','P2A.S1','P2B.S1','P2B.S1','P3A.S1','P3A.S1','P3B.S1','P3B.S1','P4A.S1','P4A.S1','P4B.S1','P4B.S1','P5A.S1','P5A.S1','P5B.S1','P5B.S1','P6A.S1','P6A.S1','P6B.S1','P6B.S1']
	hcol_names['F'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1','P2A.S1','P2A.S1','P2B.S1','P2B.S1','P3A.S1','P3A.S1','P3B.S1','P3B.S1','P4A.S1','P4A.S1','P4B.S1','P4B.S1','P5A.S1','P5A.S1','P5B.S1','P5B.S1','P6A.S1','P6A.S1','P6B.S1','P6B.S1']
	hcol_names['G'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1','P2A.S1','P2A.S1','P2B.S1','P2B.S1','P3A.S1','P3A.S1','P3B.S1','P3B.S1','P4A.S1','P4A.S1','P4B.S1','P4B.S1','P5A.S1','P5A.S1','P5B.S1','P5B.S1','P6A.S1','P6A.S1','P6B.S1','P6B.S1']
	hcol_names['H'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1','P2A.S1','P2A.S1','P2B.S1','P2B.S1','P3A.S1','P3A.S1','P3B.S1','P3B.S1','P4A.S1','P4A.S1','P4B.S1','P4B.S1','P5A.S1','P5A.S1','P5B.S1','P5B.S1','P6A.S1','P6A.S1','P6B.S1','P6B.S1']
	hcol_names['I'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1']
	hcol_names['J'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1']
	hcol_names['K'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1']
	hcol_names['L'] = ['P1A.S1','P1A.S1','P1B.S1','P1B.S1']
	return hcol_names 

def findMissingColumns(rowheader,col_names,header_type):
	expected_column = col_names
	found_column = []	
	for i in col_names:
		for headerCell in rowheader:
			if(header_type != 'tile'):
				txt = i + '.' + header_type
			else:
				txt = i
			if( headerCell.find(txt) != -1):
				found_column.append(i)	
	col_missing = list(set(expected_column)-set(found_column))
	return col_missing
	
# Read how many lines are in a file
def num_lines(filename):
	return sum(1 for line in open(filename)) - 1

#Check the file has all the columns
def check_file_columns(f,hcol_count,htile_count,hvwctemp_count):
	status = False
	hutName = os.path.basename(f).split('-')[1][0]
	errorMsg = []
	htile_names = create_tile_name_dict()
	h_vwc_temp_cols = create_vwctemp_col_dict()
	with io.open(os.path.basename(f), 'r', encoding='utf-16-le') as fr:
		reader1 = csv.reader(fr)
		rowheader = next(reader1)
		columns = len(rowheader)
		if(hcol_count[hutName] == columns):
			status = True
		else:
			tmp1_tilenum = []
			utc_count = 0
			tile_count = 0
			temp_sensor_count = 0
			vwc_sensor_count = 0
			t1_count = 0
			sol_count = 0
			batt_count = 0
			lowv_count = 0
			scripterror_count = 0
			internalerror_count = 0
			radioerror_count = 0
			sensorerror_count = 0
			lowbatterror_count = 0
			flooderror_count = 0
			serialError_count = 0
			for headerCell in rowheader:
				if( headerCell.find('- TB') != -1):					
					tile_count = tile_count + 1
				elif headerCell.find('UTC_minus') != -1:
					utc_count = utc_count + 1
				elif headerCell.find('VWC') != -1:
					vwc_sensor_count = vwc_sensor_count + 1
				elif headerCell.find('temp') != -1:
					temp_sensor_count = temp_sensor_count + 1
				elif headerCell.find('T1') != -1:
					t1_count = t1_count + 1
				elif headerCell.find('SOL') != -1:
					sol_count = sol_count + 1	
				elif headerCell.find('BATT') != -1:
					batt_count = batt_count + 1
				elif headerCell.find('LOWV') != -1:
					lowv_count = lowv_count + 1					
				elif headerCell.find('ScriptError') != -1:
					scripterror_count = scripterror_count + 1				
				elif headerCell.find('InternalError') != -1:
					internalerror_count = internalerror_count + 1				
				elif headerCell.find('RadioError') != -1:
					radioerror_count = radioerror_count + 1
				elif headerCell.find('SensorError') != -1:
					sensorerror_count = sensorerror_count + 1
				elif headerCell.find('LowBattError') != -1:
					lowbatterror_count = lowbatterror_count + 1				
				elif headerCell.find('FloodError') != -1:
					flooderror_count = flooderror_count + 1
				elif headerCell.find('SerialError') != -1:
					serialError_count = serialError_count + 1
			#Check if the count of each column matches			
			if(htile_count[hutName] != tile_count):					
				status = False
				tiles_missing = findMissingColumns(rowheader,htile_names[hutName],'tile')
				errString = 'Following tile column/s is missing for Hut ' + hutName +': ' + str(tiles_missing)
				errorMsg.append(errString)	

			if(utc_count != 1):			
				status = False
				errString = 'UTCMinus column is missing for Hut ' + hutName
				errorMsg.append(errString)

			if(hvwctemp_count[hutName] != vwc_sensor_count):					
				status = False
				tiles_missing = findMissingColumns(rowheader,h_vwc_temp_cols[hutName],'VWC')
				errString = 'Following VWC column/s is missing for Hut ' + hutName +': ' + str(tiles_missing)
				errorMsg.append(errString)
				
			if(hvwctemp_count[hutName] != temp_sensor_count):					
				status = False
				tiles_missing = findMissingColumns(rowheader,h_vwc_temp_cols[hutName],'temp')
				errString = 'Following temp column/s is missing for Hut ' + hutName +': ' + str(tiles_missing)
				errorMsg.append(errString)
			
			if(t1_count != 1):					
				status = False
				errString = 'T1 column is missing for Hut ' + hutName
				errorMsg.append(errString)
			
			if(sol_count != 1):					
				status = False
				errString = 'SOL column is missing for Hut ' + hutName
				errorMsg.append(errString)
			
			if(batt_count != 1):					
				status = False
				errString = 'BATT column is missing for Hut ' + hutName
				errorMsg.append(errString)
				
			if(scripterror_count != 1):					
				status = False
				errString = 'ScriptError column is missing for Hut ' + hutName
				errorMsg.append(errString)

			# Hut G has missing internalError
			if(internalerror_count != 1 and hutName != "G"):					
				status = False
				errString = 'InternalError column is missing for Hut ' + hutName
				errorMsg.append(errString)
				
			if(radioerror_count != 1):					
				status = False
				errString = 'RadioError column is missing for Hut ' + hutName
				errorMsg.append(errString)
				
			if(sensorerror_count != 1):					
				status = False
				errString = 'SensorError column is missing for Hut ' + hutName
				errorMsg.append(errString)

			# Hut A,B,C,D,E,F,G,H are missing serialError
			if(serialError_count != 1 and hutName in ('I','J','K','L')):					
				status = False
				errString = 'SerialError column is missing for Hut ' + hutName
				errorMsg.append(errString)
				
			if(lowbatterror_count != 1):					
				status = False
				errString = 'lowbatterror_count column is missing for Hut ' + hutName
				errorMsg.append(errString)

			#Hut A and G has missing floodError
			if(flooderror_count != 1 and (hutName != "G" and hutName != "A") ):
				status = False
				errString = 'FloodError column is missing for Hut ' + hutName
				errorMsg.append(errString)
		return status, errorMsg

# Converts the date into julian date with 24hr time
def convert_to_julian(date):
	dt = datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')	
	return dt
	
# Identify the extra rows in the excel sheet 
def identify_rows_to_delete(f):
	loop_flag = True
	try_line = 1
	global previous_file_date
	while loop_flag:
		rows_delete = []
		#If rows are greater than 25, then we identify the rows to be deleted
		with io.open(f, 'r', encoding='utf-16-le') as fr:
			erroneous_lines_count = 0
			# iterate over each row
			for rowNum, row in enumerate(fr):
				if rowNum == 0:
					# Parse the header of the file into a list
					header = [col for col in row.replace('\n','').split(',')]
				else:
					current_file_date = row.split(',')[0].split(' ')[0]
					for colNum, col in enumerate(row.replace('\n','').split(',')):
						# For second row, determine the previous time and for rest of the rows determine current
						if header[colNum].find('UTC_minus') != -1 and rowNum == try_line:
							p_time = convert_to_julian(col)
						elif header[colNum].find('UTC_minus') != -1 and rowNum < try_line:
							rows_delete.append(rowNum)
							erroneous_lines_count = erroneous_lines_count + 1
						elif header[colNum].find('UTC_minus') != -1:
							# set the current time
							c_time = convert_to_julian(col)
							# determine difference in time
							total_diff = c_time - p_time						
							if total_diff < timedelta(minutes=57) or total_diff > timedelta(minutes=63):
								rows_delete.append(rowNum)
								erroneous_lines_count = erroneous_lines_count + 1
							else:
								p_time = c_time
			# Check if all the files belong to the same date, else abort
			# Set the previous file date value the first time, do comparisons later on
			if previous_file_date == '':
				previous_file_date = current_file_date
			elif previous_file_date != current_file_date:
				raise Exception("Error: File/s do not belong to same date.")
		# print os.path.basename(f) + str(erroneous_lines_count)
		# print num_lines(f)
		if num_lines(f) == (erroneous_lines_count + 25):
			loop_flag = False
		elif num_lines(f) == try_line:
			loop_flag = False
			raise Exception('Error. Check the hourly entries of file: {0}'.format(os.path.basename(f)))
		else:
			try_line = try_line + 1
	# print rows_delete
	return rows_delete

#Delete the extra rows from the file
def delete_rows(f, rows_no_delete):
	rows_retained = set()
	#Save the details of the removed erroneous entries
	rows_error = {}
	#Get Hut Name
	hutName = (str(f).split("_")[0].split("-"))[1]
	# Read the lines into a variable - lines
	with io.open(f, 'r', encoding='utf-16-le') as fr:			
		lines = fr.readlines()			
	# Open the file again and write all the lines except the ones not required
	with io.open(f, 'r', encoding='utf-16-le') as fr:
		#Original File Row Number
		rowNum = 0
		#New File Row Number
		newRowNum = 0
		# iterate over each row
		for line in lines:
  			if rowNum not in rows_no_delete:
				newRowNum = newRowNum + 1
				#fr.write(line)
			else:
				rows_retained.add(newRowNum)
				if newRowNum >= 24:
					errRowNum = 24
				else:
					errRowNum = newRowNum
				rows_error[rowNum] = '<<'+str(errRowNum) +'>>'+line.split(',')[0]
			rowNum = rowNum + 1
		if newRowNum != 25:
			raise Exception("Error: Following file doesn't contain entries for each hour interval: {0}".format(os.path.basename(f)))
	
	if len(rows_no_delete):
		#populate rows dictionary
		rows_modified_dict[hutName] =  ",".join(str(value) for key, value in rows_error.iteritems())
		#populate rows dictionary
		rows_delete_dict[hutName] =  ",".join(str(x) for x in rows_no_delete)

def fix_data_file(f):
	problem_rows = []
	p_hour = 0
	p_min = 0
	p_sec = 0
	#Array to hold rows deleted
	rows_no_delete = []
	# Idenify rows to be deleted
	rows_no_delete = identify_rows_to_delete(f)
	# Delete extra rows
	delete_rows(f, rows_no_delete)	

# Verify if the dates are contiguous
def verify_file_dates(file_date_list):
	# Convert the string date values to date type
	file_dates = [datetime.strptime(d, "%Y-%m-%d") for d in file_date_list]
	file_date_ints = set([d.toordinal() for d in file_dates])
	if max(file_date_ints) - min(file_date_ints) != (len(file_date_ints) - 1):
		raise Exception("Error. Missing Files for few dates in between. Should be contiguous to upload.")
	    
'''Our main function of the file.
This function searches the directory
for files and passes each file to the
funtion to be parsed.
'''
def parse_files_for_date(file_list, file_date):
	'''
	We have to use global to modify the value
	of the variable outside the function because
	the variable is global
	'''
	# print file_list
	# Output for a set of input files related to a specific date
	output = {'isValid':'false'}
	# Initializing variables
	num_files = 0
	err_file_list = []
	global previous_file_date
	global rows_modified_dict
	global rows_delete_dict
	previous_file_date = ''
	file_dates = []
	huts_list = set()
	hcol_dict = create_column_hut_dict()
	htile_dict = create_tile_hut_dict()
	hvwctemp_count = create_vwc_temp_count_dict()
	# Iterate the current directory looking
	# for the CSV files
	for fname in file_list:
		f = open(fname,'r')
		# # Get the date-time fields from the file name to compare with other file names 
		# file_dates = f.split('.')[0].split('_')[3].split('-')
		# file_date = file_dates[0] +'-'+ file_dates[1] +'-'+ file_dates[2]
		# # Verify if they belong to same date, abort if not
		# if ( previous_file_date != '') and ( file_date != previous_file_date ):
		# 	raise Exception("Error: Files do not belong to same date.")
		# else:
		# 	previous_file_date = file_date
		f.read()
		if num_lines(fname) >= 25:
			fix_data_file(fname)
		elif num_lines(fname) < 25:
			err_file_list.append(fname)
			raise Exception("Error: Following files contains less than 24 entries: {0}".format(','.join(err_file_list)))
		status,errMsg = check_file_columns(fname,hcol_dict,htile_dict,hvwctemp_count)
		if status == False:
			err_msg = str(errMsg)+ " in file: "+f.name
			raise Exception(err_msg)
		huts_list.add(fname.split('.')[0].split('_')[0]) 
		num_files += 1
	if num_files == 0:
		raise Exception('Error: There are no CSV files to upload.')
	elif num_files != 12:
		raise Exception('Error: Expecting 12 files to be uploaded. Found '+str(num_files)+' for date '+previous_file_date)
	else:
		num_files = 0
		for hut in huts_list:
			num_files += 1
		if num_files != 12:
			raise Exception('Error: Duplicate files found.')
		output['rows_modified'] = rows_modified_dict
		output['rows_deleted'] = rows_delete_dict
		output['success_message'] = 'The files were successfully uploaded.'
		# print previous_file_date
		iso_dates = previous_file_date.split('/')
		date_val = int(iso_dates[1])
		if date_val < 10 :
			date_val = '0'+str(date_val)
		iso_date = iso_dates[2] +'-'+ iso_dates[0] +'-'+ str(date_val) 
		output['iso_date'] = iso_date+'T00:00:00'
		output['file_date'] = file_date
		output['isValid'] = 'true'
	rows_modified_dict = {}
	rows_delete_dict = {}
	# print json.dumps(output)
	return output, iso_date

def main():
	'''
	We have to use global to modify the value
	of the variable outside the function because
	the variable is global
	'''
	global output
	global all_files
	# Set to hold the different unique dates the file belongs
	unique_dates_set = set()
	# List to hold the dates so they can be sorted according to the date
	unique_dates_list = []
	output_list = []
	output_dict = {}
	iso_date_list = []	 
	try:
		# Iterate through all the .csv files and get the unique dates the files belong to from their file names
		for f in os.listdir(os.getcwd()):
			if f.endswith('.csv'):
				# Get the date-time fields from the file name
				file_dates = f.split('.')[0].split('_')[3].split('-')
				file_date = file_dates[0] +'-'+ file_dates[1] +'-'+ file_dates[2]
				unique_dates_set.add(str(file_date))
				all_files.append(os.path.basename(f))
		if len(all_files) == 0:
			raise Exception('Error: There are no CSV files to upload.')
		# elif len(all_files) % 12 != 0:
		# 	raise Exception('Error: Few files are missing. Please recheck if files are present for all the huts, for all the dates')
		else:
			# Convert the unique_dates_set (enforces uniqueness) to unique_dates_list (so we can sort the list) by iterating over the set items
			for dates in unique_dates_set:
				unique_dates_list.append(dates)
			unique_dates_list.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
			# print unique_dates_list
			# Need to verify before proceeding ahead if the files are continuous, before proceeding further
			verify_file_dates(unique_dates_list)
			# Group the files belonging to the same date and pass the list to be validated
			for file_date in unique_dates_list:
				files_grouped_by_date = [file_name for file_name in all_files if file_date in file_name]
				# outputOverall[file_date] = parse_files_for_date(files_grouped_by_date)
				retured_output , iso_date = parse_files_for_date(files_grouped_by_date, file_date)
				output_dict[iso_date] = retured_output
				iso_date_list.append(iso_date+'T00:00:00')
				output_list.append(output_dict)
				output_dict = {}
				# print output_list
			outputOverall['result'] = output_list
			outputOverall['iso_dates'] = iso_date_list
			outputOverall['success_message'] = 'The files were successfully uploaded.'
			outputOverall['isValid'] = 'true'
	except Exception as e:
		outputOverall['error_message'] = str(e)
	print json.dumps(outputOverall)

'''
This is used in `best practice`
but is not required. It simply
means that main will only be called
if the file is being ran manually.
'''
if __name__ == '__main__':
	main()
