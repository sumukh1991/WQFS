#!/usr/bin/env python
'''
Authors:
Sumukh Hallymysore Ravindra

Parse the jsonResultFile and iterate over the records to 
calculate julian data and flow values based on the calibration records

(C) Purdue University 2015
'''
from datetime import datetime
import os
import io
import sys
import json
import csv
import collections

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

def main():
	'''
	We have to use global to modify the value
	of the variable outside the function because
	the variable is global
	'''
	results_list = []
	results = {'isValid':'false'}
	file_results = {}
	is_last_file = True
	try:
		inputData = sys.stdin.read()
		
		data = json.loads(inputData)
		last_file_read = data['last_file_read']
		isValid = data['isValid']
		error_message = data['error_message']

		if not isValid:
			raise Exception('Error: '+ str(error_message))

		# data = inputData.split(";")
		# last_file_read = data[0]

		# Open the file where the results have been stored by wqfs.py script
		fr = open("jsonParseFile", "r")
		file_results = json.load(fr)
		fr.close()

		# Keep track of the loop iteration, used for getting computed results for the previous day (from the finalOutput file)
		iterate_count = 0

		results_list = convert(file_results['result'])
		first_parse = 'false'
		for items in results_list:
			for key,value in items.iteritems():
				next_file_date = datetime.strptime(key, "%Y-%m-%d")
				next_key = key
				break_flag = False
				if not last_file_read:
					is_last_file = False
					first_parse = 'true'
					break_flag = True
					break
				last_file_date = datetime.strptime(last_file_read, "%Y-%m-%d")
				if next_file_date <= last_file_date:
					iterate_count += 1
					continue
				is_last_file = False
				break_flag = True
			if break_flag:
				break
		if not is_last_file:
			results['is_last_file'] = 'false'
			results['first_parse'] = first_parse
			results['iterate_count'] = iterate_count
			results['iso_day'] = next_key
			results['result'] = items[next_key]['266ac488-f15c-47df-815a-f00b06f04b0f']
			results['success_message'] = 'Data forwarded to next task successfully.'
			results['isValid'] = 'true'
		else:
			results['is_last_file'] = 'true'
			results['isValid'] = 'true'
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
