__author__ = 'leahanderson'
import sys
import csv
import matplotlib.pyplot as plt
from numpy import  zeros
from scenarioTools.networktools import load_network
from beatsTools.outputtools import load_beats_output
from matplotlib.backends.backend_pdf import PdfPages

version = 'v18'
model_name = ['VCM']
if len(sys.argv)<=1:
    print('no filename given, using '+version+'_'+model_name[0])
else:
    version =sys.argv[1]
    model_name=['CTM', 'VCM']
    if len(sys.argv)>2:
        model_name=[sys.argv[2]]
    for s in model_name:
        print('using model '+version+'_'+s)

network_xml = '/Users/leahanderson/Code/Lanksershim_Network/Lshim_'+version+'_'+model_name[0]+'.xml'
output_prefix={}
for mt in model_name:
    output_prefix[mt]='/Users/leahanderson/Code/Lanksershim_Network/output/'+version+'_'+mt
dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
time_aggregation = 5

sys.path.append(dataset)

pp = PdfPages('densities_'+version+'.pdf')
import network_properties as netprops
intersections = netprops.intersection_ids
links = netprops.link_ids
initial_time = 0
final_time = (netprops.time_range[1] - netprops.time_range[0])/1000
time_bounds = range(initial_time,final_time, time_aggregation)
network = load_network(network_xml)

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

# plot_time = range(initial_time, final_time)
# for l, mdict in link_densities.iteritems():
#     plt.figure()
#     p=1
#     for m in ['T', 'R', 'L']:
#         plt.subplot(3,1,p)
#         p+=1
#         plt.plot(plot_time, mdict[m])
#         plt.title(m)
#     plt.suptitle('Link '+str(l))
# plt.show()

model_output = {}
for mt in model_name:
    mout, model_time = load_beats_output(network, output_prefix[mt])
    model_output[mt]=mout
data_plot_time = range(initial_time, final_time)
model_plot_time = range(initial_time, final_time, time_aggregation)
network_dict = {}
for v in netprops.data_to_scenario.values():
    network_dict.update(v)
for l, mdict in link_densities.iteritems():
    if l in network_dict.keys():
        plt.figure()
        p=1
        for m in ['T', 'R', 'L']:
            plt.subplot(3,1,p)
            p+=1
            modelh = {}
            for mt in model_name:
                modelh[mt]=zeros(len(model_plot_time))
            if network_dict[l][m] is not None:
                for nlink in network_dict[l][m]:
                    if nlink in netprops.shared_lanes.keys():
                        dlink = netprops.shared_lanes[nlink][m]
                        split_scale = network.splits_dict[nlink][dlink]
                        # print link, nlink, dlink, split_scale
                    else:
                        split_scale=1.0
                    for mt in model_name:
                        # print modelh
                        modelh[mt] = [k+(j*split_scale) for k, j in zip(modelh[mt], model_output[mt]['density_car'][str(nlink)][1::])]
                    # print 'adding links'
                plt.plot(data_plot_time, mdict[m])
                for mt in model_name:
                    plt.plot(model_plot_time, modelh[mt])
            plt.legend(['data']+ model_name, bbox_to_anchor=(0, 0, 1, 1), bbox_transform=plt.gcf().transFigure)
            plt.title(m)
        plt.suptitle('Link '+str(l))
        pp.savefig()
pp.close()

#
#
# model_output, model_time = load_beats_output(network, output_prefix)
# data_plot_time = range(initial_time, final_time)
# model_plot_time = range(initial_time, final_time, time_aggregation)
# network_dict = {}
# for v in netprops.data_to_scenario.values():
#     network_dict.update(v)
# for l, mdict in link_densities.iteritems():
#     if l in network_dict.keys():
#         plt.figure()
#         p=1
#         for m in ['T', 'R', 'L']:
#             plt.subplot(3,1,p)
#             p+=1
#             modelh = [0]*len(model_plot_time)
#             if network_dict[l][m] is not None:
#                 for nlink in network_dict[link][m]:
#                     if nlink in netprops.shared_lanes.keys():
#                         dlink = netprops.shared_lanes[nlink][m]
#                         split_scale = network.splits_dict[nlink][dlink]
#                         # print link, nlink, dlink, split_scale
#                     else:
#                         split_scale=1.0
#                     modelh = [k+(j*split_scale) for k,j in zip(modelh, model_output['density_car'][str(nlink)][1::])]
#                     # print 'adding links'
#             plt.plot(data_plot_time, mdict[m])
#             plt.plot(model_plot_time, modelh)
#             plt.title(m)
#         plt.suptitle('Link '+str(l))
# plt.show()
