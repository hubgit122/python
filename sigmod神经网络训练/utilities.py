#coding=utf-8
#!/usr/bin/env python
# Filename: utilities.py

#----------------------------------------------------------------------
def getPositiveInt(descriptionStr="in put a positive int"):
	"""得到正整数, 失败后要求再次写入"""
	try:
		temp = int(raw_input(descriptionStr))
	except:
		temp = 0
	while temp <= 0:
		try:
			temp = int(raw_input(descriptionStr))
		except:
			temp = 0
	return temp

#----------------------------------------------------------------------
def getFloat(descriptionStr="in put a float"):
	"""得到浮点数, 失败后得到0"""
	try:
		temp = float(raw_input(descriptionStr))
	except:
		print "error inputing, you get 0.0 instead"
		temp = 0.0
	return temp