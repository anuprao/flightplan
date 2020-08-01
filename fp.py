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
		self.no_of_days = 1
		self.no_of_hrs = 8
		self.is_critical = False
		self.consider_weekend = False
		self.consider_holiday = False

		self.is_complete = False

	def addDependency(self, tasknode):
		self.dependencies.append(tasknode)
		
def dep_resolve(tasknode, resolved):
	#  print(tasknode.name)
	
	for edge in tasknode.dependencies:
		if edge not in resolved:
			dep_resolve(edge, resolved)
	
	resolved.append(tasknode)

class srcinput:
	
	def checkDuplicateIds():
		pass

	def autoPrefixIds():
		pass

	def addTrack():
		pass

	def addTaskToTrack()
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

	def setStartDate()
		pass

	def excludeWeekends()
		pass

	def excludeHolidays()
		pass

	def checkMilestones()
		pass

	def generate():
		# Identify node ends 
		# Identify node starts
		pass

	def render():
		pass
	
class ganttsvg:

	def renderTask:
		# Without dependencies, colour: yellow
		# With dependencies, colour: light yellow
		# With 'critical' flag, colour: red boundary
		# With 'consider weekend' flag, colour: orange1 boundary
		# With 'consider holiday' flag, colour: orange2 boundary
		# With 'is_complete' flag, colour: blue
		pass

	def renderCurrDateLine:
		pass

	def renderWeekends:
		pass

	def renderHolidays:
		pass
	
	def renderMilestones:
		pass

	def renderTracks:
		pass

	def renderDateRanges:
		pass

	def render():
		pass

class ganttpng:

	def render():
		pass
	
'''
a = tasknode('a')
b = tasknode('b')
c = tasknode('c')
d = tasknode('d')
e = tasknode('e')

a.addEdge(b)    # a depends on b
a.addEdge(d)    # a depends on d
b.addEdge(c)    # b depends on c
b.addEdge(e)    # b depends on e
c.addEdge(d)    # c depends on d
c.addEdge(e)    # c depends on e

resolved = []
dep_resolve(a, resolved)

for tasknode in resolved:
	print(tasknode.name, end=':')

print()
'''

'''
from openpyxl import load_workbook

wb = load_workbook(filename = 'sampleinput/m1.xlsx')

ws = wb['tasksheet']

print(ws['B4'].value)
'''


STYLES_0 = """
.document {
	fill : white; 
}

.frame {  
	stroke : black;
	fill : none;
	opacity: 0.15;
	stroke-width : 1px;	
}

.grid {  
	stroke : black;
	fill : none;
	stroke-linecap:square;
}

.gridFine {
	stroke-width : 1px;
	opacity: 0.05;
}

.gridRegular {
	stroke-width : 1px;
	opacity: 0.1;
}

.blueText { 
	background-color : #6699cc;
	font-size : 20px; 
	font-family : Open Sans; 
	font-weight : 300; 
	font-style : normal; 
	fill : black; 
	stroke : none;
}
"""

STYLES = """
.document {
	fill : white; 
}

.frame {  
	stroke : black;
	fill : none;
	opacity: 0.2;
	stroke-width : 1px;	
}

.grid {  
	stroke : black;
	fill : none;
	stroke-width : 1px;
	stroke-linecap:square;
}

.gridFine {
	opacity: 0.1;
}

.gridRegular {
	opacity: 0.2;
}

.blueText { 
	background-color : #6699cc;
	font-size : 20px; 
	font-family : Open Sans; 
	font-weight : 300; 
	font-style : normal; 
	fill : black; 
	stroke : none;
}

.blueText_italic { 
	font-style : italic; 
}

"""

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



