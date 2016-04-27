#!/usr/bin/env python
'''
Authors:
Craig West
Sheifali Khare
Sumukh Hallymysore Ravindra

Parsing WQFS Data Files
(C) Purdue University 2015
'''
from datetime import datetime
import os
import io
import sys
import json
import csv
import collections

output = {}

# Date after which hut files for B and G have different header format
specific_date = datetime.strptime('2016-01-17', '%Y-%m-%d')

# Dictionary for hut variable
def create_hut_dict():
	hut_dict = dict()
	hut_dict['A'] = 1
	hut_dict['B'] = 2
	hut_dict['C'] = 3
	hut_dict['D'] = 4
	hut_dict['E'] = 5
	hut_dict['F'] = 6
	hut_dict['G'] = 7
	hut_dict['H'] = 8
	hut_dict['I'] = 9
	hut_dict['J'] = 10
	hut_dict['K'] = 11
	hut_dict['L'] = 12
	return hut_dict

# Read how many lines are in a file
def num_lines(filename):
	return sum(1 for line in open(filename)) - 1

# Converts the date into julian date with 24hr time
def convert_to_julian(date):
	dt = datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')
	tt = dt.timetuple()
	time = '{0:02d}:{1:02d}:{2:02d}'.format(tt.tm_hour, tt.tm_min, tt.tm_sec)
	return (tt.tm_year, tt.tm_yday, time)

# Find the rows modofied i.e; the rows which were deleted before it
def find_rows(rows_dict,hut_name):
	str_rows = []
	if hut_name in rows_dict:
		str_rows = [int(x) for x in rows_dict[hut_name].split(",")]
	return str_rows

# Find the rows modofied i.e; the rows which were deleted before it
def find_rows_modified(rows_dict,hut_name):
	str_rows = []
	if hut_name in rows_dict:
		str_rows = [str(x) for x in rows_dict[hut_name].split(",")]
	# print str_rows
	return str_rows

def parse_file(filename,rows_modified_dict,rows_deleted_dict,hut_name,file_date):
	global output
	file_date = datetime.strptime(file_date, '%Y-%m-%d')
	rows_modified = find_rows_modified(rows_modified_dict,hut_name)
	rows_deleted = find_rows(rows_deleted_dict,hut_name)
	# open our utf-16 encdode file for reading
	with io.open(filename, 'r', encoding='utf-16-le') as fr:
		calc_time = 100 #the first row will be of time 0100
		newRowNo = 0
		# iterate over each row
		for rowNum, row in enumerate(fr):
			if rowNum not in rows_deleted:
				output_data = output['266ac488-f15c-47df-815a-f00b06f04b0f'][newRowNo-1]
				tmp4 = {'number': hut_number}
				
				if newRowNo == 0:
					# Parse the header of the file into a list
					header = [col for col in row.replace('\n','').split(',')]
				else:
					# if we have no entries create the array
					if output_data == dict():
						output_data['Flows'] = []
						output_data['VWC'] = []
						output_data['Temp'] = []
						output_data['Hut'] = []
						output_data['rawTime'] = []
						output_data['annotation'] = []
							
					# Go over each column in the row
					for colNum, col in enumerate(row.replace('\n','').split(',')):
						'''
						From here on down we are checking what column we are in.
						We check to see what column we are in and add the information
						to the corrisponding location. Each Tile, Sensor WVC, and
						Sensor temp get their own entries in the list we created
						above. Also each row gets has corrisponding hut information
						which is stored in tmp4.
						'''

						# print "3a." + str(hut_name)

						if header[colNum].find('UTC_minus') != -1:
							tmp5 = {}
							tmp5['hut'] = hut_number
							tmp5['rawValue'] = col
							output_data['rawTime'].append(tmp5)
							
						elif header[colNum].find('- TB') != -1:
							tmp1 = {}
							tmp1['hut'] = hut_number
							tmp1['sensorNumber'] = header[colNum].split(" - ")[1]
							tmp1['fieldTitleNum'] = int(header[colNum][-1])						
							tmp1['numberOfTips'] = int(col)
							output_data['Flows'].append(tmp1)

						elif header[colNum].find('VWC') != -1:
							tmp2 = {}
							tmp2['hut'] = hut_number
							tmp2['sensorNumber'] = int(header[colNum].split(" - ")[0])
							if file_date > specific_date:
								if hut_name =='B' or hut_name =='G':
									tmp2['plotNumber'] = header[colNum].split(" - ")[1].split("_")[0]
									tmp2['sensorType'] = int(header[colNum].split(" - ")[1].split("_")[1][1])
								else:
									tmp2['plotNumber'] = header[colNum].split(" - ")[1].split(".")[0]
									tmp2['sensorType'] = int(header[colNum].split(" - ")[1].split(".")[1][1])
							else:
								tmp2['plotNumber'] = header[colNum].split(" - ")[1].split(".")[0]
								tmp2['sensorType'] = int(header[colNum].split(" - ")[1].split(".")[1][1])
							tmp2['rawValue'] = float(col)
							tmp2['calculatedValue'] = 0
							output_data['VWC'].append(tmp2)

						elif header[colNum].find('temp') != -1:
							tmp3 = {}
							tmp3['hut'] = hut_number
							tmp3['sensorNumber'] = int(header[colNum].split(" - ")[0])
							if file_date > specific_date:
								if hut_name =='B' or hut_name =='G':
									tmp3['plotNumber'] = header[colNum].split(" - ")[1].split("_")[0]
									# Hut B files have column header mistake
									# Handling this case separately
									if tmp3['plotNumber'] == "P5BS1":
										tmp3['plotNumber'] = header[colNum].split(" - ")[1].split("_")[0].split("S")[0]
										tmp3['sensorType'] = int(header[colNum].split(" - ")[1].split("_")[0][4])
									else:
										tmp3['sensorType'] = int(header[colNum].split(" - ")[1].split("_")[1][1])	
								else:
									tmp3['plotNumber'] = header[colNum].split(" - ")[1].split(".")[0]
									tmp3['sensorType'] = int(header[colNum].split(" - ")[1].split(".")[1][1])
							else:
								tmp3['plotNumber'] = header[colNum].split(" - ")[1].split(".")[0]
								tmp3['sensorType'] = int(header[colNum].split(" - ")[1].split(".")[1][1])			
							tmp3['rawValue'] = float(col)
							tmp3['calculatedValue'] = 0
							output_data['Temp'].append(tmp3)

						elif header[colNum].find('T1') != -1:
							tmp4['T1'] = float(col)

						elif header[colNum].find('SOL') != -1:
							tmp4['SOL'] = float(col)

						elif header[colNum].find('BATT') != -1:
							tmp4['BATT'] = float(col)

						elif header[colNum].find('LOWV') != -1:
							tmp4['LOWV'] = int(col)

						elif header[colNum].find('ScriptError') != -1:
							tmp4['ScriptError'] = int(col)

						elif header[colNum].find('InternalError') != -1:
							tmp4['InternalError'] = int(col)

						elif header[colNum].find('RadioError') != -1:
							tmp4['RadioError'] = int(col)

						elif header[colNum].find('SensorError') != -1:
							tmp4['SensorError'] = int(col)

						elif header[colNum].find('LowBattError') != -1:
							tmp4['LowBattError'] = int(col)

						elif header[colNum].find('FloodError') != -1:
							tmp4['FloodError'] = int(col)

						elif header[colNum].find('SerialError') != -1:
							tmp4['SerialError'] = int(col)

						# else:
							# print "Error." + str(hut_name)

					output_data['Hut'].append(tmp4)
					if int(calc_time) < 1000 :
						output_data['calculatedtime'] = "0"+ str(calc_time)
					else:
						output_data['calculatedtime'] = str(calc_time)
					calc_time += 100

					annotation = 'Removed following entries'
					tmp5 = {}
					tmp5['hut'] = hut_number
					annotation_present = False
					
					# print rows_modified
					for err in rows_modified:
						if ('<<'+str(newRowNo) + '>>') in err:
							annotation = annotation + str(' -->'+err.split('>>')[1])
							annotation_present = True

					if(annotation_present):
						tmp5['annotationText'] = annotation
						output_data['annotation'].append(tmp5)
				newRowNo = newRowNo + 1

