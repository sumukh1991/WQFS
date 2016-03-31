#!/usr/bin/env python
'''
Author:
Sumukh Hallymysore Ravindra

Parsing WQFS Data Files
(C) Purdue University 2015
'''
import os
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
	try:
		results = {}
		result = []
		finalresultstr = '['
		first = 1

		fd = os.open("finalOutput", os.O_RDWR | os.O_CREAT)

		fw = os.fdopen(fd,"r")

		# Check if the file is empty
		if os.stat("finalOutput").st_size != 0:
			result = json.load(fw)
			result = convert(result)
			results['isValid'] = 'true'
			results['success_message'] = 'Data extracted from file to template successfully.'
			for record in result:
				if first:
					finalresultstr = finalresultstr+json.dumps(record)
					first = 0
				else:
					finalresultstr = finalresultstr+'\n'+json.dumps(record)
			finalresultstr = finalresultstr+']'
			# print result
		else:                                                                                                                                              
			results['isValid'] = 'false'

		f = open('jsonFinalOutputStr', 'w')
		f.write(finalresultstr)
		f.close()
		
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
