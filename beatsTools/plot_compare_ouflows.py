__author__ = 'leahanderson'
'''
    This is a simple script to plot modeled outflows and observed outflows on the same axis.
    Before using this script, you need to run ngsimTools/save_loop_events.py for desired dataset to get observed flows.
'''
import sys
import csv
import matplotlib.pyplot as plt
from numpy import histogram, arange
# import itertools
from scenarioTools.networktools import load_network
from beatsTools.outputtools import load_beats_output


dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
network_xml = 'scenarios/test_network_lankershim.xml'
output_prefix = '/Users/leahanderson/Code/Lanksershim_Network/output/v11_VCM'


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
intersections = netprops.intersection_ids
initial_time = netprops.time_range[0]+(125*1000)
final_time = netprops.time_range[0]+(1925*1000)
# time_range = [initial_time, final_time]
time_bounds = arange(initial_time,final_time, 5000).tolist()
# ignore_these_links = netprops.boundary_links

events_dict={}
with open(dataset+'/count_events.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for e in reader:
        # e = row[0].split(',')
        # print e
        i = int(e[0])
        l=e[1]
        m=e[2]
        ts=[float(t) for t in e[3::]]
        if not i in events_dict.keys():
            events_dict[i] = { l:{m:ts} }
        elif not l in events_dict[i].keys():
            events_dict[i][l] = {m: ts}
        else:
            events_dict[i][l][m] = ts

data_dict = netprops.data_to_scenario
network = load_network(network_xml)
model_output, model_time = load_beats_output(network, output_prefix)
plot_time = [(t-initial_time)/1000.0 for t in time_bounds[1::]]
# markers = itertools.cycle([ '+', '*', ',', 'o', '.', '1', 'p', ])

for i in intersections:
    for link, move_dict in events_dict[i].iteritems():
        if link in data_dict[i].keys():
            plt.figure()
            p=1
            for m in ['T', 'R', 'L']:
                if m in move_dict.keys():
                    datah, _ = histogram(move_dict[m], bins=time_bounds)
                else:
                    datah = [0]*len(plot_time)
                if data_dict[i][link][m] is not None:
                    modelh = model_output['outflow_car'][str(data_dict[i][link][m][0])][1::]
                    for nlink in data_dict[i][link][m][1::]:
                        modelh = [k+j for k,j in zip(modelh, model_output['outflow_car'][str(nlink)][1::])]
                        # print 'adding links'
                else:
                    modelh = [0]*len(plot_time)
                plt.subplot(3,1,p)
                p+=1
                plt.plot(plot_time, accumu(datah))
                plt.plot(plot_time, accumu(modelh))
                plt.legend(['data', 'VCM'])
                plt.title('movement: '+str(m))
                # plt.gca().axes.xaxis.set_ticklabels([])
            if is_integer(link) in netprops.origin_ids:
                plt.suptitle('Intersection '+str(i) +' INCOMING BOUNDARY FLOW '+ link)
            else:
                plt.suptitle('Link '+ link)
plt.show()


