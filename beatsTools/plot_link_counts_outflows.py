__author__ = 'leahanderson'

import matplotlib.pyplot as plt
from os import listdir, path
import sys

from scenarioTools.networktools import load_network
from outputtools import load_beats_output
from ngsimTools.trajtools import read_trajectory_file, convert_list_to_trajectories, output_count_sensor

network_xml = 'scenarios/test_network_lankershim.xml'
output_prefix = '/Users/leahanderson/Code/Lanksershim_Network/output/v7_TEST'


def main():
    network = load_network(network_xml)
    model_output, time = load_beats_output(network, output_prefix)
    selected_links = ['61', '42', '15', '5', '4']
    for l in selected_links:

        plt.subplot(2,1,1)
        plt.plot(time, model_output['density_car'][l])
        plt.title('Vehicles in Link '+l)
        plt.ylabel('vehicles')


        plt.subplot(2,1,2)
        plt.plot(time[0:-1], model_output['outflow_car'][l])
        plt.title('Link '+l+ ' Outflow')
        plt.ylabel('vehicles per second')
        plt.xlabel('timestamp')

        plt.show()


    dataset = '/Users/leahanderson/Code/datasets_external/lankershim'
    sys.path.append(dataset)
    import network_properties
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
        s_time, s_out = output_count_sensor(traj_list,link_info[0], link_info[1], link_info[2:-1],
                                            [network_properties.time_range[0], network_properties.time_range[1]], 5)
        plt.plot(s_time, s_out)

###################################################################
if __name__ == '__main__':
    main()
