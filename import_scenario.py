#!/usr/bin/env python
__author__ = 'leahanderson'
import xml.etree.ElementTree as ET
import time


scenario_file = './Lshim_v2.xml'
tree = ET.parse(scenario_file)
scenario = tree.getroot()
network = scenario.find('NetworkSet/network')
nodes = network.find('NodeList')
links = network.find('LinkList')

'''
STEP 1: remove all references to input/output links in node structures
    (these are not typically handled well by scenario editor)
'''
for n in nodes.iter('node'):
    bad_outs = n.find('outputs')
    bad_ins = n.find('inputs')
    for o in bad_outs.findall('output'):
        bad_outs.remove(o)
    for i in bad_ins.findall('input'):
        bad_ins.remove(i)
    # ET.dump(n)

'''
STEP 2: add correct references to input/output links in node structures
'''
for l in links.iter('link'):
    input_id = l.find('begin').attrib['node_id']
    input_node = nodes.find(".//node[@id='"+input_id+"']")
    ET.SubElement(input_node.find('outputs'), 'output', {'link_id':l.attrib['id']})
    # ET.dump(input_node)


