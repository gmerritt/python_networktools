__author__ = 'leahanderson'

import matplotlib.pyplot as plt
from os import listdir, path
import sys
from numpy import array

from scenarioTools.networktools import load_network
from outputtools import load_beats_output

network_xml = 'scenarios/test_network_lankershim.xml'
output_prefix = '/Users/leahanderson/Code/Lanksershim_Network/output/v12_VCM'


def main():
    network = load_network(network_xml)
    model_output, time = load_beats_output(network, output_prefix)
    selected_links = ['16', '32', '60']



    for l in selected_links:
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(time, model_output['density_car'][l])
        plt.title('Vehicles in Link '+l)
        plt.ylabel('vehicles')
        plt.subplot(2,1,2)
        plt.plot(time[0:-1], model_output['outflow_car'][l], 'b')
        plt.title('Link '+l+ ' Outflow')
        plt.ylabel('vehicles (per 5 seconds)')
        plt.xlabel('timestamp')
        # plt.plot(time[0:-1], accumu(model_output['outflow_car'][l]), 'b')
        # plt.show()
        print (model_output['outflow_car'][l])
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
