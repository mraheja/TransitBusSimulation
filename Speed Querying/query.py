import utils
import queries
import datetime
from os import path
import sys

DEST_PATH = '../Data/Speed Data/Mesh/'

month, day, hour = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

start = datetime.datetime(2019,month,day,hour,0)
end = datetime.datetime(2019,month,day,hour,59)
dt_hour = datetime.timedelta(minutes=60)

get_repr = lambda start:str(start.month) + "_" + str(start.day) + "_" + str(start.hour)
get_path = lambda start: DEST_PATH + get_repr(start) + '.shp'

data = queries.optimized_query(start,end)
df = utils.mesh(data,path=get_path(start))
