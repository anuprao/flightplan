#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# fp.py
#
# Copyright (c) 2017 Anup Jayapal Rao <anup.kadam@gmail.com>
#
# Ref: https://www.electricmonk.nl/docs/dependency_resolving_algorithm/dependency_resolving_algorithm.html
#

import argparse
import ctypes
import datetime
from enum import Enum, unique
import json
import logging
import math
import os
import os.path
import platform
#from queue import Queue
import shutil
import subprocess
import sys
import time
import datetime
#import threading
#from threading import Thread

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import colorama
from colorama import Fore, Back, Style

import svgwrite

weekend_list = None
holidy_list = None

milestone_list = None

class daterange:
	pass

class tasknode:

	def __init__(self, name):
		self.name = name
		self.dependencies = []
		self.start_date = None
		self.end_date = None
		self.num_hrs = 8
		self.is_critical = False
		self.consider_weekend = False
		self.consider_holiday = False

		self.is_complete = False

	def addDependency(self, tasknode):
		self.dependencies.append(tasknode)

def dep_resolve(tasknode, resolved, unresolved, errorList):
	bRetVal = True
	
	#print(">", tasknode.name)
	
	unresolved.append(tasknode)
	
	'''
	print("tasknode.dependencies")
	for samplenode in tasknode.dependencies:
		print(samplenode.name, end=':')
	print()
	'''
	
	iterTaskDep = iter(tasknode.dependencies)
	
	bDone = False
	while(False == bDone):
		oSubTask = next(iterTaskDep, None)
		if None == oSubTask:
			bDone = True
		else:
			#print("samplenode")
			#for samplenode in resolved:
			#	print(samplenode.name, end=':')
				
			if oSubTask not in resolved:
				if oSubTask in unresolved:
					errorList.append("Circular reference detected ")
					errorList.append(tasknode.name)
					errorList.append("-->")
					errorList.append(oSubTask.name)
					bRetVal = False
					bDone = True
				else:
					bRetValSubTask = dep_resolve(oSubTask, resolved, unresolved, errorList)
					bRetVal = bRetVal and bRetValSubTask
					if False == bRetVal:
						bDone = True
	
	if True == bRetVal:
		resolved.append(tasknode)
		unresolved.remove(tasknode)
	
	return bRetVal

class srcinput:
	
	def checkDuplicateIds():
		pass

	def autoPrefixIds():
		pass

	def addTrack():
		pass

	def addTaskToTrack():
		pass

class gantt:

	def addSrcLocalPath():
		pass

	def addSrcURL():
		pass

	def resolveDependency():
		pass
	
	def checkCircularDependency():
		pass

	def setStartDate():
		pass

	def excludeWeekends():
		pass

	def excludeHolidays():
		pass

	def checkMilestones():
		pass

	def generate():
		# Identify node ends 
		# Identify node starts
		pass

	def render():
		pass
	
class ganttsvg:

	def renderTask():
		# Without dependencies, colour: yellow
		# With dependencies, colour: light yellow
		# With 'critical' flag, colour: red boundary
		# With 'consider weekend' flag, colour: orange1 boundary
		# With 'consider holiday' flag, colour: orange2 boundary
		# With 'is_complete' flag, colour: blue
		pass

	def renderCurrDateLine():
		pass

	def renderWeekends():
		pass

	def renderHolidays():
		pass
	
	def renderMilestones():
		pass

	def renderTracks():
		pass

	def renderDateRanges():
		pass

	def render():
		pass

class ganttpng:

	def render():
		pass
	
h1 = datetime.datetime.fromisoformat('2020-11-16')

def getAvailableHrsFor(dtSample):
	numAvailableHrs = 8

	#print(dtSample, h1, h1 == dtSample)
	if h1 == dtSample:
		numAvailableHrs = 0

	return numAvailableHrs

def planEffort(oActivityList, dtCommence):
	#print(dtFrom)

	tdDay = datetime.timedelta(hours=24)

	tmpDtStart = None

	tmpDtEnd = None

	tmpDtCurr = dtCommence.replace()

	#print(tmpDtFrom)

	for tasknode in resolved:
		print(tasknode.name, "<", tasknode.num_hrs, ">", end=' ')
	
		#num_days = tasknode.num_hrs/8

		#td_Days = datetime.timedelta(hours=num_days*24)

		#tmpDtEnd = tmpDtStart + td_Days

		effortHrs = tasknode.num_hrs

		while effortHrs > 0:

			tmpAllotedHrs = getAvailableHrsFor(tmpDtCurr)

			if tmpAllotedHrs > 0 :

				if None == tmpDtStart:
					tmpDtStart = tmpDtCurr

				effortHrs = effortHrs - tmpAllotedHrs

			tmpDtCurr = tmpDtCurr + tdDay

		tmpDtEnd = tmpDtCurr

		tasknode.start_date = tmpDtStart

		tasknode.end_date = tmpDtEnd

		print("[", tmpDtStart.strftime("%d-%m-%Y"), " to ", tmpDtEnd.strftime("%d-%m-%Y"), "]")

		tmpDtStart = None

		tmpDtEnd = None