# Convert the unicode code dictionary into ascii string format
def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def parse_each_date(file_records, iso_date):
	'''
	We have to use global to modify the value
	of the variable outside the function because
	the variable is global
	'''
	global output
	global hut_number
	# file_records = convert(file_records)
	hut_number = 0
	output = {}
	output = {
		'266ac488-f15c-47df-815a-f00b06f04b0f':[dict() for d in xrange(24)] # initialize our 24 entries
	}
	rows_modified_dict = file_records['rows_modified']
	rows_deleted_dict = file_records['rows_deleted']
	# Need to use iso date to find out if rcords are present or not
	# print iso_date
	previous_records = {}
	file_date = file_records['file_date']
	if len(previous_records) != 0 :
		raise Exception("Error. Records already present for this date.")
	hut_num_dict = create_hut_dict()	
	# Iterate the current directory looking
	# for the CSV files
	for f in sorted(os.listdir(os.getcwd())):
		if f.endswith('.csv') and (file_date in f):
			# print os.path.basename(f)
			hutName = str(f).split("_")[0].split("-")			
			hut_number = hut_num_dict[str(hutName[1])] 
			parse_file(f,rows_modified_dict,rows_deleted_dict,hutName[1], file_date)
	# print json.dumps(output)
	return output

def main():
	'''
	We have to use global to modify the value
	of the variable outside the function because
	the variable is global
	'''
	results_list = []
	results = {'isValid':'false'}
	fileresults = {}
	try:
		inputData = sys.stdin.read()
		
		fw = open("jsonWQFSInput", "w")
		fw.write(inputData)
		fw.close()

		data = json.loads(inputData)
		# print data[0]
		all_results = data['result']
		# DB query results
		previous_records = data['previous_records']

		# Old way
		
		# data = inputData.split(";")
		# # print data[0]
		# all_results = json.loads(data[0])
		# # DB query 
		# previous_records = json.loads(data[1])

		if previous_records:
			previous = set()
			for record in previous_records:
				previous.add(record)
			record_dates = ', '.join(str(rec) for rec in previous)
			raise Exception("Error. Records already present for dates:"+record_dates)
		if len(all_results) == 0 :
			raise Exception("Error. No results from the Validation stage to Ingest files stage.")
		# Iterate the current directory looking
		# for the CSV files
		for iso_date in all_results:
			# print iso_date
			for key,value in iso_date.iteritems():
				returned_output = {}
				returned_output[key] = parse_each_date(value, key)
				results_list.append(returned_output)
		results['success_message'] = 'Data extracted from file to template successfully. '
		results['last_file_read'] = ''
		results['isValid'] = 'true'		
		f = open('jsonParseFile', 'w')
		fileresults['result'] = results_list
		f.write(json.dumps(fileresults))
	except Exception as e:
		results['error_message'] = str(e)
	print json.dumps(results)

'''
This is used in `best practice`
but is not required. It simply
means that main will only be called
if the file is being ran manually.
'''
if __name__ == '__main__':
	main()
