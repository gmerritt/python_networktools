__author__ = 'leahanderson'
'''
    This is a simple script to plot modeled outflows and observed outflows on the same axis.
    Before using this script, you need to run ngsimUtils/save_loop_events.py for desired dataset to get observed flows.
'''
import sys
import csv
import matplotlib.pyplot as plt
from numpy import histogram
from scenarioUtils.networktools import load_network
from beatsUtils.outputtools import load_beats_output
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

pp = PdfPages('cumu_outflows_'+version+'.pdf')
network_xml = '/Users/leahanderson/Code/Lanksershim_Network/Lshim_'+version+'_'+model_name[0]+'.xml'
output_prefix={}
for mt in model_name:
    output_prefix[mt]='/Users/leahanderson/Code/Lanksershim_Network/output/'+version+'_'+mt
dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
time_aggregation = 5


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
initial_time = netprops.time_range[0]
final_time = netprops.time_range[1]
# time_range = [initial_time, final_time]
time_bounds = range(initial_time,final_time, time_aggregation*1000)
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
model_output={}
for mt in model_name:
    mout, model_time = load_beats_output(network, output_prefix[mt])
    model_output[mt]=mout
plot_time = [(t-initial_time)/1000.0 for t in time_bounds[1::]]
# markers = itertools.cycle([ '+', '*', ',', 'o', '.', '1', 'p', ])


for i in intersections:
    for link, move_dict in events_dict[i].iteritems():
        if link in data_dict[i].keys():# and not is_integer(link) in netprops.origin_ids:
            plt.figure()
            p=1
            for m in ['T', 'R', 'L']:
                if m in move_dict.keys():
                    datah, _ = histogram(move_dict[m], bins=time_bounds)
                else:
                    datah = [0]*len(plot_time)
                modelh = {}
                for mt in model_name:
                    modelh[mt]=[0]*len(plot_time)
                if data_dict[i][link][m] is not None:
                    for nlink in data_dict[i][link][m]:
                        if not nlink in netprops.shared_lanes.keys():
                            for mt in model_name:
                                modelh[mt] = [k+j for k,j in zip(modelh[mt], model_output[mt]['outflow_car'][str(nlink)][1::])]
                            # print link, nlink
                        # print 'adding links'
                plt.subplot(3,1,p)
                p+=1
                plt.plot(plot_time, accumu(datah))
                for mt in model_name:
                    plt.plot(plot_time, accumu(modelh[mt]))
                # plt.legend(['data']+ model_name, loc=2 )
                plt.title('movement: '+str(m))
                # plt.gca().axes.xaxis.set_ticklabels([])
                if link in ['2NB', '3NB', '4NB', '4SB', '3SB', '2SB'] and m is 'T':
                    for mt in model_name:
                        print(mt + ' cumulative error Link '+link+': ' + str((accumu(modelh[mt])[-1]- accumu(datah)[-1])))
                        pererror = (accumu(modelh[mt])[-1] -  accumu(datah)[-1])/accumu(datah)[-1] *100
                        print ( '= '+ str(pererror) +'%')
            if is_integer(link) in netprops.origin_ids:
                plt.suptitle('Intersection '+str(i) +' BORDER FLOW THROUGH SIGNAL '+ link)
            else:
                plt.suptitle('Link '+ link)
                plt.legend(['data']+ model_name, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
                pp.savefig()

pp.close()

