__author__ = 'leahanderson'
import sys
import csv
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy import zeros, histogram
from scenarioTools.networktools import load_network
from beatsTools.outputtools import load_beats_output


#
#
# plt.plot([1,2,3])
# plt.savefig('myfig2.png')


version = 'v19'
model_name = ['CTM', 'VCM']
network_xml = '/Users/leahanderson/Code/Lanksershim_Network/Lshim_'+version+'_'+model_name[0]+'.xml'
output_prefix={}
for mt in model_name:
    output_prefix[mt]='/Users/leahanderson/Code/Lanksershim_Network/output/'+version+'_'+mt
dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
time_aggregation = 5
sys.path.append(dataset)

import network_properties as netprops
intersections = netprops.intersection_ids
links = netprops.link_ids
initial_time = 0
final_time = (netprops.time_range[1] - netprops.time_range[0])/1000
time_bounds = range(netprops.time_range[0],netprops.time_range[1], time_aggregation*1000)
network = load_network(network_xml)

#load data density
link_densities={}
with open(dataset+'/densities_links.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        link = row[0]+row[1]
        movement = row[2]
        denlist = [int(d) for d in row[3::]]
        if link not in link_densities.keys():
            link_densities[link]={movement:denlist}
        else:
            link_densities[link][movement]=denlist

#load data outflow events
events_dict={}
with open(dataset+'/count_events.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for e in reader:
        # e = row[0].split(',')
        # print e
        i = int(e[0])
        l=e[1]
        mo=e[2]
        ts=[float(t) for t in e[3::]]
        if not l in events_dict.keys():
            events_dict[l] = {mo: ts}
        else:
            events_dict[l][mo] = ts

#load model output
model_output = {}
for mt in model_name:
    mout, model_time = load_beats_output(network, output_prefix[mt])
    model_output[mt]=mout


#set up plotting stuff
data_plot_time = range(initial_time, final_time)
model_plot_time = range(initial_time, final_time, time_aggregation)
#create mapping from model links to data links
network_dict = {}
for v in netprops.data_to_scenario.values():
    network_dict.update(v)








#plot densities
plotorder = ['2NB', '3NB', '4NB', '4SB', '3SB', '2SB']
lineplotstyles = {'data':'y', 'CTM':'c--', 'VCM':'m:'}

fig=plt.figure()
for l, mdict in link_densities.iteritems():
    matplotlib.rc('xtick', labelsize=10)
    if l in network_dict.keys():
        p = plotorder.index(l) +1
        ax=plt.subplot(6,1,p)
        modelh = {}
        for mt in model_name:
            modelh[mt]=zeros(len(model_plot_time))
        if network_dict[l]['T'] is not None:
            for nlink in network_dict[l]['T']:
                if nlink in netprops.shared_lanes.keys():
                    dlink = netprops.shared_lanes[nlink]['T']
                    split_scale = network.splits_dict[nlink][dlink]
                    # print link, nlink, dlink, split_scale
                else:
                    split_scale=1.0
                for mt in model_name:
                    # print modelh
                    modelh[mt] = [k+(j*split_scale) for k, j in zip(modelh[mt], model_output[mt]['density_car'][str(nlink)][1::])]
                # print 'adding links'
            plt.plot(data_plot_time, mdict['T'],  lineplotstyles['data'], lw=1)
            for mt in model_name:
                plt.plot(model_plot_time[1::], modelh[mt][0:-1], lineplotstyles[mt], lw=2)
        plt.legend(['observed']+model_name, bbox_to_anchor=(0, 0, 1, 1), bbox_transform=plt.gcf().transFigure, fontsize=16)
        plt.title('Link '+str(l), fontsize=14)
        plt.ylabel('vehicles',fontsize=14)
        if p==6:
            plt.xlabel('seconds since 0800',fontsize=14)
            matplotlib.rc('xtick', labelsize=14)
        else:
            ax.set_xticklabels([])
        # else:
        #     plt.get_xaxis().set_ticks([])

plt.suptitle('Link Vehicle-Counts', fontsize=16)
# plt.show()
#
# #plot outflows
# fig = plt.figure()
# for link, move_dict in events_dict.iteritems():
#     if link in plotorder:# and not is_integer(link) in netprops.origin_ids:
#         p = plotorder.index(link) +1
#         ax=plt.subplot(6,1,p)
#         if 'T' in move_dict.keys():
#             datah, _ = histogram(move_dict['T'], bins=time_bounds)
#         else:
#             datah = [0]*(len(model_plot_time)-1)
#         modelh = {}
#         for mt in model_name:
#             modelh[mt]=[0]*(len(model_plot_time))
#         if network_dict[link]['T'] is not None:
#             for nlink in network_dict[link]['T']:
#                 if not nlink in netprops.shared_lanes.keys():
#                     for mt in model_name:
#                         modelh[mt] = [k+j for k,j in zip(modelh[mt], model_output[mt]['outflow_car'][str(nlink)])]
#                     # print link, nlink
#                 # print 'adding links'
#         # print len(datah), len(data_plot_time)
#         plt.plot(model_plot_time[0:-1], datah, lineplotstyles['data'], lw=1)
#         for mt in model_name:
#             plt.plot(model_plot_time, modelh[mt], lineplotstyles[mt], lw=2)
#         # plt.legend(['data']+ model_name, loc=2 )
#         plt.title('Link '+link)
#         # plt.gca().axes.xaxis.set_ticklabels([])
#         if p==6:
#             plt.xlabel('seconds since 0800',fontsize=14)
#             matplotlib.rc('xtick', labelsize=14)
#         else:
#             ax.set_xticklabels([])
# plt.legend(['observed']+model_name, bbox_to_anchor=(0, 0, 1, 1), bbox_transform=plt.gcf().transFigure,fontsize=16)
# plt.suptitle('Link Outflows', fontsize=16)


#plot outflow error
fig=plt.figure()
for link, move_dict in events_dict.iteritems():
    if link in plotorder:# and not is_integer(link) in netprops.origin_ids:
        p = plotorder.index(link) +1
        ax = plt.subplot(6,1,p)
        if 'T' in move_dict.keys():
            datah, _ = histogram(move_dict['T'], bins=time_bounds)
        else:
            datah = [0]*(len(model_plot_time)-1)
        modelh = {}
        for mt in model_name:
            modelh[mt]=[0]*(len(model_plot_time))
        if network_dict[link]['T'] is not None:
            for nlink in network_dict[link]['T']:
                if not nlink in netprops.shared_lanes.keys():
                    for mt in model_name:
                        modelh[mt] = [k+j for k,j in zip(modelh[mt], model_output[mt]['outflow_car'][str(nlink)])]
                    # print link, nlink
                # print 'adding links'
        # print len(datah), len(data_plot_time)
        for mt in model_name:
            model_error = [m-d for m,d in zip(modelh[mt][0:-1], datah)]
            plt.plot(model_plot_time[160:240], model_error[161:241], lineplotstyles[mt], lw=2)
        # plt.legend(['data']+ model_name, loc=2 )
        plt.title('Link '+link)
        plt.ylabel('vehicles',fontsize=14)
        # plt.gca().axes.xaxis.set_ticklabels([])
        if p==6:
            plt.xlabel('seconds since 0800',fontsize=14)
            matplotlib.rc('xtick', labelsize=14)
        else:
            ax.set_xticklabels([])
plt.legend(model_name, bbox_to_anchor=(0, 0, 1, 1), bbox_transform=plt.gcf().transFigure,fontsize=16)
plt.suptitle('Model Error: Link Outflows', fontsize=16)


#plot outflow 3SB
linkdir = '3SB'
fig = plt.figure()
datah, _ = histogram(events_dict[linkdir]['T'], bins=time_bounds)
modelh = {}
for mt in model_name:
    modelh[mt]=[0]*(len(model_plot_time))
for nlink in network_dict[linkdir]['T']:
    if not nlink in netprops.shared_lanes.keys():
        for mt in model_name:
            modelh[mt] = [k+j for k,j in zip(modelh[mt], model_output[mt]['outflow_car'][str(nlink)])]
plt.plot(model_plot_time[0:-1], datah, lineplotstyles['data'], lw=1)
for mt in model_name:
    plt.plot(model_plot_time, modelh[mt], lineplotstyles[mt], lw=2)
plt.legend(['observed']+model_name, loc=2 )
plt.title('Outflow Link '+linkdir, fontsize=16)
plt.xlabel('seconds since 0800',fontsize=14)
plt.ylabel('vehicles',fontsize=14)
matplotlib.rc('xtick', labelsize=14)
plt.legend(['observed']+model_name,loc=1,fontsize=16)


plt.show()