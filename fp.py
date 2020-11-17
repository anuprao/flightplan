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
from collections import OrderedDict 
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
weekendList = None
holidayList = None
eventList = None
leaveList = None

milestoneList = None

class weekday:
	def __init__(self, strDtStart):
		self.dtStart = datetime.datetime.fromisoformat(strDtStart)
		self.strDesc = "Weekday"

		self.bWeekend = False
		self.strDesc_Weekend = ""

		self.bHoliday = False
		self.strDesc_Holiday = ""

		self.bEvent = False
		self.strDesc_Event = ""

		self.bLeave = False
		self.strDesc_Leave = ""

		self.bMilestone = False
		self.strDesc_Milestone = ""

		self.width = None
		self.strClass = None

	def setup(self):
		pass

	def strftime(self, stFormat):
		return self.dtStart.strftime(stFormat)

	def __eq__(self, other):
			if isinstance(other, datetime.datetime):
				if self.dtStart == other:
					return True
				else:
					return False
			else:
				return False


class document:
	def __init__(self):
		self.SW = 1920
		self.SH = 1080

		self.margin = 10
		self.marginx = self.margin
		self.marginy = self.margin

		self.project_title_height = 10
		self.project_title_offy = 4

		self.dr_W = self.SW - 2*self.margin
		self.dr_H = self.SH - 2*self.margin - self.project_title_height

		self.ca_offx = self.marginx
		self.ca_offy = self.marginy + self.project_title_height

		self.gridx_fine = 10
		self.gridy_fine = 10

		self.gridx_reg = 50
		self.gridy_reg = 50

		self.crosshair_len_x = 10
		self.crosshair_len_y = 10
		self.crosshair_len_x_by_2 = self.crosshair_len_x /2
		self.crosshair_len_y_by_2 = self.crosshair_len_y /2

		self.Lw = 1	

		self.dwg = None

	def prepSVG(self, fnSVG, strDocTitle):
		fnCSS = open('fp.css', 'r')
		strCSS = fnCSS.read()
		fnCSS.close()

		self.strDocTitle = strDocTitle

		self.dwg = svgwrite.Drawing(fnSVG, size=(str(self.SW) + "px", str(self.SH) + "px")) # size=(800,480))
		self.dwg.defs.add(self.dwg.style(strCSS))

	def drawGrid(self):

		oText = self.dwg.text(self.strDocTitle, x=[self.marginx], y=[self.marginy + self.project_title_offy], class_= "projectTitle")
		self.dwg.add(oText)

		#
		
		oRectFrame = self.dwg.rect(insert=(self.ca_offx + 0.5*self.Lw, self.ca_offy + 0.5*self.Lw), size=(str(self.dr_W) + "px", str(self.dr_H) + "px"), rx=None, ry=None, class_= "frame")
		self.dwg.add(oRectFrame)	
		
		# Verticals
		
		for i in range(self.ca_offx + self.gridx_fine, self.ca_offx + self.dr_W, self.gridx_fine):
			Xs = i
			Ys = self.ca_offy 
			Xe = i
			Ye = self.ca_offy + self.dr_H
			self.Lw = 1	
			
			oLine = self.dwg.line((Xs + 0.5*self.Lw, Ys + 0.5*self.Lw), (Xe + 0.5*self.Lw, Ye - 0.5*self.Lw), class_= "grid gridFine")
			self.dwg.add(oLine)			
		
		##
		
		for i in range(self.ca_offx + self.gridx_reg, self.ca_offx + self.dr_W, self.gridx_reg):
			Xs = i
			Ys = self.ca_offy
			Xe = i
			Ye = self.ca_offy + self.crosshair_len_y_by_2
			self.Lw = 1	
			
			oLine = self.dwg.line((Xs + 0.5*self.Lw, Ys + 0.5*self.Lw), (Xe + 0.5*self.Lw, Ye - 0.5*self.Lw), class_= "grid gridRegular")
			self.dwg.add(oLine)	
		
		
		for j in range(self.ca_offy + self.gridy_reg, self.ca_offy + self.dr_H, self.gridy_reg):
			for i in range(self.ca_offx + self.gridx_reg, self.ca_offx + self.dr_W, self.gridx_reg):
				Xs = i
				Ys = j - self.crosshair_len_y_by_2 + 2
				Xe = i
				Ye = j + self.crosshair_len_y_by_2 - 1
				self.Lw = 1	
				
				oLine = self.dwg.line((Xs + 0.5*self.Lw, Ys + 0.5*self.Lw), (Xe + 0.5*self.Lw, Ye - 0.5*self.Lw), class_= "grid gridRegular")
				self.dwg.add(oLine)			
		
		for i in range(self.ca_offx + self.gridx_reg, self.ca_offx + self.dr_W, self.gridx_reg):
			Xs = i
			Ys = self.ca_offy + self.dr_H - self.crosshair_len_y_by_2
			Xe = i
			Ye = self.ca_offy + self.dr_H
			self.Lw = 1	
			
			oLine = self.dwg.line((Xs + 0.5*self.Lw, Ys + 0.5*self.Lw), (Xe + 0.5*self.Lw, Ye - 0.5*self.Lw), class_= "grid gridRegular")
			self.dwg.add(oLine)
					
		# Horizontals
		
		for j in range(self.ca_offy + self.gridy_fine, self.ca_offy + self.dr_H, self.gridy_fine):
			Xs = self.ca_offx
			Ys = j
			Xe = self.ca_offx + self.dr_W
			Ye = j
			self.Lw = 1	
			
			oLine = self.dwg.line((Xs + 0.5*self.Lw, Ys + 0.5*self.Lw), (Xe - 0.5*self.Lw, Ye + 0.5*self.Lw), class_= "grid gridFine")
			self.dwg.add(oLine)			
		
		##
		
		for j in range(self.ca_offy + self.gridy_reg, self.ca_offy + self.dr_H, self.gridy_reg):
			Xs = self.ca_offx
			Ys = j
			Xe = self.ca_offx + self.crosshair_len_x_by_2
			Ye = j
			self.Lw = 1	
			
			oLine = self.dwg.line((Xs + 0.5*self.Lw, Ys + 0.5*self.Lw), (Xe - 0.5*self.Lw, Ye + 0.5*self.Lw), class_= "grid gridRegular")
			self.dwg.add(oLine)	
		
		for i in range(self.ca_offx + self.gridx_reg, self.ca_offx + self.dr_W, self.gridx_reg):
			for j in range(self.ca_offy + self.gridy_reg, self.ca_offy + self.dr_H, self.gridy_reg):
				Xs = i - self.crosshair_len_x_by_2 + 2
				Ys = j
				Xe = i + self.crosshair_len_x_by_2 - 1
				Ye = j
				self.Lw = 1	
				
				oLine = self.dwg.line((Xs + 0.5*self.Lw, Ys + 0.5*self.Lw), (Xe - 0.5*self.Lw, Ye + 0.5*self.Lw), class_= "grid gridRegular")
				self.dwg.add(oLine)	
		
		for j in range(self.ca_offy + self.gridy_reg, self.ca_offy + self.dr_H, self.gridy_reg):
			Xs = self.ca_offx + self.dr_W - self.crosshair_len_x_by_2
			Ys = j
			Xe = self.ca_offx + self.dr_W
			Ye = j
			self.Lw = 1	
			
			oLine = self.dwg.line((Xs + 0.5*self.Lw, Ys + 0.5*self.Lw), (Xe - 0.5*self.Lw, Ye + 0.5*self.Lw), class_= "grid gridRegular")
			self.dwg.add(oLine)			

	def drawElements(self):
		pass

	def saveSVG(self):
		self.dwg.save()

	def renderSVG(self, fnSVG, strDocTitle):
		self.prepSVG(fnSVG, strDocTitle)
		self.drawGrid()
		self.drawElements()
		self.saveSVG()

