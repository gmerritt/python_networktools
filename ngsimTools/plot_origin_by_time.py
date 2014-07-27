__author__ = 'leahanderson'

from trajtools import direct_to_trajectories

import sys
from numpy import histogram
import matplotlib.pyplot as plt


time_aggregation = 5
dataset = '/Users/leahanderson/Code/datasets_external/lankershim'

trajectories = direct_to_trajectories(dataset)


sys.path.append(dataset)
import network_properties as netprops
# netlinks_dict = {}
# # for odict in network_properties.data_to_scenario.values():
# #     for oid, mdict in odict.iteritems():
# #         for mid,nid in mdict.iteritems():
# #             netlinks_dict[oid+mid]=nid
initial_time = netprops.time_range[0]
final_time = netprops.time_range[1]
# time_range = [initial_time, final_time]
time_bounds = range(initial_time,final_time, time_aggregation*1000)


origin_dict = {}
for t in trajectories:
    if not t.origin in origin_dict.keys():
        origin_dict[t.origin]=[]
    origin_dict[t.origin].append(t.time[0])

hist_dict={}
for o, olist in origin_dict.iteritems():
    (hist_dict[t.origin], _)=histogram(olist, time_bounds)
    plt.figure()
    plt.plot(time_bounds[1::], hist_dict[t.origin])
    plt.title('origin '+str(o))
plt.show()