STYLES = """
.document {
	fill : white; 
}

.frame {  
	stroke : black;
	fill : none;
	opacity: 0.02;
	stroke-width : 1px;	
}

.task {  
	stroke : black;
	fill : #ffcc66;
	opacity: 0.2;
	stroke-width : 2px;	
}

.grid {  
	stroke : black;
	fill : none;
	opacity: 0.01;
	stroke-width : 1px;
	stroke-linecap:square;
}

.gridFine {
	opacity: 0.01;
}

.gridRegular {
	opacity: 0.02;
}

.blueText { 
	background-color : #6699cc;
	font-size : 20px; 
	font-family : Open Sans; 
	font-weight : 300; 
	font-style : normal; 
	fill : blue; 
	stroke : none;
}

.blueText_italic { 
	font-style : italic; 
}
"""

def days_hours_minutes(td):
	return td.days, td.seconds//3600, (td.seconds//60)%60


def renderSVG(oActivityList):

	dwg = svgwrite.Drawing('output.svg', size=("10.2in","5.6in")) # size=(800,480))
	
	dwg.defs.add(dwg.style(STYLES))
	
	#oRectBkg = dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, class_= "document")
	#dwg.add(oRectBkg)
	
	Lw = 1	
	
	###
	
	oRectFrame = dwg.rect(insert=(10 + 0.5*Lw, 10 + 0.5*Lw), size=('800', '480'), rx=None, ry=None, class_= "frame")
	dwg.add(oRectFrame)	
	
	# Verticals
	
	for i in range(20, 800+10, 10):
		Xs = i
		Ys = 10
		Xe = i
		Ye = 480+10
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridFine")
		dwg.add(oLine)			
	
	##
	
	for i in range(60, 800+10, 50):
		Xs = i
		Ys = 10
		Xe = i
		Ye = 15
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridRegular")
		dwg.add(oLine)	
		
	for j in range(60, 480, 50):
		for i in range(60, 800+10, 50):
			Xs = i
			Ys = j-3
			Xe = i
			Ye = j+4
			Lw = 1	
			
			oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridRegular")
			dwg.add(oLine)			
		
	for i in range(60, 800+10, 50):
		Xs = i
		Ys = 475+10
		Xe = i
		Ye = 480+10
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridRegular")
		dwg.add(oLine)	
				
	# Horizontals
	
	for j in range(20, 480+10, 10):
		Xs = 10
		Ys = j
		Xe = 800+10
		Ye = j
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe - 0.5*Lw, Ye + 0.5*Lw), class_= "grid gridFine")
		dwg.add(oLine)			
	
	##
	
	for j in range(60, 480+10, 50):
		Xs = 10
		Ys = j
		Xe = 15
		Ye = j
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe - 0.5*Lw, Ye + 0.5*Lw), class_= "grid gridRegular")
		dwg.add(oLine)	
		
		
	for i in range(60, 800+10, 50):
		for j in range(60, 480+10, 50):
			Xs = i-3
			Ys = j
			Xe = i+4
			Ye = j
			Lw = 1	
			
			oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe - 0.5*Lw, Ye + 0.5*Lw), class_= "grid gridRegular")
			dwg.add(oLine)	
			
	for j in range(60, 480+10, 50):
		Xs = 795+10
		Ys = j
		Xe = 800+10
		Ye = j
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe - 0.5*Lw, Ye + 0.5*Lw), class_= "grid gridRegular")
		dwg.add(oLine)		
	
	'''
	Xs = 60
	Ys = 10
	Xe = 160
	Ye = 120
	Lw = 1				
	
	oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridRegular")
	dwg.add(oLine)	
	'''
	
	sampleText = 'flightplan'
	oText = dwg.text(sampleText, x=[820], y=[30], class_= "blueText blueText_italic")
	dwg.add(oText)

	'''
	oText = dwg.text('800x480', x=[820], y=[90], class_= "blueText")
	dwg.add(oText)
	'''
	
	

	rr_offx = 10 + 50
	rr_offy = 10 + 50 
	rr_w = 50
	rr_h = 20

	prevTask = None
	for tasknode in resolved:

		tdDayWidth = tasknode.end_date - tasknode.start_date
		print(type(tdDayWidth))

		tw = rr_w * tdDayWidth.days
		th = rr_h

		if None != prevTask:
			gapDayWidth = tasknode.start_date - prevTask.end_date 
			gap_x = rr_w * gapDayWidth.days
			#print(gapDayWidth.days)
		else :
			gap_x = 0	
		
		rr_offx = gap_x + rr_offx

		print(gap_x, rr_offx)

		oTmpRect = dwg.rect(insert=(rr_offx + 0.5*Lw, rr_offy + 0.5*Lw), size=(tw, th), rx=5, ry=5, class_= "task")
		dwg.add(oTmpRect)
		
		rr_offx =  rr_offx + tw

		prevTask = tasknode


	dwg.save()