class calendar(document):
	def __init__(self, dtStart, dtEnd, holidayList, eventList, milestoneList, leaveList, tracklist):
		super().__init__()
		self.dtStart = dtStart
		self.dtEnd = dtEnd

		self.holidayList = holidayList
		self.eventList = eventList
		self.milestoneList = milestoneList
		self.leaveList = leaveList
		self.tracklist = tracklist

		self.dtToday = datetime.datetime.today()
		
		self.dictDays = OrderedDict()

		#
		
		self.widthWeekDay = 50
		self.widthWeekendDay = 25
		self.widthWorkDay = 50

		self.widthHoliday = 50
		self.widthEventDay = 50
		self.widthMilestoneMarker = 10
		self.widthTodayMarker = 2

		self.heightTrack = 50
		self.heightTask = 20

		self.margin_task_x = 3
		self.margin_task_y = 3
		self.taskname_offx = 10
		self.taskname_offy = 13
		self.task_roundx = 2
		self.task_roundy = 2

	def isWeekend(self, sampleDay):
		bWeekend = False
		nWeekDay = sampleDay.dtStart.weekday()

		strDesc_Weekend = None
		if 5 == nWeekDay:
			bWeekend = True
			strDesc_Weekend = "Saturday of Week " + str(sampleDay.dtStart.isocalendar()[1])
		elif 6 == nWeekDay:
			bWeekend = True
			strDesc_Weekend = "Sunday of Week " + str(sampleDay.dtStart.isocalendar()[1])

		return (bWeekend, strDesc_Weekend)


	def isHoliday(self, dayName):
		bHoliday = False
		strDesc = None
		iterHoliday = iter(self.holidayList)
		bDone = False
		while(False == bDone):
			oHoliday = next(iterHoliday, None)
			if None == oHoliday:
				bDone = True
			else:
				if dayName == oHoliday[0] :
					strDesc = oHoliday[1]
					bHoliday = True
					bDone = True
		return (bHoliday, strDesc)

	def isEvent(self, dayName):
		bEvent = False
		strDesc = None
		iterEvent = iter(self.eventList)
		bDone = False
		while(False == bDone):
			oEventday = next(iterEvent, None)
			if None == oEventday:
				bDone = True
			else:
				if dayName == oEventday[0] :
					strDesc = oEventday[1]
					bEvent = True
					bDone = True
		return (bEvent, strDesc)

	def isLeave(self, dayName):
		bLeave = False
		strDesc = None
		iterLeave = iter(self.leaveList)
		bDone = False
		while(False == bDone):
			oLeave = next(iterLeave, None)
			if None == oLeave:
				bDone = True
			else:
				if dayName == oLeave[0] :
					strDesc = oLeave[1]
					bLeave = True
					bDone = True
		return (bLeave, strDesc)

	def isMilestone(self, dayName):
		bMilestone = False
		strDesc = None
		iterMilestone = iter(self.milestoneList)
		bDone = False
		while(False == bDone):
			oMilestone = next(iterMilestone, None)
			if None == oMilestone:
				bDone = True
			else:
				if dayName == oMilestone[0] :
					strDesc = oMilestone[1]
					bMilestone = True
					bDone = True
		return (bMilestone, strDesc)

	def initDays(self, dtToday):
		self.dtToday = dtToday
		self.period = self.dtEnd - self.dtStart

		print(Fore.GREEN + 'Generating for ' + Fore.WHITE + str(self.period.days) + Fore.GREEN + ' days!')

		if 0 < self.period.days :

			tdDay = datetime.timedelta(hours=24)

			tmpDay = self.dtStart.replace()
			while self.dtEnd != tmpDay:

				dayName = tmpDay.strftime("%Y-%m-%d")
				#print(dayName)

				oDay = weekday(dayName)

				retWeekend = self.isWeekend(oDay)
				if True == retWeekend[0]:
					oDay.bWeekend = True
					oDay.strDesc_Weekend = retWeekend[1]
				else:
					retHoliday = self.isHoliday(dayName)
					if True == retHoliday[0]:
						oDay.bHoliday = True
						oDay.strDesc_Holiday = retHoliday[1]
					else: 
						retEvent = self.isEvent(dayName)
						if True == retEvent[0]:
							oDay.bEvent = True
							oDay.strDesc_Event = retEvent[1]
						else: 
							retLeave = self.isLeave(dayName)
							if True == retLeave[0]:
								oDay.bLeave = True
								oDay.strDesc_Leave = retLeave[1]
				
				retMilestone = self.isMilestone(dayName)
				if True == retMilestone[0]:
					oDay.bMilestone = True
					oDay.strDesc_Milestone = retMilestone[1]

				self.dictDays[dayName] = oDay

				tmpDay = tmpDay + tdDay

	def setup(self):
		
		offx = self.ca_offx
		for dayName, sampleDay in self.dictDays.items():
			print(dayName, sampleDay.strDesc, sampleDay.strDesc_Weekend, sampleDay.strDesc_Holiday, sampleDay.strDesc_Event, sampleDay.strDesc_Leave, sampleDay.strDesc_Milestone)

			sampleDay.offx = offx
			if True == sampleDay.bWeekend :
				sampleDay.width = self.widthWeekendDay
				sampleDay.strClass = "weekend"
			else:
				if True == sampleDay.bHoliday :
					sampleDay.width = self.widthHoliday
					sampleDay.strClass = "holiday"
				else:
					if True == sampleDay.bEvent :
						sampleDay.width = self.widthEventDay
						sampleDay.strClass = "eventday"
					else:
						if True == sampleDay.bLeave :
							sampleDay.width = self.widthWeekDay
							sampleDay.strClass = "leaveday"
						else:
							sampleDay.width = self.widthWeekDay
							sampleDay.strClass = ""

			offx = offx + sampleDay.width

	
	def drawElements(self):
		'''
		# How to draw a line 
		Xs = self.ca_offx 
		Ys = self.ca_offy 
		Xe = self.ca_offx + 100 
		Ye = self.ca_offy + 100 + 1
		Lw = 1				
		
		oLine = self.dwg.line((Xs + 0.5*self.Lw, Ys + 0.5*self.Lw), (Xe + 0.5*self.Lw, Ye - 0.5*self.Lw), class_= "grid gridRegular")
		self.dwg.add(oLine)	
		'''

		#
		
		for sampleTrack in trackList:

			hol_offx = self.ca_offx 
			hol_offy = self.ca_offy + sampleTrack.offy
			hol_w = self.dr_W
			hol_h = self.heightTrack
			
			oTmpRect = self.dwg.rect(insert=(hol_offx + 0.5*self.Lw, hol_offy + 0.5*self.Lw), size=(hol_w, hol_h), rx=0, ry=0, class_= "track")
			self.dwg.add(oTmpRect)
		
		#

		for dayName, sampleDay in self.dictDays.items():
			hol_offx = sampleDay.offx 
			hol_offy = self.ca_offy
			hol_w = sampleDay.width
			hol_h = self.dr_H
			
			if "" != sampleDay.strClass:
				oTmpRect = self.dwg.rect(insert=(hol_offx + 0.5*self.Lw, hol_offy + 0.5*self.Lw), size=(hol_w, hol_h), rx=0, ry=0, class_= sampleDay.strClass)
				oTmpRect.set_desc(sampleDay.strDesc, sampleDay.strDesc)
				self.dwg.add(oTmpRect)

			if True == sampleDay.bMilestone:
				hol_offx = hol_offx - (self.widthMilestoneMarker/3) - 1
				hol_w = self.widthMilestoneMarker

				oTmpRect = self.dwg.rect(insert=(hol_offx + 0.5*self.Lw, hol_offy + 0.5*self.Lw), size=(hol_w, hol_h), rx=0, ry=0, class_= "milestone")
				oTmpRect.set_desc(sampleDay.strDesc_Milestone, sampleDay.strDesc_Milestone)
				self.dwg.add(oTmpRect)

		nMult = dtToday - self.dtStart

		hol_offx = self.ca_offx + (nMult.days*self.widthWeekDay) - (self.widthTodayMarker/2) 
		hol_offy = self.ca_offy
		hol_w = self.widthTodayMarker
		hol_h = self.dr_H
		
		oTmpRect = self.dwg.rect(insert=(hol_offx + 0.5*self.Lw, hol_offy + 0.5*self.Lw), size=(hol_w, hol_h), rx=0, ry=0, class_= "today")
		oTmpRect.set_desc("Today", "Today")
		self.dwg.add(oTmpRect)

		#

		'''
		prevTask_end_date = self.dtStart

		for sampleTrack in trackList:

			rr_offx = self.ca_offx 
			rr_offy = self.ca_offy

			prevTask_end_date = self.dtStart

			for tasknode in sampleTrack.resolved:

				if False == tasknode.bRendered:

					#print(tasknode.name)
					rr_offy = self.ca_offy + tasknode.track.offy 

					tdDayWidth = tasknode.end_date - tasknode.start_date
					#print(type(tdDayWidth))

					tw = self.widthWorkDay * tdDayWidth.days 
					th = self.heightTask - self.margin_task_y

					gapDayWidth = tasknode.start_date - prevTask_end_date 
					gap_x = self.widthWorkDay * gapDayWidth.days
					#print(gapDayWidth.days)	
					
					rr_offx = gap_x + rr_offx

					#print(gapDayWidth.days, gap_x, rr_offx)

					tw_w_margin = tw - self.margin_task_x

					strClass = "task"
					if True == tasknode.bHasDeps:
						strClass = strClass + " " + "with_dependencies"
					if True == tasknode.bCritical:
						strClass = strClass + " " + "critical"
					if True == tasknode.bComplete:
						strClass = strClass + " " + "complete"

					oTmpRect = self.dwg.rect(insert=(rr_offx + 2*self.Lw, rr_offy + 2*self.Lw), size=(tw_w_margin, th), rx=self.task_roundx, ry=self.task_roundy, class_= strClass)
					oTmpRect.set_desc(tasknode.strDesc, tasknode.strDesc)
					self.dwg.add(oTmpRect)

					en_x = rr_offx + self.taskname_offx
					en_y = rr_offy + self.taskname_offy
					oText = self.dwg.text(tasknode.name, x=[en_x], y=[en_y], class_= "taskname")
					self.dwg.add(oText)
					
					rr_offx =  rr_offx + tw

					prevTask_end_date = tasknode.end_date

					tasknode.bRendered = True
		'''

