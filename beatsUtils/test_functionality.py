__author__ = 'leahanderson'

from scenarioUtils.networktools import load_network
from outputtools import load_beats_output

network = load_network('test_network_lankershim.xml')
data, time = load_beats_output(network, '/Users/leahanderson/Code/Lanksershim_Network/output/v7_TEST')
print data.keys()



# print data['density_car']['11']
print data['outflow_car']['11']
