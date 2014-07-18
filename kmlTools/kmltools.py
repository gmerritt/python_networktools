__author__ = 'leahanderson'
import os
from zipfile import ZipFile
from tempfile import mkstemp
from kmlobjects import KML
# from xml.etree.ElementTree import ElementTree as ET


def convert_network_to_kml(networkobj):
    #set up kmz document (define styles)
    k = KML(networkobj.file_location+networkobj.name)

    d_desc = 'kml as translated from scenario file %s' %(networkobj.name)
    d = setup_kdoc(k, networkobj.name, d_desc)

    nodes = k.createFolder('Nodes')
    links = k.createFolder('Links')

    for nid, ninfo in networkobj.node_dict.iteritems():
        desc = 'Node ' + nid
        print ninfo['type']
        if ninfo['type']=="Signalized Intersection":
            n = k.createPlacemark(nid, float(ninfo['position'][0]), float(ninfo['position'][1]), desc, 'intersection_node')
        elif ninfo['type']=="Terminal":
            n = k.createPlacemark(nid, float(ninfo['position'][0]), float(ninfo['position'][1]), desc, 'terminal_node')
        else:
            n = k.createPlacemark(nid, float(ninfo['position'][0]), float(ninfo['position'][1]), desc, 'intermediate_node')
        nodes.appendChild(n)
    d.appendChild(nodes)

    for lid, linfo in networkobj.link_dict.iteritems():
        #TODO: make this correct!!
        description = 'Link ' + lid + ': ' + linfo['lanes'] + ' lanes , ' + linfo['length'] + ' meters'
        coords=[]
        for p in linfo['position']:
            coords.append((float(p[0]),float(p[1]),0.0))
        l = k.createPlacemark(lid, desc=description, style='empty_link', altMode='clampedToGround')
        l.appendChild(k.createLineString(coords, 'clampedToGround'))
        links.appendChild(l)
    d.appendChild(links)
    k.root.appendChild(d)
    write_kmz(k, networkobj.file_location + '/' + networkobj.name.split('.')[0]+'.kmz')
    return k


def convert_data_to_kml(networkobj, data):
    return None


def setup_kdoc(kobj, dname, desc):
    doc = kobj.createDocument(dname, desc)
    label_size=0 #change this to \in [0,1] to make object labels show up in kmz files
    # define node styles
    doc.appendChild(kobj.createStyle('intersection_node', [kobj.createIconStyle(1.2, kobj.createIcon('../map_icons/signalized_intersection.png')),  kobj.createLabelStyle(label_size)]))
    doc.appendChild(kobj.createStyle('terminal_node', [kobj.createIconStyle(0.5, kobj.createIcon('../map_icons/blue_rounded_square.png')),  kobj.createLabelStyle(label_size)]))
    doc.appendChild(kobj.createStyle('intermediate_node', [kobj.createIconStyle(0.8, kobj.createIcon('../map_icons/shaded_dot.png')),  kobj.createLabelStyle(label_size)]))
    doc.appendChild(kobj.createStyle('empty_link', kobj.createLineStyle('ffffffff', 1)))
    # define link styles
    lwidth = {'red':1, 'green':2}
    for i in lwidth.keys():
        doc.appendChild(kobj.createStyle('freeflow_link_' + i, kobj.createLineStyle('ff00ff00', lwidth[i])))
        doc.appendChild(kobj.createStyle('queueing_link_' + i, kobj.createLineStyle('ff00ffff', lwidth[i])))
        doc.appendChild(kobj.createStyle('full_link_' +i, kobj.createLineStyle('ff0000ff', lwidth[i])))
    return doc


def write_kmz(kml, filename):
    """Write a KML object out to a compressed .kmz file."""
    kmz = ZipFile(filename+".tmp", 'w')
    (tmpfh, tmpname) = mkstemp('.kml', '')#sys.argv[0] )
    tmp = os.fdopen(tmpfh, 'w')
    kml.writePlain(tmp)
    tmp.close()
    kmz.write(tmpname, 'doc.kml')
    for z in kmz.infolist():
        z.external_attr = 0644 << 16L # set file perms
    kmz.close()
    os.unlink(tmpname)
    os.rename(filename+'.tmp', filename)