class calendarMember(calendar):
	def __init__(self, dtStart, dtEnd):
		super().__init__(dtStart, dtEnd)


class holiday:
	def __init__(self, strDtHoliday, strDesc):
		self.dtHoliday = datetime.datetime.fromisoformat(strDtHoliday)
		self.strDesc = strDesc

	def strftime(self, stFormat):
		return self.dtHoliday.strftime(stFormat)
	
	def __eq__(self, other):
			if isinstance(other, datetime.datetime):
				if self.dtHoliday == other:
					return True
				else:
					return False
			else:
				return False

class eventday:
	def __init__(self, strDtEventday, strDesc):
		self.dtEventday = datetime.datetime.fromisoformat(strDtEventday)
		self.strDesc = strDesc

	def strftime(self, stFormat):
		return self.dtEventday.strftime(stFormat)
	
	def __eq__(self, other):
			if isinstance(other, datetime.datetime):
				if self.dtEventday == other:
					return True
				else:
					return False
			else:
				return False

class milestone:
	def __init__(self, strDtMilestoneday, strDesc):
		self.dtMilestoneday = datetime.datetime.fromisoformat(strDtMilestoneday)
		self.strDesc = strDesc

	def strftime(self, stFormat):
		return self.dtMilestoneday.strftime(stFormat)
	
	def __eq__(self, other):
			if isinstance(other, datetime.datetime):
				if self.dtMilestoneday == other:
					return True
				else:
					return False
			else:
				return False

