__author__ = 'leahanderson'

from os import listdir, path
import sys
import csv

from ngsimTools.trajtools import read_trajectory_file, convert_list_to_trajectories, \
                                    link_outflow_events_by_intersection, network_outflow_events, network_inflow_events


dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
sys.path.append(dataset)
import network_properties as netprops


t=[]
for f in listdir(dataset+'/vehicle-trajectory-data/'):
    if path.isdir(dataset+'/vehicle-trajectory-data/'+f):
        filename = listdir(dataset+'/vehicle-trajectory-data/'+f)[0]
        print filename
        t.append(read_trajectory_file(dataset+'/vehicle-trajectory-data/'+f+'/'+filename))
trajectories = convert_list_to_trajectories(t)
intersections = netprops.intersection_ids
links = netprops.link_ids


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


with open(dataset+'/net_inflow_events.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    entry_events = network_inflow_events(trajectories)
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
        # for i in intersections+[0]:
        #     density_dict['intersections'][i]={'NB':{'T':[0]*dt, 'L':[0]*dt, 'R':[0]*dt}, 'SB':{'T':[0]*dt, 'L':[0]*dt, 'R':[0]*dt} }
loss_count = {1:[], 2:[], 3:[], 4:[], 5:[], 0:[]}
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
                else:
                    # print len(t.time)-ts, t.link[ts], t.direction[ts]
                    loss_count[t.link[ts]].append(t.id)
                    loss_count[t.link[ts]] = list(set(loss_count[t.link[ts]]))
            else:
                link_density_dict[t.link[ts]][t.direction[ts]][m][tindex] += 1
print loss_count


        # with open(dataset+'/densities_intersections.csv', 'wb') as csvfile:
        #     writer = csv.writer(csvfile)
        #     for i, dirdict in density_dict['intersections'].iteritems():
        #         if i != 0:
        #             for direct, mdict in dirdict:
        #                 for m, iden in mdict.iteritems():
        #                     writer.writerow([i, direct, m] + iden)

with open(dataset+'/densities_links.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for l, dirdict in link_density_dict.iteritems():
        if l != 0:
            for direct, mdict in dirdict.iteritems():
                for m, lden in mdict.iteritems():
                    writer.writerow([l, direct, m] + lden)



