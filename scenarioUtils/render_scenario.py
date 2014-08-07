__author__ = 'leahanderson'

from networktools import load_network, render_network, animate_network

def main():
    network = load_network(scenario_file)
    # animate_network(network, [])
    render_network(network)

scenario_file = './test_network_lankershim.xml'
main()


