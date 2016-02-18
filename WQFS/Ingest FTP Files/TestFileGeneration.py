#!/usr/bin/env python
'''
Sumukh Hallymysore Ravindra
shallymy@purdue.edu

Parsing WQFS Test
(C) Purdue University 2015
'''
from datetime import datetime
import os
import io
import sys
import json
import csv


for f in os.listdir(os.getcwd()):
	if f.endswith('.csv'):
		f = open(f,'r')
		fo = open('Test_'+f,'wb')
		# go through each line of the file
		for line in f:
		    bits = line.split(',')
		    # change first column
		    values= bits[0].split(' ')
		    if '/28/' in values[0] :
		    	bits[0] = '12/31/2008' + values[1]
		    else :
		    	bits[0] = '1/1/2009' + values[1]
		    # join it back together and write it out
		    fo.write( ','.join(bits) )

f.close()
fo.close()