__author__ = 'leahanderson'




def load_beats_output(network, output_prefix):
    import csv
    data_types = ['density_car', 'inflow_car', 'outflow_car']
    expected_files = ['_'+p+'_0.txt' for p in data_types]
    file_list = [output_prefix+o for o in expected_files]
    data={'links':network.get_link_list()}
    for idx,path in enumerate(file_list):
        with open(path) as f:
            reader = csv.reader(f, delimiter="\t")
            data_string = list(reader)
        data[data_types[idx]]={}
        for il,l in enumerate(data['links']):
            # print il, l
            # print len(data_string)
            for t in data_string:
                if len(t)<59: print data_types[idx], il, l, len(t)
            data[data_types[idx]][l]=[float(t[il]) for t in data_string]

    with open(output_prefix+'_time_0.txt') as f:
        reader = csv.reader(f, delimiter="\t")
        time = [float(t[0]) for t in list(reader)]
    return data, time
