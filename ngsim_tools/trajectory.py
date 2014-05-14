__author__ = 'leahanderson'


class Trajectory:
    def __init__(self, datapoints):
        datapoints.sort(key=operator.itemgetter(3))
        self.id = datapoints[0][0]
        self.start = datapoints[0][3]
        self.duration = datapoints[0][2]*.1  # in seconds
        vtypes = {1:'motorcycle', 2:'car', 3:'truck'}
        self.vehicletype =vtypes[datapoints[0][10]]
        self.origin = datapoints[0][14]
        self.destination = datapoints[0][15]
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
            self.time.append(d[3])
            self.x.append(d[4])
            self.y.append(d[5])
            self.velocity.append(d[11])
            self.acceleration.append(d[12])
            self.lane.append(d[13])
            self.intersection.append(d[16])
            self.link.append(d[17])
            self.direction.append(vdirs[d[18]])
            self.movement.append(vmovs[d[19]])

    def generate_map(self):
        return 0


    def find_link_entry_time(self, link_id):
        return 0

    def find_intersection_entry_time(self, intersection_id):
        return 0