__author__ = 'leahanderson'


def loadNetwork(scenario_file_name):
    import xml.etree.ElementTree as ET
    tree = ET.parse(scenario_file_name)
    scenario = tree.getroot()
    network = scenario.find('NetworkSet/network')
    nodes = network.find('NodeList')
    links = network.find('LinkList')
    node_dict={}
    for n in nodes.iter('node'):
        print n.attrib['id']
        node_position = n.find('position').find('point')
        node_dict[n.attrib['id']] = {'position':[node_position.attrib['lat'], node_position.attrib['lng']],
                                     'type':n.find('node_type').attrib['name']}
    link_dict={}
    for l in links.iter('link'):
        print l.attrib['id']
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
    return link_dict, node_dict


def renderNetwork(link_dict, node_dict):
    import pylab as p
    print 'Enumerating end nodes.'
    end_nodes = {}
    link_types = {}
    for link_id in link_dict.keys():
        end_nodes[link_id] = [link_dict[link_id]['nodes'][0], link_dict[link_id]['nodes'][-1]]

    print 'Done enumerating end nodes'



    rendering_rules = {
        'Freeway': dict(
                marker          = 'D',
                markeredgecolor = 'b',
                markeredgewidth = 1,
                markerfacecolor = 'b',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 10,
                color           = (0.7,0.7,1.0,0.1),
                alpha           = 1.0,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -1,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'g',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'g',
                _firstmarkersize      = 8,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 8,
                _lastzorder           = 0,
                ),
        'Street': dict(
                marker          = 'D',
                markeredgecolor = 'b',
                markeredgewidth = 1,
                markerfacecolor = 'b',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 6,
                color           = (0.2,0.2,0.7,0.1),
                alpha           = 0.5,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -2,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'g',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'g',
                _firstmarkersize      = 10,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 8,
                _lastzorder           = 0,
                ),
        'primary': dict(
                marker          = 'D',
                markeredgecolor = 'b',
                markeredgewidth = 1,
                markerfacecolor = 'b',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 10,
                color           = (0.7,0.7,1.0,0.1),
                alpha           = 1.0,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -1,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'g',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'g',
                _firstmarkersize      = 8,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 8,
                _lastzorder           = 0,
                ),
        'primary_link': dict(
                marker          = 'D',
                markeredgecolor = 'b',
                markeredgewidth = 1,
                markerfacecolor = 'b',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 8,
                color           = (0.7,0.7,1.0,0.1),
                alpha           = 1.0,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -1,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'g',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'g',
                _firstmarkersize      = 12,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 8,
                _lastzorder           = 0,
                ),
        'secondary': dict(
                marker          = 'D',
                markeredgecolor = 'b',
                markeredgewidth = 1,
                markerfacecolor = 'b',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 6,
                color           = (0.2,0.2,0.7,0.1),
                alpha           = 0.5,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -2,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'g',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'g',
                _firstmarkersize      = 10,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 8,
                _lastzorder           = 0,
                ),
        'secondary_link': dict(
                marker          = 'D',
                markeredgecolor = 'b',
                markeredgewidth = 1,
                markerfacecolor = 'b',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 6,
                color           = (0.2,0.2,0.7,0.1),
                alpha           = 0.5,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -2,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'g',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'g',
                _firstmarkersize      = 10,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 8,
                _lastzorder           = 0,
                ),
        'tertiary': dict(
                marker          = 'D',
                markeredgecolor = 'b',
                markeredgewidth = 1,
                markerfacecolor = 'b',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 4,
                color           = (0.0,0.0,0.7,0.1),
                alpha           = 0.5,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -3,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'g',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'g',
                _firstmarkersize      = 10,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 8,
                _lastzorder           = 0,
                ),
        'tertiary_link': dict(
                marker          = 'D',
                markeredgecolor = 'b',
                markeredgewidth = 1,
                markerfacecolor = 'b',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 4,
                color           = (0.0,0.0,0.7,0.1),
                alpha           = 0.5,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -3,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'g',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'g',
                _firstmarkersize      = 10,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 8,
                _lastzorder           = 0,
                ),
        'residential': dict(
                marker          = 'D',
                markeredgecolor = 'b',
                markeredgewidth = 1,
                markerfacecolor = 'b',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 1,
                color           = (0.1,0.1,0.1,1.0),
                alpha           = 1.0,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -99,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'g',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'g',
                _firstmarkersize      = 10,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 8,
                _lastzorder           = 0,
                ),
        'unclassified': dict(
                marker          = 'D',
                markeredgecolor = (0.5,0.5,0.5),
                markeredgewidth = 1,
                markerfacecolor = (0.5,0.5,0.5),
                markersize      = 2,
                linestyle       = ':',
                linewidth       = 1,
                color           = (0.5,0.5,0.5),
                alpha           = 0.5,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -1,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'g',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'g',
                _firstmarkersize      = 6,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 6,
                _lastzorder           = 0,
                ),
        'default': dict(
                marker          = 'D',
                markeredgecolor = 'b',
                markeredgewidth = 1,
                markerfacecolor = 'b',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 3,
                color           = 'b',
                alpha           = 0.5,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -1,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'b',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'b',
                _firstmarkersize      = 6,
                _firstzorder          = 1,
                _lastmarker     = 'o',
                _lastmarkeredgecolor = 'b',
                _lastmarkeredgewidth = 1,
                _lastmarkerfacecolor = 'b',
                _lastmarkersize      = 6,
                _lastzorder           = 0,
                ),
        }



    for idx,nodeID in enumerate(node_dict.keys()):
        if idx==0:
            minX = float(node_dict[nodeID]['position'][1])
            maxX = float(node_dict[nodeID]['position'][1])
            minY = float(node_dict[nodeID]['position'][0])
            maxY = float(node_dict[nodeID]['position'][0])
        else:
            minX = min(minX,float(node_dict[nodeID]['position'][1]))
            maxX = max(maxX,float(node_dict[nodeID]['position'][1]))
            minY = min(minY,float(node_dict[nodeID]['position'][0]))
            maxY = max(maxY,float(node_dict[nodeID]['position'][0]))

    # minX = float(myMap['bounds']['minlon'])
    # maxX = float(myMap['bounds']['maxlon'])
    # minY = float(myMap['bounds']['minlat'])
    # maxY = float(myMap['bounds']['maxlat'])



    fig = p.figure()
    fig.add_subplot(111,autoscale_on=False,xlim=(minX,maxX),ylim=(minY,maxY))
    for idx,link_id in enumerate(link_dict.keys()):
        if idx>100:
            break
        try:
            this_link_type=link_dict[link_id]['type']

            oldX = None
            oldY = None

            if this_link_type in rendering_rules.keys():
                this_rendering = rendering_rules[this_link_type]
            else:
                this_rendering = rendering_rules['default']



            for pidx, point in enumerate(link_dict[link_id]['position']):
                y = float(point[0])
                x = float(point[1])
                if oldX is None:
                    # first point in road way
                    p.plot([x],[y],
                        marker          = this_rendering['_firstmarker'],
                        markeredgecolor = this_rendering['_firstmarkeredgecolor'],
                        markeredgewidth = this_rendering['_firstmarkeredgewidth'],
                        markerfacecolor = this_rendering['_firstmarkerfacecolor'],
                        markersize      = this_rendering['_firstmarkersize'],
                        zorder          = this_rendering['_firstzorder'],
                        )
                elif pidx<(len(link_dict[link_id]['position'])-1):
                    p.plot([oldX,x],[oldY,y],
                        marker          = '',
                        linestyle       = this_rendering['linestyle'],
                        linewidth       = this_rendering['linewidth'],
                        color           = this_rendering['color'],
                        alpha           = this_rendering['alpha'],
                        solid_capstyle  = this_rendering['solid_capstyle'],
                        solid_joinstyle = this_rendering['solid_joinstyle'],
                        zorder          = this_rendering['zorder'],
                        )
                    p.plot([x],[y],
                        marker          = this_rendering['marker'],
                        markeredgecolor = this_rendering['markeredgecolor'],
                        markeredgewidth = this_rendering['markeredgewidth'],
                        markerfacecolor = this_rendering['markerfacecolor'],
                        markersize      = this_rendering['markersize'],
                        color           = this_rendering['color'],
                        alpha           = this_rendering['alpha'],
                        zorder          = this_rendering['markerzorder'],
                        )
                else:
                    # last segment in road way
                    p.plot([oldX,x],[oldY,y],
                        marker          = '',
                        linestyle       = this_rendering['linestyle'],
                        linewidth       = this_rendering['linewidth'],
                        color           = this_rendering['color'],
                        alpha           = this_rendering['alpha'],
                        solid_capstyle  = this_rendering['solid_capstyle'],
                        solid_joinstyle = this_rendering['solid_joinstyle'],
                        zorder          = this_rendering['zorder'],
                        )
                oldX = x
                oldY = y
            # last point in road way
            p.plot([x],[y],
                        marker          = this_rendering['_lastmarker'],
                        markeredgecolor = this_rendering['_lastmarkeredgecolor'],
                        markeredgewidth = this_rendering['_lastmarkeredgewidth'],
                        markerfacecolor = this_rendering['_lastmarkerfacecolor'],
                        markersize      = this_rendering['_lastmarkersize'],
                        zorder          = this_rendering['_lastzorder'],
                    )
        except KeyError:
            pass
        if idx%100 == 0:
            print idx
    #p.ioff()
    print'Done Plotting'
    p.show()