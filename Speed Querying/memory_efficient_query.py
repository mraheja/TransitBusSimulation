import os
from os import path
import datetime
import sys

DATA_PATH = '../Data/Speed Data/Mesh/'

month, day, hour = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

start = datetime.datetime(2019,month,day,hour,0)
dt_hour = datetime.timedelta(minutes=60)

get_repr = lambda start:str(start.month) + "_" + str(start.day) + "_" + str(start.hour)
get_path = lambda start: DATA_PATH + get_repr(start) + '.shp'

while True:
    if not path.exists(get_path(start)):
        os.system('python3 query.py ' + str(start.month) + ' ' + str(start.day) + ' ' + str(start.hour))
        start += dt_hour