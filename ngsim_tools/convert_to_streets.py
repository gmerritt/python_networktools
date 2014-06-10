import xml.etree.ElementTree as ET

tree = ET.parse('Lshim_v5_TEST.xml')
scenario = tree.getroot()
networkxml=scenario.find('NetworkSet').find('network')
link_set = networkxml.find('LinkList')

for l in link_set:
    l.find('link_type').attrib['name']='Street'
    l.find('link_type').attrib['id']='11'


tree.write("Lshim_v5_TEST.xml")