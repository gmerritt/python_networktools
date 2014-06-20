__author__ = 'leahanderson'


def load_network(scenario_file_name):
    from scenariobjects import ScenarioNetwork
    return ScenarioNetwork(scenario_file_name)


def render_network(network):
    from matplotlib import pyplot as p
    from numpy import arctan2, sin, cos, degrees
    from matplotlib.transforms import offset_copy

    link_dict = network.get_link_dict()
    node_dict = network.get_node_dict()
    end_nodes = {}
    for link_id in link_dict.keys():
        end_nodes[link_id] = [link_dict[link_id]['nodes'][0], link_dict[link_id]['nodes'][-1]]
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
                _lastmarker           = 'x',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 8,
                _lastzorder           = 0,
                ),
        'Street': dict(
                marker          = 'D',
                markeredgecolor = 'g',
                markeredgewidth = 1,
                markerfacecolor = 'g',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 3,
                color           = 'g', #(0.2,0.2,0.7,0.1),
                alpha           = 0.5,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -2,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'b',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'b',
                _firstmarkersize      = 5,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'b',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'b',
                _lastmarkersize       = 3,
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

    fig = p.figure()
    # ax=fig.add_subplot(111,autoscale_on=False,xlim=(minX,maxX),ylim=(minY,maxY))
    ax=fig.add_subplot(111,autoscale_on=True)
    for idx,link_id in enumerate(link_dict.keys()):
        if idx>100:
            break
        try:
            this_link_type=link_dict[link_id]['type']
            start_position = node_dict[link_dict[link_id]['nodes'][0]]['position']
            end_position = node_dict[link_dict[link_id]['nodes'][1]]['position']
            dx=float(end_position[1]) - float(start_position[1])
            dy=float(end_position[0]) - float(start_position[0])
            # begin_xy = [float(link_dict[link_id]['position'][0][1]), float(link_dict[link_id]['position'][0][0])]
            # end_xy = [float(link_dict[link_id]['position'][-1][1]), float(link_dict[link_id]['position'][-1][0])]
            theta = arctan2(dy, dx)
            if theta ==0:
                x_offset = 0
                y_offset = float(link_dict[link_id]['offset'])
            elif degrees(theta)==90:
                x_offset = float(link_dict[link_id]['offset'])
                y_offset = 0
            else:
                x_offset = float(link_dict[link_id]['offset'])/sin(theta)
                y_offset = float(link_dict[link_id]['offset'])/cos(theta)
            trans = offset_copy(ax.transData, x=1.5*x_offset, y=1.5*y_offset, units='dots')
            # print trans
            oldX = None
            oldY = None

            if this_link_type in rendering_rules.keys():
                this_rendering = rendering_rules[this_link_type]
            else:
                this_rendering = rendering_rules['default']

            for pidx, point in enumerate(link_dict[link_id]['position']):
                y = float(point[0])
                x = float(point[1])
                # print [x,y]
                if oldX is None:
                    # first point in road way
                    ax.plot([x],[y],
                        marker          = this_rendering['_firstmarker'],
                        markeredgecolor = this_rendering['_firstmarkeredgecolor'],
                        markeredgewidth = this_rendering['_firstmarkeredgewidth'],
                        markerfacecolor = this_rendering['_firstmarkerfacecolor'],
                        markersize      = this_rendering['_firstmarkersize'],
                        zorder          = this_rendering['_firstzorder'],
                        )
                elif pidx<(len(link_dict[link_id]['position'])-1):
                    ax.plot([oldX,x],[oldY,y],
                        marker          = '',
                        linestyle       = this_rendering['linestyle'],
                        linewidth       = this_rendering['linewidth'],
                        color           = this_rendering['color'],
                        alpha           = this_rendering['alpha'],
                        solid_capstyle  = this_rendering['solid_capstyle'],
                        solid_joinstyle = this_rendering['solid_joinstyle'],
                        zorder          = this_rendering['zorder'],
                        transform = trans
                        )
                    ax.plot([x],[y],
                        marker          = this_rendering['marker'],
                        markeredgecolor = this_rendering['markeredgecolor'],
                        markeredgewidth = this_rendering['markeredgewidth'],
                        markerfacecolor = this_rendering['markerfacecolor'],
                        markersize      = this_rendering['markersize'],
                        color           = this_rendering['color'],
                        alpha           = this_rendering['alpha'],
                        zorder          = this_rendering['markerzorder'],
                        transform = trans
                        )
                else:
                    # last segment in road way
                    ax.plot([oldX,x],[oldY,y],
                        marker          = '',
                        linestyle       = this_rendering['linestyle'],
                        linewidth       = this_rendering['linewidth'],
                        color           = this_rendering['color'],
                        alpha           = this_rendering['alpha'],
                        solid_capstyle  = this_rendering['solid_capstyle'],
                        solid_joinstyle = this_rendering['solid_joinstyle'],
                        zorder          = this_rendering['zorder'],
                        transform = trans
                        )
                oldX = x
                oldY = y
            # last point in road way
            ax.plot([x],[y],
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
    print'Done Plotting'
    ax.autoscale_view()
    p.show()


def animate_network(network, data, data_type='density_car'):
    from matplotlib import pyplot as p
    # from numpy import arctan2, sin, cos, degrees
    # from matplotlib.transforms import offset_copy
    import matplotlib.animation as animation

    link_dict = network.get_link_dict()
    node_dict = network.get_node_dict()
    end_nodes = {}
    for link_id in link_dict.keys():
        end_nodes[link_id] = [link_dict[link_id]['nodes'][0], link_dict[link_id]['nodes'][-1]]
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
                _lastmarker           = 'x',
                _lastmarkeredgecolor  = 'r',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'r',
                _lastmarkersize       = 8,
                _lastzorder           = 0,
                ),
        'Street': dict(
                marker          = 'D',
                markeredgecolor = 'g',
                markeredgewidth = 1,
                markerfacecolor = 'g',
                markersize      = 2,
                linestyle       = '-',
                linewidth       = 3,
                color           = 'g', #(0.2,0.2,0.7,0.1),
                alpha           = 0.5,
                solid_capstyle  = 'round',
                solid_joinstyle = 'round',
                zorder          = -2,
                markerzorder    = 0,
                _firstmarker          = 'x',
                _firstmarkeredgecolor = 'b',
                _firstmarkeredgewidth = 1,
                _firstmarkerfacecolor = 'b',
                _firstmarkersize      = 5,
                _firstzorder          = 1,
                _lastmarker           = 'o',
                _lastmarkeredgecolor  = 'b',
                _lastmarkeredgewidth  = 1,
                _lastmarkerfacecolor  = 'b',
                _lastmarkersize       = 3,
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

    fig = p.figure()
    ax=fig.add_subplot(111,autoscale_on=False,xlim=(minX,maxX),ylim=(minY,maxY))
    # ax=fig.add_subplot(111,autoscale_on=True)
    line, = ax.plot([], [], lw=2)

    def init():
        line.set_data([],[])
        return line
    '''

    1) plot the network as initial state
    2) calculate each of the new states
    3) replot the new states that have changed with 2 lines: red being the queue length
    and another line behind with color corresponding to the number of vehicels in transit

    '''
    def draw_streets(i):
        print i
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
                    # print [x,y]
                    if oldX is None:
                        # first point in road way
                        ax.plot([x],[y],
                            marker          = this_rendering['_firstmarker'],
                            markeredgecolor = this_rendering['_firstmarkeredgecolor'],
                            markeredgewidth = this_rendering['_firstmarkeredgewidth'],
                            markerfacecolor = this_rendering['_firstmarkerfacecolor'],
                            markersize      = this_rendering['_firstmarkersize'],
                            zorder          = this_rendering['_firstzorder'],
                            )
                    elif pidx<(len(link_dict[link_id]['position'])-1):
                        ax.plot([oldX,x],[oldY,y],
                            marker          = '',
                            linestyle       = this_rendering['linestyle'],
                            linewidth       = this_rendering['linewidth'],
                            color           = this_rendering['color'],
                            alpha           = this_rendering['alpha'],
                            solid_capstyle  = this_rendering['solid_capstyle'],
                            solid_joinstyle = this_rendering['solid_joinstyle'],
                            zorder          = this_rendering['zorder'],
                            # transform = trans
                            )
                        ax.plot([x],[y],
                            marker          = this_rendering['marker'],
                            markeredgecolor = this_rendering['markeredgecolor'],
                            markeredgewidth = this_rendering['markeredgewidth'],
                            markerfacecolor = this_rendering['markerfacecolor'],
                            markersize      = this_rendering['markersize'],
                            color           = this_rendering['color'],
                            alpha           = this_rendering['alpha'],
                            zorder          = this_rendering['markerzorder'],
                            # transform = trans
                            )
                    else:
                        # last segment in road way
                        ax.plot([oldX,x],[oldY,y],
                            marker          = '',
                            linestyle       = this_rendering['linestyle'],
                            linewidth       = this_rendering['linewidth'],
                            color           = this_rendering['color'],
                            alpha           = this_rendering['alpha'],
                            solid_capstyle  = this_rendering['solid_capstyle'],
                            solid_joinstyle = this_rendering['solid_joinstyle'],
                            zorder          = this_rendering['zorder'],
                            # transform = trans
                            )
                    oldX = x
                    oldY = y
                # last point in road way
                ax.plot([x],[y],
                            marker          = this_rendering['_lastmarker'],
                            markeredgecolor = this_rendering['_lastmarkeredgecolor'],
                            markeredgewidth = this_rendering['_lastmarkeredgewidth'],
                            markerfacecolor = this_rendering['_lastmarkerfacecolor'],
                            markersize      = this_rendering['_lastmarkersize'],
                            zorder          = this_rendering['_lastzorder'],
                        )
            except KeyError:
                pass
            # if idx%100 == 0:
            #     print idx
        print'Done Plotting'

    anim = animation.FuncAnimation(fig, draw_streets, init_func=init, frames=10, interval=10, blit=True)
    # anim.save('basic_animation.mp4', fps=30)
    p.show()



def process_beats_output(network, output_prefix):
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