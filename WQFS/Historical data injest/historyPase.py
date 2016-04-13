'''
Authors:
Sumukh Hallymysore Ravindra

One time parse of the WQFS Sensor history data
'''

import csv
from datetime import datetime, timedelta
import linecache

# Main function called on running the file
def main():
	try:
		# List to hold the dates whose data has been parsed
		dateList = []

		print 'Parsing the file...'
		
		# --------------
		# Parse the data to get the different dates in the file for which the data needs to be parsed and saved in the files

		# Import the data in the csv file to a dictionary object
		csvFile = csv.DictReader(open('WQFS_history_data.csv','rb'), delimiter=',', fieldnames=['fieldSection','fieldDateTime','fieldValue','fieldIdentifier'])
		# Parse the data
		for line in csvFile:
			# print line['fieldDateTime']
			varDate = str(line['fieldDateTime']).split(' ')[0]
			# If the date is not present in the list, append it
			# Maintaining the order of the dates would help in parsing the file better (else will result in 'n' complexity) 
			if varDate not in dateList:
				dateList.append(varDate)

		# ---------------
		# Parse the file for data

		# Get the date value
		for date in dateList:

			# Variables to hold the comma separated values of a hut (6 plots) and save them later in individual file
			strFileHeader = '''UTC_minus_5,24 - P1A.S1.temp,25 - P1A.S2.temp,26 - P1A.S1.VWC,27 - P1A.S2.VWC,28 - P1B.S1.temp,29 - P1B.S2.temp,30 - P1B.S1.VWC,31 - P1B.S2.VWC,32 - P2A.S1.temp,
			33 - P2A.S2.temp,34 - P2A.S1.VWC,35 - P2A.S2.VWC,36 - P2B.S1.temp,37 - P2B.S2.temp,38 - P2B.S1.VWC,39 - P2B.S2.VWC,
			40 - P3A.S1.temp,41 - P3A.S2.temp,42 - P3A.S1.VWC,43 - P3A.S2.VWC,1001 - P3B.S1.temp,1003 - P3B.S2.temp,1005 - P3B.S1.VWC,1007 - P3B.S2.VWC,
			48 - P4A.S1.temp,49 - P4A.S2.temp,50 - P4A.S1.VWC,51 - P4A.S2.VWC,1009 - P4B.S1.temp,1011 - P4B.S2.temp,1013 - P4B.S1.VWC,1015 - P4B.S2.VWC,
			56 - P5A.S1.temp,57 - P5A.S2.temp,58 - P5A.S1.VWC,59 - P5A.S2.VWC,60 - P5B.S1.temp,61 - P5B.S2.temp,62 - P5B.S1.VWC,63 - P5B.S2.VWC,
			64 - P6A.S1.temp,65 - P6A.S2.temp,66 - P6A.S1.VWC,67 - P6A.S2.VWC,1017 - P6B.S1.temp,1019 - P6B.S2.temp,1021 - P6B.S1.VWC,1023 - P6B.S2.VWC,
			74 - ScriptError,75 - InternalError,76 - RadioError,77 - SensorError,78 - LowBattError,1 - TB1,2 - TB2,3 - TB3,4 - TB4,5 - TB5,6 - TB6,8 - T1,9 - SOL,10 - BATT,11 - LOWV\n'''
			
			dictHutA = {}
			dictHutB = {}
			dictHutC = {}
			dictHutD = {}
			dictHutE = {}
			dictHutF = {}
			dictHutG = {}
			dictHutH = {}
			dictHutI = {}
			dictHutJ = {}
			dictHutK = {}
			dictHutL = {}

			dictHutA['header'] = strFileHeader
			dictHutA['date'] = date

			for line in csvFile:
				
				if date not in line['fieldDateTime']:
					continue

				# Strip the micro seconds from the date time value 
				varDateRecord = str(line['fieldDateTime']).split('.')[0]

				# Convert (from) yyyy-mm-dd hh:mm:ss -> (to) mm/dd/yyyy hh:mm:ss AM/PM

				varDateRecord = datetime.strftime(datetime.strptime(varDateRecord, '%Y-%m-%d %H:%M:%S'), '%m/%d/%Y %I:%M:%S %p')

				if 'Plot' in line['fieldSection']:
					intPlotNo = int(line['fieldSection'].split(' ')[1])
					intHutIndex = math.ceil(intPlotNo/6)
					# Hut A
					if intHutIndex == 1:
						listValues =  []
						if intPlotNo != 01
							listValues = dictHutA[varDateRecord]
						listValues.append(line['fieldValue'])
						# Update the list
						dictHutA[varDateRecord] = listValues
					# Hut B
					if intHutIndex == 2:
						listValues =  []
						if intPlotNo != 07
							listValues = dictHutB[varDateRecord]
						listValues.append(line['fieldValue'])
						# Update the list
						dictHutA[varDateRecord] = listValues
					# Hut C
					if intHutIndex == 3:
						listValues =  []
						if intPlotNo != 13
							listValues = dictHutC[varDateRecord]
						listValues.append(line['fieldValue'])
						# Update the list
						dictHutA[varDateRecord] = listValues
					# Hut D
					if intHutIndex == 4:
						listValues =  []
						if intPlotNo != 19
							listValues = dictHutD[varDateRecord]
						listValues.append(line['fieldValue'])
						# Update the list
						dictHutA[varDateRecord] = listValues
					# Hut E
					if intHutIndex == 5:
						listValues =  []
						if intPlotNo != 25
							listValues = dictHutE[varDateRecord]
						listValues.append(line['fieldValue'])
						# Update the list
						dictHutA[varDateRecord] = listValues
					# Hut F
					if intHutIndex == 6:
						listValues =  []
						if intPlotNo != 31
							listValues = dictHutF[varDateRecord]
						listValues.append(line['fieldValue'])
						# Update the list
						dictHutA[varDateRecord] = listValues
					# Hut G
					if intHutIndex == 7:
						listValues =  []
						if intPlotNo != 37
							listValues = dictHutG[varDateRecord]
						listValues.append(line['fieldValue'])
						# Update the list
						dictHutA[varDateRecord] = listValues
					# Hut H
					if intHutIndex == 8:
						listValues =  []
						if intPlotNo != 43
							listValues = dictHutH[varDateRecord]
						listValues.append(line['fieldValue'])
						# Update the list
						dictHutA[varDateRecord] = listValues

				elif 'Tile Spacing' in line['fieldSection']:

				elif 'Bucket' in line['fieldSection']:

				elif 'WQFS' in line['fieldSection']:

		
	except Exception as e:
		print e

	print 'Completed'

if __name__ == '__main__':
	main()

