__author__ = 'leahanderson'

'''
    these functions are used to read in and manipulate/analyze NGSIM trajectory data
    The idea is to FIRST FILTER into the subset of trajectories you are interested in, and then convert into a
    human-readable trajectory object type -- because the whole trajectory files are huge, and the conversion process is
    relatively slow... so first run read_trajectory_file, then do filtering, then convert the resulting list of data
    points into Trajectory objects!
'''



def read_trajectory_file(trajectoryfile):
    #THIS READS IN THE TRAJECTORY FILES. IT IS THE FIRST THING YOU NEED TO DO.
    trajlist=[]
    with open(trajectoryfile) as inputfile:
        for line in inputfile:
            trajlist.append(line.split())
    return trajlist



'''
    the following operations are intended to run on lists generated by read_trajectory.
    they typically return subsets of a trajectory list, actually as a list of list to be
    consistent with the output of the read_trajectory_data function.
'''

def filter_by_link(tlist, link, intersection=0):
    #you can filter by intersection by setting link = 0 and setting intersection value
    link_trajs=[]
    for tl in tlist:
        for dp in tl:
                if dp[16] == intersection and dp[17] == link:
                    link_trajs.append(dp)
    return [link_trajs]


def filter_by_origin(tlist, origin):
    origin_trajs=[]
    for tl in tlist:
        for dp in tl:
            if dp[14] == str(origin):
                origin_trajs.append(dp)
    return [origin_trajs]


def filter_by_destination(tlist, destination):
    dest_trajs=[]
    for tl in tlist:
        for dp in tl:
                if dp[14] == str(destination):
                    dest_trajs.append(dp)
    return [dest_trajs]



'''
    once you have culled down the total list of trajectories into one that is more managable, use these functions to
    transform this list into Trajectory objects and manipulate these objects
'''
from ngsimobjects import Trajectory

def convert_list_to_trajectories(tlist):
    vehs={}
    for tl in tlist:
        for dp in tl:
            # print(dp)
            # time.sleep(1)
            # print(dp[0])
            id = int(dp[0])
            if not vehs.has_key(id):
                vehs[id]=[]
            vehs[id].append(dp)
    # print vehs[id]
    trajectories = []
    for v in vehs.keys():
        trajectories.append(Trajectory(vehs[v]))
    return trajectories

def calculate_demands(trajectories):
    return 0