a = tasknode('a')
a.num_hrs = 8

b = tasknode('b')
b.num_hrs = 24

c = tasknode('c')
c.num_hrs = 8

d = tasknode('d')
d.num_hrs = 8

e = tasknode('e')
e.num_hrs = 16

a.addDependency(b)    # a depends on b
a.addDependency(d)    # a depends on d
b.addDependency(c)    # b depends on c
b.addDependency(e)    # b depends on e
c.addDependency(d)    # c depends on d
c.addDependency(e)    # c depends on e
#d.addDependency(b)

resolved = []
unresolved = []
errorList = []
bSuccess = dep_resolve(a, resolved, unresolved, errorList)
if False == bSuccess:
	print('Dependency resolution unsuccessful! Check Data!!')
	
	print('resolved :')
	for tasknode in resolved:
		print(tasknode.name, end=':')
	print()		
	
	print('unresolved :')
	for tasknode in unresolved:
		print(tasknode.name, end=':')
	print()

	print('errorList :')
	for item in errorList:
		print(item, end='')
	print()
		
else:
	print('Dependency resolution successful!!!')

	for tasknode in resolved:
		print(tasknode.name, end=':')

	print()

	print('Considering holiday on ', h1.strftime("%d-%m-%Y"))

	dtCommence = datetime.datetime.fromisoformat('2020-11-15')
	planEffort(resolved, dtCommence)

	renderSVG(resolved)


'''
from openpyxl import load_workbook

wb = load_workbook(filename = 'sampleinput/m1.xlsx')

ws = wb['tasksheet']

print(ws['B4'].value)
'''



'''
if __name__ == '__main__':
	dwg = svgwrite.Drawing('output.svg', size=("10.2in","5.6in")) # size=(800,480))
	
	dwg.defs.add(dwg.style(STYLES))
	
	#oRectBkg = dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, class_= "document")
	#dwg.add(oRectBkg)
	
	Lw = 1	
	
	###
	
	oRectFrame = dwg.rect(insert=(10 + 0.5*Lw, 10 + 0.5*Lw), size=('800', '480'), rx=None, ry=None, class_= "frame")
	dwg.add(oRectFrame)	
	
	# Verticals
	
	for i in range(20, 800+10, 10):
		Xs = i
		Ys = 10
		Xe = i
		Ye = 480+10
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridFine")
		dwg.add(oLine)			
	
	##
	
	for i in range(60, 800+10, 50):
		Xs = i
		Ys = 10
		Xe = i
		Ye = 15
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridRegular")
		dwg.add(oLine)	
		
	for j in range(60, 480, 50):
		for i in range(60, 800+10, 50):
			Xs = i
			Ys = j-3
			Xe = i
			Ye = j+4
			Lw = 1	
			
			oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridRegular")
			dwg.add(oLine)			
		
	for i in range(60, 800+10, 50):
		Xs = i
		Ys = 475+10
		Xe = i
		Ye = 480+10
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridRegular")
		dwg.add(oLine)	
				
	# Horizontals
	
	for j in range(20, 480+10, 10):
		Xs = 10
		Ys = j
		Xe = 800+10
		Ye = j
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe - 0.5*Lw, Ye + 0.5*Lw), class_= "grid gridFine")
		dwg.add(oLine)			
	
	##
	
	for j in range(60, 480+10, 50):
		Xs = 10
		Ys = j
		Xe = 15
		Ye = j
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe - 0.5*Lw, Ye + 0.5*Lw), class_= "grid gridRegular")
		dwg.add(oLine)	
		
		
	for i in range(60, 800+10, 50):
		for j in range(60, 480+10, 50):
			Xs = i-3
			Ys = j
			Xe = i+4
			Ye = j
			Lw = 1	
			
			oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe - 0.5*Lw, Ye + 0.5*Lw), class_= "grid gridRegular")
			dwg.add(oLine)	
			
	for j in range(60, 480+10, 50):
		Xs = 795+10
		Ys = j
		Xe = 800+10
		Ye = j
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe - 0.5*Lw, Ye + 0.5*Lw), class_= "grid gridRegular")
		dwg.add(oLine)		
	
	
	Xs = 60
	Ys = 10
	Xe = 160
	Ye = 120
	Lw = 1				
	
	oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridRegular")
	dwg.add(oLine)	
	
	
	sampleText = 'DopeSheet'
	oText = dwg.text(sampleText, x=[820], y=[30], class_= "blueText blueText_italic")
	dwg.add(oText)

	oText = dwg.text('800x480', x=[820], y=[90], class_= "blueText")
	dwg.add(oText)
	
	dwg.save()
'''


