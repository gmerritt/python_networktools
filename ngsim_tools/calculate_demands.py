#!/usr/bin/env python
__author__ = 'leahanderson'



#SET NUMBER OF SECONDS TO AGGREGATE DEMANDS (typically model dt)
TIME_AGGREGATION = 5
#DEFINE PATH TO DATASET MAIN FOLDER
dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
#LANKERSHIM:
network_links = {'101T':10, '102R':8, '102L':7, '103R':11, '103L':2, '103T':3, '105R':24, '105L':25, '105T':26,
                 '107R':53, '107L':54, '107T':52, '108R':51, '108L':50, '108T':48, '109R':57, '109L':58, '109T':56,
                 '110R':28, '110L':27, '110T':30, '111R':20, '111L':21, '111T':22}


import trajtools
from os import listdir, path
import sys
from numpy import histogram
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
sys.path.append(dataset)
import network_properties

#import raw trajectory data
t=[]
for f in listdir(dataset+'/vehicle-trajectory-data/'):
    if path.isdir(dataset+'/vehicle-trajectory-data/'+f):
        filename = listdir(dataset+'/vehicle-trajectory-data/'+f)[0]
        t.append(trajtools.read_trajectory_file(dataset+'/vehicle-trajectory-data/'+f+'/'+filename))

#sort by origin, convert to trajectory objects
trajs_by_origin = {}
entries={}
for o in network_properties.origin_ids:
    olist = trajtools.convert_list_to_trajectories(trajtools.filter_by_origin(t, o))
    print 'ORIGIN'+ str(o)
    if len(olist)>0:
        trajs_by_origin[o] = olist
        driveway=False
        if o in network_properties.driveways:
            driveway = True
        else:
            entries[o]={'L':[], 'R':[], 'T':[]}
        for oi in olist:
            entry_point = oi.get_start_point()
            ei=1
            while entry_point[2]==0 and entry_point[4] ==0:
                entry_point = oi.get_traj_point(ei)
                ei+=1
            if not driveway:
                entries[o][entry_point[5]].append(entry_point[0])

#aggregate entry time stamps into buckets of length TIME_AGGREGATION
tbins = range(network_properties.time_range[0], network_properties.time_range[1], TIME_AGGREGATION*1000)
for origin_id, entry_list in entries.iteritems():
    lefts, unused = histogram(entry_list['L'], tbins)
    entry_list['L'] = lefts/float(TIME_AGGREGATION)
    rights, unused = histogram(entry_list['R'], tbins)
    entry_list['R'] = rights/float(TIME_AGGREGATION)
    throughs, unused = histogram(entry_list['T'], tbins)
    entry_list['T'] = throughs/float(TIME_AGGREGATION)

#print out xml
demand_set= ET.Element('DemandSet')
demand_set.attrib['id']='-1'
demand_set.attrib['project_id']='-1'
for origin_id, movement_queues in entries.iteritems():
    for m in movement_queues.keys():
        if sum(movement_queues[m])>0:
            demand_profile = ET.SubElement(demand_set, 'demandProfile')
            demand_profile.attrib['dt']=str(TIME_AGGREGATION)
            demand_profile.attrib['id']=str(-1)
            demand_profile.attrib['knob']=str(1)
            demand_profile.attrib['link_id_org']=str(network_links[str(origin_id)+m])
            demand = ET.SubElement(demand_profile, 'demand')
            demand.attrib['vehicle_type_id']='0'
            demand.text = str(movement_queues[m].tolist()).strip('[]').replace(' ','')


rough_string = ET.tostring(demand_set, 'utf-8')
reparsed = minidom.parseString(rough_string)
print(reparsed.toprettyxml(indent="\t"))
