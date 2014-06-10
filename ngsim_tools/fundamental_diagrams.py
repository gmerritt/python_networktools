#!/usr/bin/env python
__author__ = 'leahanderson'
import xml.etree.ElementTree as ET

tree = ET.parse('Lshim_v5_SignalController_demand_splits.xml')
scenario = tree.getroot()
networkxml=scenario.find('NetworkSet').find('network')
link_set = networkxml.find('LinkList')



fd_set = ET.SubElement(scenario, 'FundamentalDiagramSet')
fd_set.attrib={'project_id':'-1', 'id':'-1'}

for l in link_set:
    link_id = l.attrib['id']
    fd_profile = ET.SubElement(fd_set, 'FundamentalDiagramProfile')
    fd_profile.attrib = {'id':link_id, 'link_id':link_id}
    fD = ET.SubElement(fd_profile, 'fundamentalDiagram')
    fD.attrib = {'id':'1', 'capacity':'0.47222', 'congestion_speed':"7.7548", 'free_flow_speed':"15.8324"}


tree.write("Lshim_v5_SignalController_demand_splits_fd.xml")





