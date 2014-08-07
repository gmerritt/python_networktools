__author__ = 'leahanderson'

import matplotlib.pyplot as plt
import sys

from scenarioUtils.networktools import load_network
from beatsUtils.outputtools import load_beats_output
from ngsimUtils.trajtools import direct_to_trajectories, output_count_sensor

network_xml = 'scenarios/test_network_lankershim.xml'
output_prefix = '/Users/leahanderson/Code/Lanksershim_Network/output/v15_VCM'


def main():
    network = load_network(network_xml)
    model_output, model_time = load_beats_output(network, output_prefix)
    selected_links = ['38']




    dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
    sys.path.append(dataset)
    import network_properties as netprops
    #for lankershim...
    corresponding = {'61':[4, 'NB', [2,3]],
                     '42':[3, 'SB', [2,1]],
                     '15':[3, 'SB', [31]],
                     '5': None,
                     '4':[4, 'NB', [11]],
                     '10':[1, 'NB', [1,2]],
                     '38': [2,'NB',[2,3]], 
                     '31':[2, 'NB', [11]] }


    traj_list = direct_to_trajectories(dataset)

    for l in selected_links:
        link_info = corresponding[l]
        initial_time = netprops.time_range[0]
        final_time = netprops.time_range[1]
        data_counts, data_time = output_count_sensor(traj_list, link_info[0], link_info[1], [initial_time, final_time],
                                                     5, link_info[2])
        data_time = [(d-initial_time)/1000.0 for d in data_time]
        plt.subplot(2,1,1)
        plt.plot(model_time, model_output['density_car'][l])
        plt.title('Vehicles in Link '+l)
        plt.ylabel('vehicles')
        plt.subplot(2,1,2)
        plt.plot(model_time[0:-1], model_output['outflow_car'][l], 'b', data_time, data_counts, 'k')
        plt.title('Link '+l+ ' Outflow')
        plt.ylabel('vehicles (per 5 seconds)')
        plt.xlabel('timestamp')
        plt.show()
        plt.plot(model_time[0:-1], accumu(model_output['outflow_car'][l]), 'b',
                 data_time,accumu(data_counts), 'k')
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
