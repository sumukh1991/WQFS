#!/usr/bin/env python
'''
Sheifali Khare
khare2@purdue.edu

Calculate Julian Day and Year. ALso identify the previous JDay
(C) Purdue University 2015
'''
from datetime import datetime, timedelta
import os
import io
import sys
import json
import csv


currJDay = 0
currYear = 0
prevJDay = 0
prevJyear = 0
output = {
	'isValid':'true'   
	}
sensor_dict = dict()
sensor_dict[1] = "Shallow"
sensor_dict[2] = "Deep"

# Converts the date into julian date with 24hr time
def convert_to_julian(date):
	dt = datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')
	dt = dt.replace(minute = 0,second = 0)
	dt = dt + timedelta(hours = 5)
	tt = dt.timetuple()
	time = '{0:02d}:{1:02d}:{2:02d}'.format(tt.tm_hour, tt.tm_min, tt.tm_sec)
	
	return (tt.tm_year, tt.tm_yday)


''' Calculate the prevous Julian Day . Also set the global variable - "Current Julian Day - currJDay" and "current Year- cuurYear"'''
def calculateJulianDay(inputDataArray):	
	global currJDay
	global currYear
	for i in inputDataArray:
		for j in i['rawTime']:
			year,jDay = convert_to_julian(j['rawValue'])
			#Set the Julian Date and Year for the data
			i['Year'] = year
			i['JDay'] = jDay
			currJDay = jDay
			currYear = year
			
		
'''Calculate ISO Day format for many reason'''
def calculateISODay(inputDataArray):
	global currJDay
	global currYear	 
	for i in inputDataArray:
		'''the current day is reduced by 1, because while calculating isoDay in the line below - we begin from day 1 and then add no of days to it.
		So we need to substract the no of days by 1'''
		jtempday = int(currJDay) - 1
		i['isoDay'] = str((datetime(currYear, 1, 1) + timedelta(jtempday)).isoformat())

def calculatePreviousDay():
	global prevJDay
	global prevJyear
	prevJtempDay = prevJDay - 1
	previousDate = (datetime(prevJyear, 1, 1) + timedelta(prevJtempDay)).isoformat()
	return str(previousDate)			

def calculateprevJdayJyear():
	global prevJDay
	global prevJyear
	global currJDay
	global currYear
	prevJDay = int(currJDay) - 1
	if(prevJDay == 0):
		prevJyear = currYear - 1
		if(prevJyear % 4 == 0):
			prevJDay = 366
		else:
			prevJDay = 365
	else:
		prevJyear = currYear
	
	
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
	global currJDay
	global currYear
	try:	
		inputData = sys.stdin.read()
		# For debug purpose - write data into file
		fw = open("jsonCalculateJulianDateInput", "w")
		fw.write(inputData)
		fw.close()
		# Parse data 
		data = inputData.split(";");
		inputDataArray = json.loads(data[0])
		# First calcuate Julain day and then calulate ISO Day 
		calculateJulianDay(inputDataArray)
		calculateISODay(inputDataArray)
		#Calculate previous julian day and year
		calculateprevJdayJyear()
		
		output['prevJDay'] = prevJDay
		output['year'] = prevJyear
		output['previousDay'] = calculatePreviousDay()
		output['266ac488-f15c-47df-815a-f00b06f04b0f'] = inputDataArray
		output['success_message'] = 'Convert to juilan date and calculatedDay term updated'		
		
		# For debug purpose - write data into file
		fw = open("jsonCalculateJulianDateOutput", "w")
		fw.write(json.dumps(output))
		fw.close()	
	except Exception as e:
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
