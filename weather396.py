# weather: get the weather on the CLI
#
# Copyright (C) ja4e, Eason Qin, 2024.
#
# This source code form is licensed under the MIT/expat license. This program is provided
# on an AS IS BASIS with NO implications or expression of warranty. Please visit the
# OSI website for a full text of the license. 
#

import math
import os
import subprocess
import sys
import warnings
from tabulate import tabulate
import time

def converter(INPUT):
	SUM = 0
	for i in range(len(INPUT)):
		DIGIT = int(INPUT[i])
		if DIGIT not in (0, 1):
			print("Not a binary digit")
			return -1
		else:
			SUM = SUM * 2 + DIGIT
	return SUM

def d2bconverter(INPUT):
	SUM = 0
	COUNTER = 0
	for i in range(len(INPUT)):
		DIGIT = int(INPUT[i])
		if DIGIT not in (0, 1):
			print("Not a binary digit")
			return -1
		else:
			SUM = SUM + DIGIT
			COUNTER += 1
	SUM = COUNTER + SUM
	SUM = SUM / 2
	return SUM

def friction():
	try:
		A = float(input("GIVE (p=u/s): "))
		B = input("MASS(KG) OR N: ")
		if B == "MASS" or B == "1":
			NUM = float(input("input: "))
			N = 9.81 * NUM
		elif B == "N" or B == "2":
			N = float(input("input: "))
			NUM = N / 9.81
		F2 = N * A
		C = input("NEED ACCELERATION? ").upper()
		if C == "YES" or C == "1":
			E = float(input("GIVE (p=u/k): "))
			K2 = 0
			F = E * N
			K2 = A - F
			print("formula: F=ma")
			print("Using: a=F/A")
			ACCEL = N / NUM
			print("F(S): ", ACCEL, "N")
		else:
			print("Accleration not calculated")
		print("F(F): ", F2, "N")
	except TypeError or ValueError:
		print("try again")
	except SyntaxError:
		print("Syntax error (program fault)")

def momentum(): #working on it
	try:
		print("ok")
	except:
		print('not don')

def notequal(SUM):
	if SUM != -1:
		print(SUM)

def Fun():
	try:
		print("nothing is selected")		
	except ValueError or TypeError:
		print("try again")
	except SyntaxError:
		print("Error system quitting")

def Geometric(): #working on it
	print("How many rows and columns? ")
	PTABLE=prettytable()
	ROW=input("ROW(S): ")
	COL=input("COLUMN(S): ")
	TABLE=[]
	for d in COL:
		PTABLE.add_column(columns[0], i+1)
		for i in ROW:
			a=int(input())
			PTABLE.add_row(columns[d+1], a)
		
	
def Statistic(): #working on it
	a = input("ok")
	
def clear():
		time.sleep(5)
		clear()

def open_terminal():
	if sys.platform == 'win32':
		subprocess.Popen('start', shell=True)
		warnings.filterwarnings("ignore")
	elif sys.platform == 'Darwin':
		subprocess.Popen('open -a Terminal .', shell=True)
		warnings.filterwarnings("ignore")
	else:
		try:
			a=input("kitty or gnome: ").upper()
			if a in ("KITTY", "1"):
				My_Cmmnd="cmatrix"
				#subprocess.Popen('kitty', shell=True)
				os.system("kitty -e "+My_Cmmnd)
				warnings.filterwarnings("ignore")
			elif a in ("GNOME", "2"):
				My_Cmmnd="cmatrix"			
				#subprocess.Popen('gnome-terminal', shell=True)
				os.system("gnome-terminal -e 'bash -c \"" + My_Cmmnd + ";bash\"'")
				warnings.filterwarnings("ignore")
		except:
			print("Unsupported platform")
			sys.exit(1)

def main():
	while True:
		try:
			b = input("Computer Science, Physics or Math: ").upper()
			if b in ("COMPUTER SCIENCE", "CP","1","COMPUTER"):
				a = input("binary or denary: ").upper()
				if a == "BINARY" or a == "1":	
					INPUT = input("Input binary number: ")
					SUM = converter(INPUT)
					notequal(SUM)
				elif a == "DENARY" or a == "2":
					INPUT = input("Input denary: ")
					SUM = d2bconverter(INPUT)
					notequal(SUM)
			elif b in ("PHYSICS","2","P","PHYSIC"):
				a = input("FRICTION or idk: ").upper()
				if a == "FRICTION" or a == "1": 
					friction()
			elif b in ("MATH", "3", "M"):
				a = input("Calculate Geometric seq and series or Statistic: ").upper()
				if a == "1" or a == "GEOMETRIC" or a == "G" or a=="GEOMETRIC SEQ":
					print("Function required, not done yet")
					exit()
					Geometric()
				elif a=="2" or a=="STATISTIC" or a =="S":
					print("Function required, not done yet")
					exit()
					Statistic()
			elif b in ("FUN"): #easter egg
				open_terminal()
			elif b in ("CLEAR", "CLR"):
				os.system('clear')
			else:
				print("try again")
			clear()
			
		except ValueError or TypeError:
			print("Try again.")
			
		except KeyboardInterrupt:
			print("ancelled")
			os.system('clear')
			break


if __name__ == "__main__":
	os.system('clear')
	main()
