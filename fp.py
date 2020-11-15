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

calendar_start_date = None
today_date = None
weekendList = None
holidayList = None
eventList = None
milestoneList = None

leavePlan = None

class daterange:
	pass

class track:
	def __init__(self, name):
		self.name = name
		self.offy = 0

class tasknode:

	def __init__(self, name, desc, bCritical=False, bComplete=False, track=None):
		self.name = name
		self.desc = desc
		self.dependencies = []
		self.start_date = None
		self.end_date = None
		self.num_hrs = 8
		self.bCritical = bCritical
		self.consider_weekend = False
		self.track = track
		self.consider_holiday = False

		self.bComplete = False

		self.bHasDeps = False

	def addDependency(self, tasknode):
		if None == tasknode.track:
			tasknode.track = self.track
		self.dependencies.append(tasknode)

def dep_resolve(tasknode, resolved, unresolved, errorList): 
	bRetVal = True
	
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


def getAvailableHrsFor(dtSample):
	numAvailableHrs = 8

	bDone = False
	#print(dtSample, h1, h1 == dtSample)
	
	if (False == bDone) and (dtSample in weekendList):
		numAvailableHrs = 0
		bDone = True
	
	if (False == bDone) and (dtSample in holidayList):
		numAvailableHrs = 0
		bDone = True
	
	if (False == bDone) and (dtSample in eventList):
		numAvailableHrs = 0
		bDone = True

	if (False == bDone) and (dtSample in leavePlan):
		numAvailableHrs = 0
		bDone = True

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

.weekend {  
	stroke : None;
	fill : #ffeed7;
	opacity: 0.3;
	stroke-width : 1px;	
}

.holiday {  
	stroke : None;
	fill : #d7f4ff;
	opacity: 0.3;
	stroke-width : 1px;	
}

.eventday {  
	stroke : None;
	fill : #f7c3d6;
	opacity: 0.3;
	stroke-width : 1px;	
}

.milestone {  
	stroke : None;
	fill : #f9865b;
	opacity: 0.5;
	stroke-width : 1px;	
}

.leaveplan {  
	stroke : None;
	fill : #e0c4f9;
	opacity: 0.3;
	stroke-width : 1px;	
}

.track {  
	stroke : None;
	fill : #f8efff;
	opacity: 0.4;
	stroke-width : 0px;	
}

.today {  
	stroke : None;
	fill : #8b00ff;
	opacity: 0.5;
	stroke-width : 1px;	
}

.task {  
	stroke : None;
	fill : #eef055;
	opacity: 0.2;
	stroke-width : 2px;	
}

.with_dependencies {  
	fill : #f5f531;
	opacity: 0.4;
}

.critical {  
	stroke : #f56631;
	opacity: 0.3;
}

