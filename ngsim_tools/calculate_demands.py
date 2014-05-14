#!/usr/bin/env python
__author__ = 'leahanderson'
import trajtools
from os import listdir, path
import sys


dataset = '/Users/leahanderson/Code/datasets_external/test'
sys.path.append(dataset)
import network_properties

# print network_properties.origin_ids

# trajfiles=[]
t=[]
for f in listdir(dataset+'/vehicle-trajectory-data/'):
    if path.isdir(dataset+'/vehicle-trajectory-data/'+f):
        filename = listdir(dataset+'/vehicle-trajectory-data/'+f)[0]
        t.append(trajtools.read_trajectory_file(dataset+'/vehicle-trajectory-data/'+f+'/'+filename))
print(t[0][0])
by_origin = {}
for o in network_properties.origin_ids:
    # print o
    by_origin[o] = trajtools.filter_by_origin(t, o)



# print(by_origin[123])
