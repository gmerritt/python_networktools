__author__ = 'leahanderson'

import operator


class Trajectory(object):

    def __init__(self, datapoints):
        datapoints.sort(key=operator.itemgetter(3))
        self.id = int(datapoints[0][0])
        self.start = int(datapoints[0][3])
        self.duration = int(datapoints[0][2])*.1  # in seconds
        vtypes = {1:'motorcycle', 2:'car', 3:'truck'}
        self.vehicletype =vtypes[int(datapoints[0][10])]
        self.origin = int(datapoints[0][14])
        self.destination = int(datapoints[0][15])
        self.time = []
        self.x=[]
        self.y=[]
        self.velocity=[]
        self.acceleration=[]
        self.lane=[]
        self.intersection=[]
        self.link=[]
        vdirs = {1:'EB', 2:'NB', 3:'WB', 4:'SB'}
        self.direction=[]
        vmovs = {1:'T', 2:'L', 3:'R'}
        self.movement=[]
        for d in datapoints:
            self.time.append(int(d[3]))
            self.x.append(float(d[4]))
            self.y.append(float(d[5]))
            self.velocity.append(float(d[11]))
            self.acceleration.append(float(d[12]))
            self.lane.append(int(d[13]))
            self.intersection.append(int(d[16]))
            self.link.append(int(d[17]))
            self.direction.append(vdirs[int(d[18])])
            self.movement.append(vmovs[int(d[19])])


    @staticmethod
    def generate_map(self):
        return 0

    def find_link_entry_time(self, link_id, direction):
        #assumes that this vehicle only enters the link once in the given direction!
        linkdir = zip(self.link, self.direction)
        return self.time[linkdir.index([link_id, direction])]

    def find_intersection_entry_time(self, intersection_id, direction=0):
        if direction == 0:
            return self.time[self.intersection.index(link_id)]
        intdir = zip(self.intersection, self.direction)
        return self.time[intdir.index([intersection_id, direction])]

    def get_start_point(self):
        # print self.id
        return [self.start, self.origin, self.link[0], self.direction[0], self.intersection[0], self.movement[0],
                self.x[0], self.y[0]]

    def get_traj_point(self, time_index):
        return [self.time[time_index], self.origin, self.link[time_index], self.direction[time_index],
                self.intersection[time_index], self.movement[time_index], self.x[time_index], self.y[time_index]]