.complete{  
	stroke : None;
	fill : #daf531;
	opacity: 0.3;
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
	font-size : 10px; 
	font-family : Open Sans; 
	font-weight : 100; 
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

	dr_W = 1900
	dr_H = 1060

	dwg = svgwrite.Drawing('output.svg', size=("1920px","1080px")) # size=(800,480))
	
	dwg.defs.add(dwg.style(STYLES))
	
	#oRectBkg = dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, class_= "document")
	#dwg.add(oRectBkg)
	
	Lw = 1	
	
	###
	
	oRectFrame = dwg.rect(insert=(10 + 0.5*Lw, 10 + 0.5*Lw), size=("1920px","1080px"), rx=None, ry=None, class_= "frame")
	dwg.add(oRectFrame)	
	
	# Verticals
	
	for i in range(20, dr_W+10, 10):
		Xs = i
		Ys = 10
		Xe = i
		Ye = dr_H+10
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridFine")
		dwg.add(oLine)			
	
	##
	
	for i in range(60, dr_W+10, 50):
		Xs = i
		Ys = 10
		Xe = i
		Ye = 15
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridRegular")
		dwg.add(oLine)	
		
	for j in range(60, dr_H, 50):
		for i in range(60, dr_W+10, 50):
			Xs = i
			Ys = j-3
			Xe = i
			Ye = j+4
			Lw = 1	
			
			oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridRegular")
			dwg.add(oLine)			
		
	for i in range(60, dr_W+10, 50):
		Xs = i
		Ys = 475+10
		Xe = i
		Ye = dr_H+10
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe + 0.5*Lw, Ye - 0.5*Lw), class_= "grid gridRegular")
		dwg.add(oLine)	
				
	# Horizontals
	
	for j in range(20, dr_H+10, 10):
		Xs = 10
		Ys = j
		Xe = dr_W+10
		Ye = j
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe - 0.5*Lw, Ye + 0.5*Lw), class_= "grid gridFine")
		dwg.add(oLine)			
	
	##
	
	for j in range(60, dr_H+10, 50):
		Xs = 10
		Ys = j
		Xe = 15
		Ye = j
		Lw = 1	
		
		oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe - 0.5*Lw, Ye + 0.5*Lw), class_= "grid gridRegular")
		dwg.add(oLine)	
		
		
	for i in range(60, dr_W+10, 50):
		for j in range(60, dr_H+10, 50):
			Xs = i-3
			Ys = j
			Xe = i+4
			Ye = j
			Lw = 1	
			
			oLine = dwg.line((Xs + 0.5*Lw, Ys + 0.5*Lw), (Xe - 0.5*Lw, Ye + 0.5*Lw), class_= "grid gridRegular")
			dwg.add(oLine)	
			
	for j in range(60, dr_H+10, 50):
		Xs = 795+10
		Ys = j
		Xe = dr_W+10
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
	
	sampleText = 'Project Plan'
	oText = dwg.text(sampleText, x=[10], y=[10], class_= "blueText blueText_italic")
	dwg.add(oText)

	'''
	oText = dwg.text('dr_Wxdr_H', x=[820], y=[90], class_= "blueText")
	dwg.add(oText)
	'''

	#

	for sampleTrack in trackList:

		hol_offx = 10 
		hol_offy = 10 + sampleTrack.offy
		hol_w = dr_W
		hol_h = 50
		
		oTmpRect = dwg.rect(insert=(hol_offx + 0.5*Lw, hol_offy + 0.5*Lw), size=(hol_w, hol_h), rx=0, ry=0, class_= "track")
		dwg.add(oTmpRect)
		
	#

	for sampleWeekendDay in weekendList:
		
		nMult = sampleWeekendDay - calendar_start_date

		hol_offx = 10 + (nMult.days*50)
		hol_offy = 10
		hol_w = 50
		hol_h = dr_H
		
		oTmpRect = dwg.rect(insert=(hol_offx + 0.5*Lw, hol_offy + 0.5*Lw), size=(hol_w, hol_h), rx=0, ry=0, class_= "weekend")
		dwg.add(oTmpRect)

	#

	for sampleDay in holidayList:
		
		nMult = sampleDay - calendar_start_date

		hol_offx = 10 + (nMult.days*50)
		hol_offy = 10
		hol_w = 50
		hol_h = dr_H
		
		oTmpRect = dwg.rect(insert=(hol_offx + 0.5*Lw, hol_offy + 0.5*Lw), size=(hol_w, hol_h), rx=0, ry=0, class_= "holiday")
		dwg.add(oTmpRect)

	#

	for sampleDay in eventList:
		
		nMult = sampleDay - calendar_start_date

		hol_offx = 10 + (nMult.days*50)
		hol_offy = 10
		hol_w = 50
		hol_h = dr_H
		
		oTmpRect = dwg.rect(insert=(hol_offx + 0.5*Lw, hol_offy + 0.5*Lw), size=(hol_w, hol_h), rx=0, ry=0, class_= "eventday")
		dwg.add(oTmpRect)

	#

	for sampleDay in milestoneList:
		
		nMult = sampleDay - calendar_start_date

		hol_offx = 10 + (nMult.days*50) - 2
		hol_offy = 10
		hol_w = 4
		hol_h = dr_H
		
		oTmpRect = dwg.rect(insert=(hol_offx + 0.5*Lw, hol_offy + 0.5*Lw), size=(hol_w, hol_h), rx=0, ry=0, class_= "milestone")
		dwg.add(oTmpRect)

	#

	for sampleDay in leavePlan:
		
		nMult = sampleDay - calendar_start_date

		hol_offx = 10 + (nMult.days*50)
		hol_offy = 10
		hol_w = 50
		hol_h = dr_H
		
		oTmpRect = dwg.rect(insert=(hol_offx + 0.5*Lw, hol_offy + 0.5*Lw), size=(hol_w, hol_h), rx=0, ry=0, class_= "leaveplan")
		dwg.add(oTmpRect)

	#

	nMult = today_date - calendar_start_date

	hol_offx = 10 + (nMult.days*50) - 2
	hol_offy = 10
	hol_w = 4
	hol_h = dr_H
	
	oTmpRect = dwg.rect(insert=(hol_offx + 0.5*Lw, hol_offy + 0.5*Lw), size=(hol_w, hol_h), rx=0, ry=0, class_= "today")
	dwg.add(oTmpRect)

	#

	rr_offx = 10 
	rr_offy = 10
	rr_w = 50
	rr_h = 20

	prevTask_end_date = calendar_start_date
	for tasknode in resolved:

		print(tasknode.name)
		rr_offy = 10 + tasknode.track.offy + 10

		tdDayWidth = tasknode.end_date - tasknode.start_date
		print(type(tdDayWidth))

		tw = rr_w * tdDayWidth.days - 3
		th = rr_h - 3

		gapDayWidth = tasknode.start_date - prevTask_end_date 
		gap_x = rr_w * gapDayWidth.days
		#print(gapDayWidth.days)	
		
		rr_offx = gap_x + rr_offx

		print(gapDayWidth.days, gap_x, rr_offx)

		strClass = "task"
		if True == tasknode.bHasDeps:
			strClass = strClass + " " + "with_dependencies"
		if True == tasknode.bCritical:
			strClass = strClass + " " + "critical"
		if True == tasknode.bComplete:
			strClass = strClass + " " + "complete"

		oTmpRect = dwg.rect(insert=(rr_offx + 2*Lw, rr_offy + 2*Lw), size=(tw, th), rx=2, ry=2, class_= strClass)
		oTmpRect.set_desc(tasknode.desc, tasknode.desc)
		dwg.add(oTmpRect)

		en_x = rr_offx + 10
		en_y = rr_offy + 13
		oText = dwg.text(tasknode.name, x=[en_x], y=[en_y], class_= "blueText blueText_italic")
		dwg.add(oText)
		
		rr_offx =  rr_offx + tw + 3

		prevTask_end_date = tasknode.end_date


	dwg.save()

