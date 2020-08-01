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
import datetime
from enum import Enum, unique
import json
import logging
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

class Node:
	def __init__(self, name):
		self.name = name
		self.edges = []

	def addEdge(self, node):
		self.edges.append(node)
		
def dep_resolve(node, resolved):
	#  print(node.name)
	
	for edge in node.edges:
		if edge not in resolved:
			dep_resolve(edge, resolved)
	
	resolved.append(node)

'''
a = Node('a')
b = Node('b')
c = Node('c')
d = Node('d')
e = Node('e')

a.addEdge(b)    # a depends on b
a.addEdge(d)    # a depends on d
b.addEdge(c)    # b depends on c
b.addEdge(e)    # b depends on e
c.addEdge(d)    # c depends on d
c.addEdge(e)    # c depends on e

resolved = []
dep_resolve(a, resolved)

for node in resolved:
	print(node.name, end=':')

print()
'''

from openpyxl import load_workbook

wb = load_workbook(filename = 'sampleinput/m1.xlsx')

ws = wb['tasksheet']

print(ws['B4'].value)


