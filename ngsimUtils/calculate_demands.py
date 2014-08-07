#!/usr/bin/env python
__author__ = 'leahanderson'

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



#### OLD VERSION
# for o in network_properties.origin_ids:
#     olist = trajtools.convert_list_to_trajectories(trajtools.filter_by_origin(t, o))
#     print 'ORIGIN'+ str(o)
#     if len(olist)>0:
#         trajs_by_origin[o] = olist
#         driveway=False
#         if o in network_properties.driveways:
#             driveway = True
#         else:
#             entries[o]={'L':[], 'R':[], 'T':[]}
#         for oi in olist:
#             entry_point = oi.get_start_point()
#             ei=1
#             while entry_point[2]==0 and entry_point[4] ==0:
#                 entry_point = oi.get_traj_point(ei)
#                 ei+=1
#             if not driveway:
#                 entries[o][entry_point[5]].append(entry_point[0])
#
#

#
# #import raw trajectory data
# t=[]
# for f in listdir(dataset+'/vehicle-trajectory-data/'):
#     if path.isdir(dataset+'/vehicle-trajectory-data/'+f):
#         filename = listdir(dataset+'/vehicle-trajectory-data/'+f)[0]
#         t.append(trajtools.read_trajectory_file(dataset+'/vehicle-trajectory-data/'+f+'/'+filename))
#
# #sort by origin, convert to trajectory objects
# trajs_by_origin = {}
# entries={}
# for o in network_properties.origin_ids:
#     olist = trajtools.convert_list_to_trajectories(trajtools.filter_by_origin(t, o))
#     print 'ORIGIN'+ str(o)
#     if len(olist)>0:
#         trajs_by_origin[o] = olist
#         driveway=False
#         if o in network_properties.driveways:
#             driveway = True
#         else:
#             entries[o]={'L':[], 'R':[], 'T':[]}
#         for oi in olist:
#             entry_point = oi.get_start_point()
#             ei=1
#             while entry_point[2]==0 and entry_point[4] ==0:
#                 entry_point = oi.get_traj_point(ei)
#                 ei+=1
#             if not driveway:
#                 entries[o][entry_point[5]].append(entry_point[0])
#
# #aggregate entry time stamps into buckets of length TIME_AGGREGATION
# tbins = range(network_properties.time_range[0], network_properties.time_range[1], TIME_AGGREGATION*1000)
# for origin_id, entry_list in entries.iteritems():
#     lefts, unused = histogram(entry_list['L'], tbins)
#     entry_list['L'] = lefts/float(TIME_AGGREGATION)
#     rights, unused = histogram(entry_list['R'], tbins)
#     entry_list['R'] = rights/float(TIME_AGGREGATION)
#     throughs, unused = histogram(entry_list['T'], tbins)
#     entry_list['T'] = throughs/float(TIME_AGGREGATION)
#
# #print out xml
# demand_set= ET.Element('DemandSet')
# demand_set.attrib['id']='-1'
# demand_set.attrib['project_id']='-1'
# for origin_id, movement_queues in entries.iteritems():
#     for m in movement_queues.keys():
#         if sum(movement_queues[m])>0:
#             demand_profile = ET.SubElement(demand_set, 'demandProfile')
#             demand_profile.attrib['dt']=str(TIME_AGGREGATION)
#             demand_profile.attrib['id']=str(-1)
#             demand_profile.attrib['knob']=str(1)
#             demand_profile.attrib['link_id_org']=str(network_links[str(origin_id)+m])
#             demand = ET.SubElement(demand_profile, 'demand')
#             demand.attrib['vehicle_type_id']='0'
#             demand.text = str(movement_queues[m].tolist()).strip('[]').replace(' ','')
#
#
# rough_string = ET.tostring(demand_set, 'utf-8')
# reparsed = minidom.parseString(rough_string)
# print(reparsed.toprettyxml(indent="\t"))
