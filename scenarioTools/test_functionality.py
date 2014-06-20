__author__ = 'leahanderson'

from networktools import load_network, process_beats_output

network = load_network('test_network_lankershim.xml')
data, time = process_beats_output(network, '/Users/leahanderson/Code/Lanksershim_Network/output/v5_TEST')
print data.keys()



print data['density_car']['11']
# print data['outflow_car']['11']
