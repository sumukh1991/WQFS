#!/usr/bin/env python
'''
Sheifali Khare
khare2@purdue.edu

Generating excel worksheet for flow
(C) Purdue University 2015
'''
from datetime import datetime
import os
import io
import sys
import json
import csv
import zipfile

fileList = []
output = {
	'isValid':'true'   
	}
			
#Create CSV File		
def create_csv_file(file_title):	
	outputFile = open(file_title, 'w')
	outputWriter = csv.writer(outputFile)
	return (outputFile,outputWriter)

#Create VWC/Temp Header row
def add_vwctemp_header_row(outputWriter,inputDataArray,hutNumber):
	headerrow = ['year','julianDay','time']
	tile_id = 'H' + str(hutNumber) + '.Temp'
	headerrow.append(tile_id)
	tile_id = 'H' + str(hutNumber) + '.Solar (V)'
	headerrow.append(tile_id)
	tile_id = 'H' + str(hutNumber) + '.Battery (V)'
	headerrow.append(tile_id)
	tile_id = 'H' + str(hutNumber) + '.ScriptError'
	headerrow.append(tile_id)
	if hutNumber != 7 :
		tile_id = 'H' + str(hutNumber) + '.InternalError'
		headerrow.append(tile_id)
	tile_id = 'H' + str(hutNumber) + '.RadioError'
	headerrow.append(tile_id)
	tile_id = 'H' + str(hutNumber) + '.SensorError'
	headerrow.append(tile_id)
	tile_id = 'H' + str(hutNumber) + '.LowBatteryError'
	headerrow.append(tile_id)
	if hutNumber != 7 and hutNumber != 1 :
		tile_id = 'H' + str(hutNumber) + '.FloodError'
		headerrow.append(tile_id)	
	for i in inputDataArray[0]['VWC']:
		if i['hut'] == hutNumber:
			tile_id = 'H'+ str(hutNumber) + '.' + i['plotNumber'] + '.S' + str(i['sensorType']) +'.'
			headerrow.append(tile_id + 'VWC(%)')
			headerrow.append(tile_id + 'Temp(C)')
	tile_id = 'Annotation'
	headerrow.append(tile_id)
	outputWriter.writerow(headerrow)

#Create VWC/Temp Object
def create_vwc_temp_object(inputDataArray,hutNumber):
	arr_obj =  []
	for i in inputDataArray :
		temp_obj = []
		temp_obj.append(i['Year'])
		temp_obj.append(i['JDay'])
		temp_obj.append(i['calculatedtime'])
		temp_obj.append(i['Hut'][hutNumber-1]['T1']) 
		temp_obj.append(i['Hut'][hutNumber-1]['SOL'])
		temp_obj.append(i['Hut'][hutNumber-1]['BATT'])
		temp_obj.append(i['Hut'][hutNumber-1]['ScriptError'])
		#Hut G does not have InternalError record
		if hutNumber != 7 :
			temp_obj.append(i['Hut'][hutNumber-1]['InternalError'])
		temp_obj.append(i['Hut'][hutNumber-1]['RadioError'])
		temp_obj.append(i['Hut'][hutNumber-1]['SensorError'])
		temp_obj.append(i['Hut'][hutNumber-1]['LowBattError'])
		#Hut A and G does not have FloodError record
		
		if hutNumber != 7 and hutNumber != 1:			
			temp_obj.append(i['Hut'][hutNumber-1]['FloodError'])
		for j in i['VWC'] :
			if(j['hut'] == hutNumber):
				temp_obj.append(j['calculatedValue'])
				for x in i['Temp']:
					if( x['hut'] == hutNumber and j['plotNumber'] == x['plotNumber'] and j['sensorType'] == x['sensorType']): 
						temp_obj.append(x['calculatedValue'])
		if('annotation' in i.keys()):
			temp_obj.append(i['annotation'])
		arr_obj.append(temp_obj)
	return arr_obj
#Create Flow Header row
def add_flw_header_row(outputWriter,inputDataArray):
	headerrow = ['year','julianDay','time']
	for i in inputDataArray[0]['Flows']:
		tile_id = 'fieldTileFlow ' + str(i['fieldTile']) + ' (liters)'
		headerrow.append(tile_id)
	outputWriter.writerow(headerrow)

#Create Flow Object
def create_flow_object(inputDataArray):
	flow_arr_obj =  []	
	for i in inputDataArray :
		flow_obj = []
		flow_obj.append(i['Year'])
		flow_obj.append(i['JDay'])
		flow_obj.append(i['calculatedtime'])
		for j in i['Flows'] :			
			flow_obj.append(j['fieldTileFlow'])
		flow_arr_obj.append(flow_obj)
	return flow_arr_obj

#Write Data in CSV File
def write_csv_file(arr_obj,outputWriter):
	for i in arr_obj:
		outputWriter.writerow(i)

#Close CSV File
def close_csv_file(outputFile):
	outputFile.close()

# Generate VWC/Temp Files
def generate_vwctemp_files(inputDataArray):
	global fileList
	for hutNumber in range(1,13):
		file_title = 'WQFSHut' + str(hutNumber) + 'FieldTempVWCDataExport.csv'
		fileList.append(file_title)
		outputFile,outputWriter = create_csv_file(file_title)
		add_vwctemp_header_row(outputWriter,inputDataArray,hutNumber)
		vmp_temp_obj = create_vwc_temp_object(inputDataArray,hutNumber)
		write_csv_file(vmp_temp_obj,outputWriter)
		close_csv_file(outputFile)

# Generate Flow Files		
def generate_flow_file(inputDataArray):
	global fileList
	file_title = 'WQFSFieldTileFlowDataExport.csv'
	fileList.append(file_title)
	outputFile,outputWriter = create_csv_file(file_title)
	add_flw_header_row(outputWriter,inputDataArray)
	flow_arr_obj = create_flow_object(inputDataArray)
	write_csv_file(flow_arr_obj,outputWriter)
	close_csv_file(outputFile)

# Generate Zip Files
def generate_zip_file(fileName):
	global fileList
	myzip = zipfile.ZipFile(fileName + '.zip', 'w')
	for fileName in fileList:
		myzip.write(fileName)

#Function to read JSON Data line by line from a file
def readJSONData(fileName):
	data = []
	with open(fileName) as f:
		for line in f:
			if line[0] == "[" or line[0] == ']':
				pass
			elif line[0] == ',':
				line = line[2:]
				data.append(json.loads(line))
			else:
				data.append(json.loads(line))
	data = sorted(data, key=lambda k: (k['isoDay'],int(k["calculatedtime"])))
	fw = open("sorted.txt", "w")
	fw.write(json.dumps(data))
	fw.close()	
	return data				
					
'''Our main function of the file.
This function generates flow excel file
'''
def main():
	'''
	We have to use global to modify the value
	of the variable outside the function because
	the variable is global
	'''
	global output
	try:		
		inputDataArray = readJSONData('ftpInputData')
		generate_vwctemp_files(inputDataArray)
		generate_flow_file(inputDataArray)
		generate_zip_file('HutDataZip')
		output['isValid'] = 'true'
		output['success_message'] = "Files created"
	except Exception as e:

		output['isValid'] = 'false'
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
