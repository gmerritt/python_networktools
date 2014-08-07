__author__ = 'leahanderson'
'''
    This is a simple script to plot modeled outflows and observed outflows on the same axis.
    Before using this script, you need to run ngsimUtils/save_loop_events.py for desired dataset to get observed flows.
'''
import sys
import csv
import matplotlib.pyplot as plt
from numpy import histogram, arange
# import itertools
from scenarioUtils.networktools import load_network
from beatsUtils.outputtools import load_beats_output


dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
network_xml = '/Users/leahanderson/Code/Lanksershim_Network/Lshim_v15_VCM.xml'
output_prefix = '/Users/leahanderson/Code/Lanksershim_Network/output/v15_VCM'


def is_integer(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return s

def accumu(alist):
    a = []
    total = alist[0]
    a.append(total)
    for x in alist[1::]:
        total += x
        a.append(total)
    return a

sys.path.append(dataset)
import network_properties as netprops

origins = netprops.origin_ids
initial_time = netprops.time_range[0]
final_time = netprops.time_range[1]
time_resolution = 5
# time_range = [initial_time, final_time]
time_bounds = arange(initial_time,final_time, 1000*time_resolution).tolist()
# ignore_these_links = netprops.boundary_links
network = load_network(network_xml)


events_dict={}
with open(dataset+'/net_inflow_events.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for e in reader:
        # e = row[0].split(',')
        # print e
        o = e[0]
        m=e[1]
        ts=[int(t) for t in e[2::]]
        if o not in events_dict.keys():
            events_dict[o] = {m:ts}
        else:
            events_dict[o][m]=ts
# print events_dict

intersections = netprops.intersection_ids
network_dict = netprops.data_to_scenario
# model_demand, model_time = load_beats_demand(network)
plot_time = [(t-initial_time)/1000.0 for t in time_bounds[1::]]

for i in intersections:
    for link, move_dict in network_dict[i].iteritems():
        if is_integer(link) in origins:
            plt.figure()
            p=1
            for m in ['T', 'R', 'L']:
                lid = move_dict[m]
                if lid is not None and m in events_dict[link].keys():
                    datah, _ = histogram(events_dict[link][m], bins=time_bounds)
                    scenarioh = [time_resolution*d for d in network.demand_dict[str(lid[0])]]
                else:
                    datah = [0]*len(plot_time)
                    scenarioh=datah
                plt.subplot(3,1,p)
                p+=1
                plt.plot(plot_time, accumu(datah))
                plt.plot(plot_time, accumu(scenarioh))
                plt.legend(['data', 'scenario demand'])
                plt.title('movement: '+str(m))
            plt.suptitle('Origin '+ link)
plt.show()


