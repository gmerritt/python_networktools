__author__ = 'leahanderson'


import xml.etree.ElementTree as ET

tree = ET.parse('./scenarios/Lshim_v7.xml')
scenario = tree.getroot()
demands = scenario.findall('DemandSet/demandProfile')
for d in demands:
    demandlist = d.find('demand').text.split(',')
    shortenedlist = demandlist[24::]
    d.find('demand').text = ','.join(shortenedlist)



tree.write('./scenarios/Lshim_v8.xml')