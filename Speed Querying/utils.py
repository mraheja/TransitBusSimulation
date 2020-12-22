import bisect
from blist import blist
import numpy as np
import json
import geopandas as gpd
import shapely
import os
import time

old_lt = shapely.geometry.LineString.__lt__
old_eq = shapely.geometry.LineString.__eq__

def lt(self,other):
	
	if self.c.shape[0] < other.c.shape[0]:
		return True
	
	if self.c.shape[0] > other.c.shape[0]:
		return False
	
	ind = np.argmin(self.c == other.c)
	return not self.c[ind] >= other.c[ind]

def eq(self,other):  
	return np.array_equal(other.c,self.c)

def mesh(data,path = False,verbose=True):

	shapely.geometry.LineString.__lt__ = lt
	shapely.geometry.LineString.__eq__ = eq

	result = blist()

	for it in range(len(data)):
		
		t1 = time.time()

		geoms = np.zeros(len(data[it]['jams']),dtype=shapely.geometry.LineString)
		speeds = np.zeros(len(data[it]['jams']))

		for i in range(len(data[it]['jams'])):
			e = data[it]['jams'][i]
			line = e['line']
			speed = e['speed']
			points = np.zeros((len(line),2))
			for j in range(len(line)):
				points[j][0] = line[j]['x']
				points[j][1] = line[j]['y']
			speeds[i] = speed
			geom = shapely.geometry.LineString(points)
			geom.c = points.flatten()
			geoms[i] = geom
			
		t_mid = time.time()
		tot_bis = 0


		for i in range(len(geoms)):
			geom = geoms[i]
			speed = speeds[i]
		   
			t_bis_1 = time.time()
			pos = bisect.bisect(result,[geom,0,0]) 
			t_bis_2 = time.time()
			
			tot_bis += t_bis_2 - t_bis_1
			
			if pos < len(result) and result[pos][0] == geom:
				result[pos][1] = (result[pos][1] * result[pos][2] + speed) / (result[pos][2]+1)
				result[pos][2] += 1
			else:
				result.insert(pos,[geom,speed,1]) 
				
		t2 = time.time()
		
		if verbose:
			print("ITERATION ",str(it+1), " TOOK ",str(t2-t1),"SECONDS")
			print("SECOND HALF",str(t2-t_mid))
			print("BISECT",str(tot_bis))

	df = gpd.GeoDataFrame(result)
	df.columns = ['geometry','speed','num']
	df.crs = 'epsg:4326'

	if path:

		shapely.geometry.LineString.__lt__ = old_lt
		shapely.geometry.LineString.__eq__ = old_eq

		df.set_geometry(col='geometry',inplace=True)
		df.to_file(path)

	return df

def merge_mesh(dfs,path=False,verbose=True):
	shapely.geometry.LineString.__lt__ = lt
	shapely.geometry.LineString.__eq__ = eq

	result = blist()

	for it in range(len(dfs)):
		
		t1 = time.time()

		geoms = dfs[it]['geometry']
		speeds = dfs[it]['speed']
		nums = dfs[it]['num']

		tot_bis = 0
		for i in range(len(geoms)):
			geom = geoms[i]
			geom.c = np.array(geom).flatten()
			speed = speeds[i]
			num = nums[i]
		   
			t_bis_1 = time.time()
			pos = bisect.bisect(result,[geom,0,0]) 
			t_bis_2 = time.time()
			
			tot_bis += t_bis_2 - t_bis_1
			
			if pos < len(result) and result[pos][0] == geom:
				result[pos][1] = (result[pos][1] * result[pos][2] + speed * num) / (result[pos][2]+num)
				result[pos][2] += num
			else:
				result.insert(pos,[geom,speed,num]) 
				
		t2 = time.time()
		
		if verbose:
			print("ITERATION ",str(it+1), " TOOK ",str(t2-t1),"SECONDS")
			print("BISECT",str(tot_bis))
           
	df = gpd.GeoDataFrame(result)
	df.columns = ['geometry','speed','num']
	df.crs = 'epsg:4326'

	if path:
		df = df.copy()

		shapely.geometry.LineString.__lt__ = old_lt
		shapely.geometry.LineString.__eq__ = old_eq

		df.to_file(path)

	return df