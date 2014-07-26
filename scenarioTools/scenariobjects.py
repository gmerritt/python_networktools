__author__ = 'leahanderson'


class ScenarioNetwork:
    def __init__(self, scenario_file_name):
        import xml.etree.ElementTree as ET
        tree = ET.parse(scenario_file_name)
        scenario_tree = tree.getroot()
        network = scenario_tree.find('NetworkSet/network')
        nodes = network.find('NodeList')
        node_dict={}
        for n in nodes.iter('node'):
            node_position = n.find('position').find('point')
            node_dict[n.attrib['id']] = {'position':[node_position.attrib['lat'], node_position.attrib['lng']],
                                         'type':n.find('node_type').attrib['name']}
        link_dict={}
        links = network.find('LinkList')
        for l in links.iter('link'):
            link_dict[l.attrib['id']] = {'lanes': l.attrib['lanes'], 'offset': l.attrib['lane_offset'],
                                         'length': l.attrib['length']}
            link_dict[l.attrib['id']]['nodes'] = [l.find('begin').attrib['node_id'], l.find('end').attrib['node_id']]
            link_position = l.find('position')
            if link_position is not None:
                link_dict[l.attrib['id']]['position'] = [[p.attrib['lat'], p.attrib['lng']]
                                                         for p in link_position.findall('point')]
            else:
                link_dict[l.attrib['id']]['position'] = [node_dict[l.find('begin').attrib['node_id']]['position'],
                                                         node_dict[l.find('end').attrib['node_id']]['position']]
            link_dict[l.attrib['id']]['type'] = l.find('link_type').attrib['name']
        self.links = [l.attrib['id'] for l in links.iter('link')]
        self.nodes = [n.attrib['id'] for n in nodes.iter('node')]
        self.link_dict = link_dict
        self.node_dict = node_dict
        scenario_path = scenario_file_name.split('/')
        self.name = scenario_path.pop()
        print self.name
        self.file_location = '/'.join(scenario_path)

        demand_dict={}
        demandset = scenario_tree.find('DemandSet')
        for d in demandset.iter('demandProfile'):
            demand_dict[d.attrib['link_id_org']]=[float(i) for i in d.find('demand').text.split(',')]
        self.demand_dict = demand_dict

        splits_dict={}
        splitset = scenario_tree.find('SplitRatioSet')
        for snode in splitset.iter('splitRatioProfile'):
            for s in snode.iter('splitratio'):
                sin = int(s.attrib['link_in'])
                sout = int(s.attrib['link_out'])
                if sin not in splits_dict.keys():
                    splits_dict[sin]={}
                splits_dict[sin][sout]=float(s.text)
        self.splits_dict = splits_dict
        # print splits_dict

    def get_link_dict(self):
        return self.link_dict

    def get_node_dict(self):
        return self.node_dict

    def get_link_list(self):
        return self.links