class leave:
	def __init__(self, strDtLeave, strDesc):
		self.dtLeave = datetime.datetime.fromisoformat(strDtLeave)
		self.strDesc = "Leave availed by " + strDesc

	def strftime(self, stFormat):
		return self.dtLeave.strftime(stFormat)
	
	def __eq__(self, other):
			if isinstance(other, datetime.datetime):
				if self.dtLeave == other:
					return True
				else:
					return False
			else:
				return False

class track:
	def __init__(self, name):
		self.name = name
		self.offy = 0
		self.resolved = []
		self.unresolved = []
		self.errorList = []

class tasknode:

	def __init__(self, name, strDesc, bCritical=False, bComplete=False, track=None):
		self.name = name
		self.strDesc = strDesc
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
		self.bTraversed = False
		self.bRendered = False

	def addDependency(self, tasknode):
		if None == tasknode.track:
			tasknode.track = self.track
		self.dependencies.append(tasknode)

def dep_resolve(tasknode, resolved, unresolved, errorList): 
	bRetVal = True
	
	unresolved.append(tasknode)
	
	print(tasknode.name + " tasknode.dependencies " , end=":")
	for samplenode in tasknode.dependencies:
		print(samplenode.name, end=':')
	print()
	
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

	for tasknode in oActivityList:

		#print(tasknode.name)

		if False == tasknode.bTraversed:

			#print("<", tasknode.num_hrs, ">", end=' ')
		
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

			tasknode.bTraversed = True

			#print("[", tmpDtStart.strftime("%d-%m-%Y"), " to ", tmpDtEnd.strftime("%d-%m-%Y"), "]")

			tmpDtStart = None

			tmpDtEnd = None

		else:

			tmpDtCurr = tasknode.end_date


