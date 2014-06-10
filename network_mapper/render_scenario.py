__author__ = 'leahanderson'

from scenarioTools import *




def main():
    links, nodes = loadNetwork(scenario_file)
    renderNetwork(links, nodes)





scenario_file = './test_network_lankershim.xml'
main()