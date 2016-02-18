#!/usr/bin/env python
'''
Craig West
west1@purdue.edu

Parsing WQFS Data Files
(C) Purdue University 2015
'''
from datetime import datetime
import os
import io
import sys
import json
import csv



output = {
	'isValid':'true' ,
	'266ac488-f15c-47df-815a-f00b06f04b0f': ''
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
		
		data = inputData.split(";")
		#print data
		inputDataArray = json.loads(data[0])
		calibrationKeyArray = json.loads(data[1])
		previousDayArray = json.loads(data[2])
		
		calculate_difference_in_tips(inputDataArray,previousDayArray)
		convert_tips_to_flow(inputDataArray,calibrationKeyArray)
		convert_temp_values(inputDataArray)
		convert_vwc_values(inputDataArray)
		
		fw = open("jsonCalibrationOutput", "w")
		fw.write(json.dumps(inputDataArray))
		fw.close()
		
		output['266ac488-f15c-47df-815a-f00b06f04b0f'] = inputDataArray
		output['success_message'] = 'Files uploaded succesfully and data calibrated as expected.'
	except Exception as e:
		#If there is an error with parsing catch it and send it
		output['isValid'] = 'false'
		del output['266ac488-f15c-47df-815a-f00b06f04b0f']
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
