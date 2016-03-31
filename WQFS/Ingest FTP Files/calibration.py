#!/usr/bin/env python
'''
Craig West
west1@purdue.edu

Parsing WQFS Data Files
(C) Purdue University 2015
'''
from datetime import datetime, timedelta
import os
import io
import sys
import json
import csv
import collections
from operator import itemgetter

output = {
	'isValid':'false'
	}
sensor_dict = dict()
sensor_dict[1] = "Shallow"
sensor_dict[2] = "Deep"

''' Find the calibration value for converting tips to a flow for a particular field tile in a hut'''
def find_tip_calibration_key(calibrationKeyArray, hut, sensorNumber):
	key = {}
	for i in calibrationKeyArray:
		for j in i['flowCalibrations']:		
			if int(j['hut']) == int(hut) and j['sensorNumber'] == sensorNumber:			 
				 key['fieldTile'] = j['fieldTile']
				 key['volumePerTip'] = j['volumePerTip']
	return key
			 
			 
'''Function to convert tips to flow'''		 
def convert_tips_to_flow(inputDataArray,calibrationKeyArray):
	for plots in inputDataArray :
		for tile in plots['Flows'] :
			calibration_key = find_tip_calibration_key(calibrationKeyArray,tile['hut'],tile['sensorNumber'])
			tile['fieldTile'] = calibration_key['fieldTile']
			tile['fieldTileFlow'] = (calibration_key['volumePerTip']) * int(tile['differenceInTips'])
			
#Calculate differtence in tips			
def calculate_difference_in_tips(inputDataArray,previousDayArray):
	for plots in inputDataArray :
		for tile in plots['Flows'] :
			previousTipCount = find_previous_hour_tip_count(plots["calculatedtime"],inputDataArray,previousDayArray,tile['hut'],tile['sensorNumber'])
			# print previousTipCount
			tile["differenceInTips"] = float(tile["numberOfTips"]) - float(previousTipCount)

			
			
#Find no of tips in previous hour
def find_previous_hour_tip_count(currenthour,currentDayArray,previousDayArray,hutNumber,sensorNumber):
	previousTipCount = 0
	previousHour = int(currenthour) - 100
	if(int(previousHour) == 0):	
		for plots in previousDayArray:
			if int(plots['calculatedtime']) == int(2400) :
				for tile in plots['Flows'] :
					if hutNumber == tile['hut'] and sensorNumber == tile['sensorNumber']:						
						previousTipCount = tile["numberOfTips"]
						break;
	else:
		for plots in currentDayArray:
			if int(previousHour) == int(plots['calculatedtime']) :
				for tile in plots['Flows'] :
					if hutNumber == tile['hut'] and sensorNumber == tile['sensorNumber']:						
						previousTipCount = tile["numberOfTips"]						
						break;	
	return previousTipCount

''' Convert temp value based on sensor type.
 Sensor 20-999 are scaled. 
 Divide the temp value by 10
 Also convert sensorType to sensorLocation'''
def convert_temp_values(inputDataArray):
	for hut in inputDataArray :
		for row in hut['Temp'] :
			if row['sensorNumber'] >= 20 and row['sensorNumber'] <= 999 :
				row['calculatedValue'] =  float(row['rawValue']) / 10.0
			else:
				row['calculatedValue'] =  float(row['rawValue']) 
			row['sensorLocation'] = sensor_dict[row['sensorType']]

''' Convert VWC value based on sensor type. 
Sensor 20-999 are scaled.
 Divide the VWC value by 100
 Also convert sensorType to sensorLocation'''
def convert_vwc_values(inputDataArray):
	for hut in inputDataArray :
		for row in hut['VWC'] :
			if row['sensorNumber'] >= 20 and row['sensorNumber'] <= 999 :
				row['calculatedValue'] =  float(row['rawValue']) / 100.0
			else:
				row['calculatedValue'] =  float(row['rawValue'])
			row['sensorLocation'] = sensor_dict[row['sensorType']]


# Convert the unicode code array of dictionary into ascii string ditionary format
def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

'''
Our main function of the file.
This function searches the directory
for files and passes each file to the
funtion to be parsed.
'''
def main():
	'''
	We have to use global to modify the value
	of the variable outside the function because
	the variable is global
	'''
	global output
	try:	
		inputData = sys.stdin.read()
		
		fw = open("jsonCalibrationInput", "w")
		fw.write(inputData)
		fw.close()
		
		data = json.loads(inputData)
		# print data
		data = convert(data)
		# print data
		inputDataArray = data['result']
		calibrationKeyArray = data['calibration_values']
		previousDayArray = data['previous_day_values']
		isoDay = data['iso_day']
		first_parse = data['first_parse']
		iterate_count = int(data['iterate_count'])

		# Variable to hold the already computed data of previous days from the finaloutput file 
		result = []
		
		fd = os.open("finalOutput", os.O_RDWR | os.O_CREAT)

		fw = os.fdopen(fd,"r+")

		if first_parse == 'false':
			# Get the previous day records stored in the finalouput file
			result = json.load(fw)
			previousDayArray = itemgetter(slice((iterate_count - 1)*24,(iterate_count - 1)*24+24))(result)
			previousDayArray = convert(previousDayArray)
		
		calculate_difference_in_tips(inputDataArray,previousDayArray)
		convert_tips_to_flow(inputDataArray,calibrationKeyArray)
		convert_temp_values(inputDataArray)
		convert_vwc_values(inputDataArray)

		# Since the file is read already, move the file header from EOF back to the start
		fw.seek(0)
		# Check if the file is empty
		if os.stat("finalOutput").st_size != 0:
			result = json.load(fw)
			# result = outputFile['266ac488-f15c-47df-815a-f00b06f04b0f']
		else:
			outputFile = {}

		# Append the data computed in the current iteration to the previous results
		for hut in inputDataArray:
			result.append(hut)
		
		fw.seek(0)
		# Write the results to the finaloutput file
		fw.write(json.dumps(result))
		fw.close()

		output['last_file_read'] = isoDay
		output['success_message'] = 'Files uploaded succesfully and data calibrated as expected for :'+ isoDay
		output['isValid'] = 'true'

	except Exception as e:
		#If there is an error with parsing catch it and send it
		output['error_message'] = str(e)

	print json.dumps(output)
	

'''
This is used in `best practice`
but is not required. It simply
means that main will only be called
if the file is being ran manually.
'''
if __name__ == '__main__':
	main()
