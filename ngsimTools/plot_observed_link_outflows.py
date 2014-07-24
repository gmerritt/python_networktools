__author__ = 'leahanderson'
import sys
import csv
import matplotlib.pyplot as plt
from numpy import histogram, linspace
import itertools


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


intersections = [is_integer(i) for i in sys.argv[1::]]
dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
sys.path.append(dataset)
import network_properties as netprops
initial_time = netprops.time_range[0]+(125*1000)
final_time = netprops.time_range[0]+(1925*1000)
# time_range = [initial_time, final_time]
time_bounds = linspace(initial_time,final_time, 5000).tolist()

events_dict={}
with open(dataset+'/count_events.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for e in reader:
        # e = row[0].split(',')
        # print e
        i = int(e[0])
        l=is_integer(e[1])
        m=e[2]
        ts=[float(t) for t in e[3::]]
        if not i in events_dict.keys():
            events_dict[i] = { l:{m:ts} }
        elif not l in events_dict[i].keys():
            events_dict[i][l] = {m: ts}
        else:
            events_dict[i][l][m] = ts



# markers = itertools.cycle([ '+', '*', ',', 'o', '.', '1', 'p', ])

for i in intersections:
    for link, move_dict in events_dict[i].iteritems():
        if link[0]+link[1] in [str(i)+'N', str(int(i)+1)+'S'] and link[0] not in ['0', '1', '5']:
            plt.figure()
            for m in ['T', 'R', 'L']:
                if m in move_dict.keys():
                    h, time_array = histogram(move_dict[m], bins=time_bounds)
                    plot_time = [t-initial_time for t in time_array[1::]]
                else:
                    h=[0]*len(plot_time)
                plt.plot(plot_time, accumu(h))
            plt.legend(['T', 'R', 'L'])
            plt.title('Link '+str(link))
            plt.gca().axes.xaxis.set_ticklabels([])
    plt.show()

