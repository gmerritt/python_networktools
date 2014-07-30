__author__ = 'leahanderson'

import matplotlib.pyplot as plt
import sys


from scenarioTools.networktools import load_network
from outputtools import load_beats_output
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


def main():
    network = load_network(network_xml)
    model_output = {}
    for mt,op in output_prefix.iteritems():
        mout, time = load_beats_output(network, op)
        model_output[mt]=mout
    selected_links = ['8','38', '6','60','18','15']

    for l in selected_links:
        plt.figure()
        plt.subplot(2,1,1)
        for mt in model_name:
            plt.plot(time, model_output[mt]['density_car'][l])
        plt.title('Vehicles in Link '+l)
        plt.ylabel('vehicles')
        plt.legend(model_name)
        plt.subplot(2,1,2)
        for mt in model_name:
            plt.plot(time[0:-1], model_output[mt]['outflow_car'][l])
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
