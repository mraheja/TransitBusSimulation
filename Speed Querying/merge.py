import numpy as np
import datetime
import os
import utils
import geopandas as gpd

DATA_PATH = '../Data/Speed Data/Mesh/'
DEST_PATH = '../Data/Speed Data/Merged/'

dt_UTC = datetime.timedelta(hours=-5)

### BUCKETS ###

get_time = lambda month, day: datetime.datetime(2019,month,day)

bucket_1 = [(get_time(12,1),get_time(1,1)),(get_time(1,1),get_time(3,1))]
bucket_2 = [(get_time(3,1),get_time(7,1))]
bucket_3 = [(get_time(7,1),get_time(9,1))]
bucket_4 = [(get_time(9,1),get_time(12,1))]

buckets = [bucket_1, bucket_2, bucket_3, bucket_4]

hour_bucket_1 = [(6, 10)]
hour_bucket_2 = [(17, 21)]
hour_bucket_3 = [(10,16)]

hour_buckets = [hour_bucket_1, hour_bucket_2, hour_bucket_3]

data_paths = np.zeros((len(buckets),len(hour_buckets)),dtype=list)
for i in range(len(data_paths)):
    for j in range(len(data_paths[0])):
        data_paths[i,j] = []

### get_bucket: returns the indexes of which bucket a time belongs in###

def get_bucket(month, day, hour):
    
    #Convert to UTC
    cur_time = datetime.datetime(2019,month,day,hour)
    cur_time += dt_UTC
    
    idx_1, idx_2 = -1,-1
    
    for idx, bucket in enumerate(buckets):
        for period in bucket:
            if period[0] <= cur_time and cur_time < period[1]:
                idx_1 = idx 
                break
                
    for idx, hour_bucket in enumerate(hour_buckets):
        for period in hour_bucket:
            if period[0] <= cur_time.hour and cur_time.hour < period[1]:
                idx_2 = idx 
                break
                
    return idx_1, idx_2 

for path in os.listdir(DATA_PATH):
    if ".shp" not in path:
        continue
    
    temp = path.replace(".shp","").split("_")
    month, day, hour = int(temp[0]), int(temp[1]), int(temp[2])
    
    idx_1, idx_2 = get_bucket(month, day, hour)
    
    
    data_paths[idx_1][idx_2].append(DATA_PATH + path)

print(data_paths)

for i in range(len(data_paths)):
    for j in range(len(data_paths[0])):
        dfs = [gpd.read_file(path) for path in data_paths[i][j]]
        merged = utils.merge_mesh(dfs,path = DEST_PATH + str(i) + "_" + str(j) + ".shp")