def days_hours_minutes(td):
	return td.days, td.seconds//3600, (td.seconds//60)%60




'''
##

a1 = tasknode('a1', 'Task A')
a1.num_hrs = 8
a1.track = t1

b1 = tasknode('b1', 'Development Task B', bCritical=True)
b1.num_hrs = 24

c1 = tasknode('c1', 'Task C')
c1.num_hrs = 8

d1 = tasknode('d1', 'Task D')
d1.num_hrs = 8
d1.bComplete = True

e1 = tasknode('e1', 'Task E')
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

c2 = tasknode('c2', 'Task C')
c2.num_hrs = 8

d2 = tasknode('d2', 'Task D')
d2.num_hrs = 8

e2 = tasknode('e2', 'Task E')
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

print('-----------------------------------------------------')

print('Considering weekends on :')
for sampleWeekendDay in weekendList:
	print(sampleWeekendDay.strftime("%d-%m-%Y"))

print('Considering holiday on :')
for sampleHoliay in holidayList:
	print(sampleHoliay.strftime("%d-%m-%Y"))

print('Considering events on :')
for sampleEvent in eventList:
	print(sampleEvent.strftime("%d-%m-%Y"))

print('Considering leaves on :')
for sampleLeave in leavePlan:
	print(sampleLeave.strftime("%d-%m-%Y"))

print('-----------------------------------------------------')

bSuccess_a1 = dep_resolve(a1, t1.resolved, t1.unresolved, t1.errorList)
if False == bSuccess_a1:
	print('Dependency resolution unsuccessful! Check Data!!')
	
	print('resolved :')
	for tasknode in t1.resolved:
		print(tasknode.name, end=':')
	print()		
	
	print('unresolved :')
	for tasknode in t1.unresolved:
		print(tasknode.name, end=':')
	print()

	print('errorList :')
	for item in t1.errorList:
		print(item, end='')
	print()
		
else:
	print('Dependency resolution successful!!!')

	for tasknode in t1.resolved:
		print(tasknode.name, end=':')
		#tasknode.bTraversed = True

	print()

	#dtCommence = datetime.datetime.fromisoformat(calendar_start_date.isoformat())
	#planEffort(resolved, dtCommence)

	#renderSVG(resolved)

print('-----------------------------------------------------')

bSuccess_a2 = dep_resolve(a2, t2.resolved, t2.unresolved, t2.errorList)
if False == bSuccess_a2:
	print('Dependency resolution unsuccessful! Check Data!!')
	
	print('resolved :')
	for tasknode in t2.resolved:
		print(tasknode.name, end=':')
	print()		
	
	print('unresolved :')
	for tasknode in t2.unresolved:
		print(tasknode.name, end=':')
	print()

	print('errorList :')
	for item in t2.errorList:
		print(item, end='')
	print()
		
else:
	print('Dependency resolution successful!!!')

	for tasknode in t2.resolved:
		print(tasknode.name, end=':')
		#tasknode.bTraversed = True

	print()

	#dtCommence = datetime.datetime.fromisoformat(calendar_start_date.isoformat())
	#planEffort(resolved, dtCommence)

	#renderSVG(resolved)

print('-----------------------------------------------------')

if bSuccess_a1 and bSuccess_a2:

	dtCommence = datetime.datetime.fromisoformat(calendar_start_date.isoformat())
	for sampleTrack in trackList:
		planEffort(sampleTrack.resolved, dtCommence)

	renderSVG()
'''

