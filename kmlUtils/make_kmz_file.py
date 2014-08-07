__author__ = 'leahanderson'
from optparse import OptionParser
from pyUtils.log import abort
from kmltools import convert_network_to_kml, convert_data_to_kml, write_kmz
from scenarioUtils.networktools import load_network
from beatsUtils.outputtools import load_beats_output


def main():
    parser = OptionParser()
    parser.add_option('-s', '--scenario', action='store', type='string', dest='scenario_xml', default='./scenarions/test_network_lankershim.xml', help='path to scenario file' )
    parser.add_option('-o', '--outdir', action='store', type='string', dest='outdir', help='directory to output files (defaults to same as input directory)' )
    parser.add_option('-d', '--data', action='store', type='string', dest='data_prefix', default=None, help='path to beats output data, if exists' )
    (options, args) = parser.parse_args()

    if not options.scenario_xml:
        # print('isthisworking')
        abort("missing --scenario file, try --help")

    scenario_network = load_network(options.scenario_xml)
    print scenario_network.name

    if options.data_prefix is None:
        k = convert_network_to_kml(scenario_network)
    else:
        data = load_beats_output(scenario_network, options.data_prefix)
        k = convert_data_to_kml(scenario_network, data)

    write_kmz(k, scenario_network.file_location + '/' + scenario_network.name.strip('.xml'))

###################################################################
if __name__ == '__main__':
    main()
