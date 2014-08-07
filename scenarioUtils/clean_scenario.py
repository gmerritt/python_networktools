#!/usr/bin/env python
__author__ = 'leahanderson'
import xml.etree.ElementTree as ET
import sys

scenario_file = sys.argv[1]
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

'''
STEP 2: add correct references to input/output links in node structures, and remove all fields
from link definitions that should be automatically regenerated
'''
for l in links.iter('link'):
    input_id = l.find('begin').attrib['node_id']
    input_node = nodes.find(".//node[@id='"+input_id+"']")
    ET.SubElement(input_node.find('inputs'), 'input', {'link_id':l.attrib['id']})
    output_id = l.find('end').attrib['node_id']
    output_node = nodes.find(".//node[@id='"+output_id+"']")
    ET.SubElement(output_node.find('outputs'), 'output', {'link_id':l.attrib['id']})
    for s in ['position', 'shape', 'roads']:
        a=l.find(s)
        if a is not None:
            l.remove(a)

tree.write(scenario_file.split('.')[-2] +'_fixed.xml')