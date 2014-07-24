__author__ = 'leahanderson'

from os import listdir, path
import sys
import csv

from ngsimTools.trajtools import read_trajectory_file, convert_list_to_trajectories, \
                                    link_outflow_events_by_intersection, network_outflow_events


dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
sys.path.append(dataset)
import network_properties as netprops
initial_time = netprops.time_range[0]+(125*1000)
final_time = netprops.time_range[0]+(1925*1000)
time_range = [initial_time, final_time]

t=[]
for f in listdir(dataset+'/vehicle-trajectory-data/'):
    if path.isdir(dataset+'/vehicle-trajectory-data/'+f):
        filename = listdir(dataset+'/vehicle-trajectory-data/'+f)[0]
        print filename
        t.append(read_trajectory_file(dataset+'/vehicle-trajectory-data/'+f+'/'+filename))
trajectories = convert_list_to_trajectories(t)


intersections = netprops.intersection_ids
with open(dataset+'/count_events.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for i in intersections:
        output_events = link_outflow_events_by_intersection(trajectories, i)
        for link, lanedata in output_events.iteritems():
            for movement, timestamp in lanedata.iteritems():
                # print i, link, lane
                writer.writerow([i, link, movement]+timestamp)


with open(dataset+'/net_outflow_events.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    exit_events = network_outflow_events(trajectories)
    for e, ed in exit_events.iteritems():
        writer.writerow([e] + ed)