'''
from openpyxl import load_workbook

wb = load_workbook(filename = 'sampleinput/m1.xlsx')

ws = wb['tasksheet']

print(ws['B4'].value)
'''

if __name__ == "__main__":

	colorama.init(autoreset=True)

	print(Style.RESET_ALL, end="")
	
	dtStart = datetime.datetime.fromisoformat('2020-11-12')
	dtEnd = datetime.datetime.fromisoformat('2021-01-31')
	dtToday = datetime.datetime.fromisoformat('2020-11-18')

	holidayList = [
		['2020-11-13', 'Deepavali']
	]

	eventList = [
		['2020-11-20', 'Demo Day']
	]

	milestoneList = [
		['2020-11-27', 'Tech1']
	]

	leaveList = [
		['2020-11-16', 'Member1'],
		['2020-11-24', 'Member2'],
		['2020-12-01', 'Member1']
	]

	##

	t1 = track('t1')
	t1.offy = 50
	t2 = track('t2')
	t2.offy = 150
	trackList = []
	trackList.append(t1)
	trackList.append(t2)

	##

	oCal = calendar(dtStart, dtEnd, holidayList, eventList, milestoneList, leaveList, trackList)
	oCal.initDays(dtToday)

	oCal.setup()
	oCal.renderSVG('overall.svg', 'Project plan')

	print(Fore.BLUE + 'Program done !')



