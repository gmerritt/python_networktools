#!/usr/bin/env python
__author__ = 'leahanderson'


'''
This script is tailored to my purpose and won't be very useful for you... but you can use the methodology for other things.
The vehicles are not always sensed in the entry links, they are not actually sensed until they reach their first
intersection. So this script finds the first time they are in an intersection and reads their origin
You will need to change the dataset path, or edit this script to make it a command line arguement
if that is more convenient for you =)
This prints the demands to a string, you will need to copy and paste into scenario file yourself...
also you'll need a network properties file like the one for lankershim_v19 in old_conversion_tools/network_properties.py
'''
from trajtools import direct_to_trajectories
import sys
from numpy import histogram
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


time_resolution = 5
dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
trajectories = direct_to_trajectories(dataset)
sys.path.append(dataset)
import network_properties
netlinks_dict = {}
for odict in network_properties.data_to_scenario.values():
    for oid, mdict in odict.iteritems():
        for mid,nid in mdict.iteritems():
            netlinks_dict[oid+mid]=nid


modeled_origins = [o for o in network_properties.origin_ids if o not in network_properties.driveways]

origin_events = {}
for m in modeled_origins:
    origin_events[m]={ 'T':[], 'R':[], 'L':[] }

for t in trajectories:
    if t.origin in modeled_origins:
        first_movement = t.movement[next((i for i, x in enumerate(t.intersection) if x), None)]
        origin_events[t.origin][first_movement].append(t.time[0])


#aggregate entry time stamps into buckets of length TIME_AGGREGATION
tbins = range(network_properties.time_range[0], network_properties.time_range[1], time_resolution*1000)
origin_dict = {}
for origin, move_dict in origin_events.iteritems():
    for m, elist in move_dict.iteritems():
        h, _ = histogram(elist, tbins)
        origin_dict[str(origin)+m] = h/float(time_resolution)

#print out xml
demand_set= ET.Element('DemandSet')
demand_set.attrib={'id':'-1','project_id':'-1','lockedForEdit':'false','lockedForHistory':'false'}
for o, d in origin_dict.iteritems():
    if sum(d)>0:
        network_link = netlinks_dict[o][0]
        demand_profile = ET.SubElement(demand_set, 'demandProfile')
        demand_profile.attrib = {'dt': str(time_resolution), 'id': '-1', 'knob':'1','link_id_org':str(network_link),
                                 'start_time':'0', 'std_dev_add':'0', 'std_dev_mult':'1'}
        demand = ET.SubElement(demand_profile, 'demand')
        demand.attrib['vehicle_type_id']='1'
        demand.text = str(d.tolist()).strip('[]').replace(' ','')

rough_string = ET.tostring(demand_set, 'utf-8')
reparsed = minidom.parseString(rough_string)
print(reparsed.toprettyxml(indent="\t"))

