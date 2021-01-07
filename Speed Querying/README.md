# Speed Querying

## Overview

Data from Waze traffic montioring is used to generate a profile of average speeds for streets throughout Mexico City. The original data is stored on a one minute resolution. The results are stored in `Data/Speed Data/Merged` with the naming convention `(Month Bucket)_(Hour Bucket).shp` where the monthly and hourly buckets are defined as follows:

#### Month Buckets
* 0: December - February
* 1: March - June
* 2: July - August
* 3: September - Novemeber

#### Hour Buckets
* 0: 6:00 - 10:00
* 1: 17:00 - 21:00
* 2 10:00 - 16:00 

## Usage

`query.py` is used to average minute resolution data into hour resolution data. To support multiprocessing and failures, query can be started using any start time using `python3 query.py (start month) (start day) (start hour)` for example `python3 query.py 3 1 4`.

`merge.py` is used to merge the hour resolution data into overall DataFrames for each (month, hour) bucket pair as specified above.

`utils.py` stores all the helper functions for querying and merging.

## Implementation

The input data is in JSON format. An example of one entry is: 

```
{
   "country":"MX",
   "level":3,
   "line":[
      {
         "x":-99.250158,
         "y":18.971177
      },
      {
         "x":-99.249257,
         "y":18.970578
      },
      {
         "x":-99.248935,
         "y":18.970266
      },
      {
         "x":-99.248737,
         "y":18.969982
      },
      {
         "x":-99.248332,
         "y":18.969267
      },
      {
         "x":-99.247858,
         "y":18.96835
      },
      {
         "x":-99.247777,
         "y":18.968155
      },
      {
         "x":-99.24771,
         "y":18.967986
      },
      {
         "x":-99.247536,
         "y":18.96759
      }
   ],
   "speedKMH":8.68,
   "length":496,
   "turnType":"NONE",
   "type":"NONE",
   "uuid":510424932,
   "endNode":"Cuernanvaca",
   "speed":2.411111111111111,
   "segments":[{}, {}, {}, {}, {}, {}],
   "roadType":6,
   "delay":162,
   "startNode":"Santa Mar\u00eda, Morelos",
   "street":"MEX-95 / M\u00e9xico - Cuernavaca",
   "pubMillis":1572631193207
}
```

To average these segments along multiple minutes, a DataFrame stores the path geometry, average speed, and number of occurences. Then, everytime the same geometry is encountered within the data for another minute, the following formulas are used to update the data frame:

```
averageSpeed = ((averageSpeed * numberOfOccurences) + newSpeed)/numberOfOccurences
numberOfOccurences += 1
```

To merge multiple hour-resolution DataFrames into the bucketed DataFrames, a very similar formula is used:

```
A := DataFrame1
B := DataFrame2
averageSpeed = ((averageSpeed_A * numberOfOccurences_A) + (averageSpeed_B * numberOfOccurences_B))/(numberOfOccurences_A + numberOfOccurences_B)
numberOfOccurences = (numberOfOccurences_A + numberOfOccurences_B)
```

The DataFrame is sorted by geometry with a custom comparator implemented for shapely LineStrings. This allows for efficiently searching for the corresponding index to a geometry.

The final result looks as follows:

```
            speed  num                                           geometry
0        1.297222   59  LINESTRING (-99.66039 19.29796, -99.65992 19.2...
1        0.000000   59  LINESTRING (-99.65663 19.29306, -99.65773 19.2...
2        3.608333   59  LINESTRING (-99.65627 19.32200, -99.65366 19.3...
3        0.000000   59  LINESTRING (-99.65444 19.29323, -99.65583 19.2...
4        0.827778   59  LINESTRING (-99.65444 19.29323, -99.65440 19.2...
...           ...  ...                                                ...
192493  11.269444   59  LINESTRING (-98.84198 19.30446, -98.83991 19.3...
192494  14.636111   59  LINESTRING (-98.82757 19.31110, -98.82686 19.3...
192495  14.158333   59  LINESTRING (-98.67229 19.34795, -98.67235 19.3...
192496  17.083333   59  LINESTRING (-98.66340 19.35198, -98.66409 19.3...
192497   7.091667   59  LINESTRING (-98.71240 19.33610, -98.71884 19.3...
```