calendar_start_date = datetime.datetime.fromisoformat('2020-11-12')
today_date = datetime.datetime.fromisoformat('2020-11-18')

wSat1 = datetime.datetime.fromisoformat('2020-11-14')
wSun1 = datetime.datetime.fromisoformat('2020-11-15')
wSat2 = datetime.datetime.fromisoformat('2020-11-21')
wSun2 = datetime.datetime.fromisoformat('2020-11-22')
wSat3 = datetime.datetime.fromisoformat('2020-11-28')
wSun3 = datetime.datetime.fromisoformat('2020-11-29')
wSat4 = datetime.datetime.fromisoformat('2020-12-05')
wSun4 = datetime.datetime.fromisoformat('2020-12-06')
wSat5 = datetime.datetime.fromisoformat('2020-12-12')
wSun5 = datetime.datetime.fromisoformat('2020-12-13')
weekendList = []
weekendList.append(wSat1)
weekendList.append(wSun1)
weekendList.append(wSat2)
weekendList.append(wSun2)
weekendList.append(wSat3)
weekendList.append(wSun3)
weekendList.append(wSat4)
weekendList.append(wSun4)
weekendList.append(wSat5)
weekendList.append(wSun5)

hSat1 = datetime.datetime.fromisoformat('2020-11-16')
holidayList = []
holidayList.append(hSat1)

eFri1 = datetime.datetime.fromisoformat('2020-11-20')
eventList = []
eventList.append(eFri1)

mWed1 = datetime.datetime.fromisoformat('2020-11-27')
milestoneList = []
milestoneList.append(mWed1)


eL1 = datetime.datetime.fromisoformat('2020-11-24')
eL2 = datetime.datetime.fromisoformat('2020-12-02')
leavePlan = []
leavePlan.append(eL1)
leavePlan.append(eL2)

##

t1 = track('t1')
t1.offy = 50
t2 = track('t2')
t2.offy = 150
trackList = []
trackList.append(t1)
trackList.append(t2)

##

a1 = tasknode('a1', 'Task A')
a1.num_hrs = 8
a1.track = t1

b1 = tasknode('b1', 'Development Task B', bCritical=True)
b1.num_hrs = 24

c1 = tasknode('c1', 'Task A')
c1.num_hrs = 8

d1 = tasknode('d1', 'Task A')
d1.num_hrs = 8
d1.bComplete = True

e1 = tasknode('e1', 'Task A')
e1.num_hrs = 16
e1.bComplete = True

a1.addDependency(b1)    # a depends on b
a1.addDependency(d1)    # a depends on d
b1.addDependency(c1)    # b depends on c
b1.addDependency(e1)    # b depends on e
c1.addDependency(d1)    # c depends on d
c1.addDependency(e1)    # c depends on e
#d.addDependency(b)

#e1.bHasDeps = True

##

a2 = tasknode('a2', 'Task A')
a2.num_hrs = 8
a2.track = t2

b2 = tasknode('b2', 'Development Task B', bCritical=True)
b2.num_hrs = 24

c2 = tasknode('c2', 'Task A')
c2.num_hrs = 8

d2 = tasknode('d2', 'Task A')
d2.num_hrs = 8

e2 = tasknode('e2', 'Task A')
e2.num_hrs = 16

a2.addDependency(b2)    # a depends on b
a2.addDependency(d2)    # a depends on d
b2.addDependency(c2)    # b depends on c
b2.addDependency(e2)    # b depends on e
c2.addDependency(d2)    # c depends on d
c2.addDependency(e2)    # c depends on e
d2.addDependency(c1)

#e2.bHasDeps = True

##

resolved = []
unresolved = []
errorList = []

bSuccess_a1 = dep_resolve(a1, resolved, unresolved, errorList)
bSuccess_a2 = dep_resolve(a2, resolved, unresolved, errorList)

bSuccess = bSuccess_a1 and bSuccess_a2
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

	print('Considering holiday on :')
	for sampleWeekendDay in weekendList:
		print(sampleWeekendDay.strftime("%d-%m-%Y"))
	

	dtCommence = datetime.datetime.fromisoformat(calendar_start_date.isoformat())
	planEffort(resolved, dtCommence)

	renderSVG(resolved)


'''
from openpyxl import load_workbook

wb = load_workbook(filename = 'sampleinput/m1.xlsx')

ws = wb['tasksheet']

print(ws['B4'].value)
'''



