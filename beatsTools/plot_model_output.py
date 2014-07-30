__author__ = 'leahanderson'

import matplotlib.pyplot as plt
import sys


from scenarioTools.networktools import load_network
from outputtools import load_beats_output

if len(sys.argv)<=1:
    SUFFIX='v18_VCM'
    print('no filename given, using '+SUFFIX)
else:
    version =sys.argv[1]
    model_name=['CTM', 'VCM']
    if len(sys.argv)>2:
        model_name=[sys.argv[2]]
    SUFFIX=[]
    for s in model_name:
        SUFFIX.append(version+'_'+s)
        print('detected model '+version+'_'+s)


network_xml = '/Users/leahanderson/Code/Lanksershim_Network/Lshim_'+SUFFIX[0]+'.xml'
output_prefix=[]
for o in SUFFIX:
    output_prefix.append( '/Users/leahanderson/Code/Lanksershim_Network/output/'+o)


def main():
    network = load_network(network_xml)
    model_output = []
    for op in output_prefix:
        mout, time = load_beats_output(network, op)
        model_output.append(mout)
    selected_links = ['8','38', '6','60','18','15']

    for l in selected_links:
        plt.figure()
        plt.subplot(2,1,1)
        for v in range(0, len(model_output)):
            plt.plot(time, model_output[v]['density_car'][l])
        plt.title('Vehicles in Link '+l)
        plt.ylabel('vehicles')
        plt.legend(model_name)
        plt.subplot(2,1,2)
        for v in range(0, len(model_output)):
            plt.plot(time[0:-1], model_output[v]['outflow_car'][l])
        plt.title('Link '+l+ ' Outflow')
        plt.ylabel('vehicles (per 5 seconds)')
        plt.xlabel('timestamp')
        plt.legend(model_name)
        # plt.plot(time[0:-1], accumu(model_output['outflow_car'][l]), 'b')
        # plt.show()
        # print (model_output['outflow_car'][l])
    plt.show()


def accumu(alist):
    a = []
    total = alist[0]
    a.append(total)
    for x in alist[1::]:
        total += x
        a.append(total)
    return a

###################################################################
if __name__ == '__main__':
    main()
