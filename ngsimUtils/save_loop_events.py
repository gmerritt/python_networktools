__author__ = 'leahanderson'
'''
THIS HAS TO BE RUN BEFORE MOST OF THE PLOTTING TOOLS WILL WORK. you will need to change the dataset path...
or edit to make this a command line input if more convenient!
also you'll need a network properties file like the one for lankershim_v19 in old_conversion_tools/network_properties.py

'''

import sys
import csv

from ngsimUtils.trajtools import direct_to_trajectories, link_outflow_events_by_intersection, network_outflow_events, \
                                    network_inflow_events


dataset = '/Users/leahanderson/Code/datasets_external/lankershim'

trajectories = direct_to_trajectories(dataset)
sys.path.append(dataset)
import network_properties as netprops
intersections = netprops.intersection_ids
links = netprops.link_ids


with open(dataset+'/count_events.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for i in intersections:
        output_events = link_outflow_events_by_intersection(trajectories, i)
        for link, lanedata in output_events.iteritems():
            for movement, timestamp in lanedata.iteritems():
                writer.writerow([i, link, movement]+timestamp)


exit_events = network_outflow_events(trajectories)
with open(dataset+'/net_outflow_events.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for e, ed in exit_events.iteritems():
        writer.writerow([e] + ed)


entry_events = network_inflow_events(trajectories)
with open(dataset+'/net_inflow_events.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for e, ed in entry_events.iteritems():
        for m, md in ed.iteritems():
            writer.writerow([e] + [m] + md)


def timestamp_to_second(tstamp):
    return (tstamp-netprops.time_range[0])/1000

initial_time = 0
final_time = (netprops.time_range[1] - netprops.time_range[0])/1000
link_density_dict = {}
dt = final_time - initial_time
for l in links+[0]:
    link_density_dict[l]={ 'NB':{'T':[0]*dt, 'L':[0]*dt, 'R':[0]*dt},'SB':{'T':[0]*dt, 'L':[0]*dt, 'R':[0]*dt} }
# loss_count = {1:[], 2:[], 3:[], 4:[], 5:[], 0:[]}
for t in trajectories:
    for ts in range(0,len(t.time), 10):
        tindex=timestamp_to_second(t.time[ts])
        if tindex in range(0, final_time-initial_time) and t.link[ts]>0:
            madd = next((i for i, x in enumerate(t.intersection[ts::]) if x), 0)
            m = t.movement[ts+madd]
            if not t.direction[ts] in ['NB', 'SB']:
                nd = next((i for i, x in enumerate(t.direction[ts::]) if x in ['NB', 'SB']), None)
                if nd is not None:
                    t.direction[ts]=t.direction[ts+nd]
                    link_density_dict[t.link[ts]][t.direction[ts+nd]][m][tindex] += 1
                # else:
                #     loss_count[t.link[ts]].append(t.id)
                #     loss_count[t.link[ts]] = list(set(loss_count[t.link[ts]]))
            else:
                link_density_dict[t.link[ts]][t.direction[ts]][m][tindex] += 1
# print loss_count


with open(dataset+'/densities_links.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for l, dirdict in link_density_dict.iteritems():
        if l != 0:
            for direct, mdict in dirdict.iteritems():
                for m, lden in mdict.iteritems():
                    writer.writerow([l, direct, m] + lden)


#
