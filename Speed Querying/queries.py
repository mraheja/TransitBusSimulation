import os
import datetime
from os import path as PATH
import time
import json

download = lambda path: os.popen('aws s3 cp "'+ path + '" "./AWS_Waze_Data"')
to_name = lambda t: '%.2d' % t.day + "_" + '%.2d' % t.hour + "_" + '%.2d' % t.minute + ".json"
to_waze = lambda t,name: "s3://wzmx2019/" + str(t.year) + "/" + '%.2d' % t.month + "/" + name
computer_path =  lambda name: 'AWS_Waze_Data\\' + name
delete = lambda computer_path: os.popen('del ' + computer_path)

dt = datetime.timedelta(minutes=1)

def query(start,end,verbose = True):
	t = start
	data = []

	while t < end:
		t += dt
		name = to_name(t)
		path = to_waze(t,name)

		download(path)
		if verbose:
			print(path)
		
		while not PATH.exists(computer_path(name)):
			time.sleep(0.5)
		with open(computer_path(name)) as f:
			data.append(json.load(f))
		
		delete(computer_path(name))

	return data

def speed_query(start,end,verbose = True):
	t = start
	data = []
	
	cur_paths = []
	del_paths = []

	while t < end:
		
		name = to_name(t)
		path = to_waze(t,name)
		download(path)
		
		t += dt
		
		
			
		cur_paths.append(path)
		del_paths.append(computer_path(name))
		
		if len(cur_paths) == 20 or t == end:
			for path in cur_paths:
				while not PATH.exists(computer_path(name)):
					time.sleep(0.5)
				if verbose:
					print(path)
				with open(computer_path(name)) as f:
					data.append(json.load(f))
			for path in del_paths:
				delete(path)
			cur_paths, del_paths = [], []
		
		

	return data

def optimized_query(start,end,verbose = True):
	t = start
	data = []
	
	cur_paths = []
	del_paths = []

	downloads = set()

	while t < end:
		
		to_name_without_hour = lambda t: '%.2d' % t.day


		download = lambda path,name_without_hour: os.popen('aws s3 cp "'+ path + '" "./AWS_Waze_Data" --recursive --exclude "*" --include "' + name_without_hour +'*"')
		download_print = lambda path,name_without_hour: print('aws s3 cp "'+ path + '" "./AWS_Waze_Data" --recursive --exclude "*" --include "' + name_without_hour +'*"')
		

		name = to_name(t)
		path = to_waze(t,name)
		path_download = to_waze(t,"")
		name_without_hour = to_name_without_hour(t)

		if not path_download in downloads:
			download(path_download,name_without_hour)
			#download_print(path_download,name_without_hour)
		
		t += dt
		
		
			
		cur_paths.append(path)
		del_paths.append(computer_path(name))
		
		if len(cur_paths) == 20 or t == end:
			for path in cur_paths:
				while not PATH.exists(computer_path(name)):
					time.sleep(0.5)
				if verbose:
					print(path)
				with open(computer_path(name)) as f:
					data.append(json.load(f))
			for path in del_paths:
				delete(path)
			cur_paths, del_paths = [], []
		
		

	return data