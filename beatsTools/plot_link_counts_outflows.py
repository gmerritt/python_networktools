__author__ = 'leahanderson'

import matplotlib.pyplot as plt
from os import listdir, path
import sys
from numpy import array

from scenarioTools.networktools import load_network
from outputtools import load_beats_output
from ngsimTools.trajtools import read_trajectory_file, convert_list_to_trajectories, output_count_sensor

network_xml = 'scenarios/test_network_lankershim.xml'
output_prefix = '/Users/leahanderson/Code/Lanksershim_Network/output/v7_TEST'


def main():
    network = load_network(network_xml)
    model_output, time = load_beats_output(network, output_prefix)
    selected_links = ['61']




    dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
    sys.path.append(dataset)
    import network_properties as netprops
    #for lankershim...
    corresponding = {'61':[4,'NB',2,3],
                     '42':[3,'SB',2,1],
                     '15':[3, 'NB', 3, 31],
                     '5': None,
                     '4':[4, 'NB', 11]}


    t=[]
    for f in listdir(dataset+'/vehicle-trajectory-data/'):
        if path.isdir(dataset+'/vehicle-trajectory-data/'+f):
            filename = listdir(dataset+'/vehicle-trajectory-data/'+f)[0]
            t.append(read_trajectory_file(dataset+'/vehicle-trajectory-data/'+f+'/'+filename))
    traj_list = convert_list_to_trajectories(t)

    for l in selected_links:
        link_info = corresponding[l]
        s_time, s_out = output_count_sensor(traj_list, link_info[0], link_info[1], link_info[2:-1],
                                            [netprops.time_range[0]+(125*1000), netprops.time_range[0]+(1925*1000)], 5)
        time_vector = (array(s_time[1::]) - array([s_time[0]]*len(s_time[1::])))/1000.0
        counts_vector = array(s_out)
        plt.subplot(2,1,1)
        plt.plot(time, model_output['density_car'][l])
        plt.title('Vehicles in Link '+l)
        plt.ylabel('vehicles')
        plt.subplot(2,1,2)
        plt.plot(time[0:-1], model_output['outflow_car'][l], 'b', time_vector.tolist(), counts_vector.tolist(), 'k')
        plt.title('Link '+l+ ' Outflow')
        plt.ylabel('vehicles (per 5 seconds)')
        plt.xlabel('timestamp')
        plt.show()
        # print len(time)
        # print len(accumu(model_output['outflow_car'][l]))
        # print len(time_vector.tolist())
        # print len(accumu(counts_vector.tolist()))
        plt.plot(time[0:-1], accumu(model_output['outflow_car'][l]), 'b',
                 time_vector.tolist(),accumu(counts_vector.tolist()), 'k')
        plt.show()


def accumu(alist):
    a = []
    total = alist[0]
    a.append(total)
    for x in alist[1::]:
        total += x
        a.append(total+x)
    return a

###################################################################
if __name__ == '__main__':
    main()
