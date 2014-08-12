#This corresponds to Lankershim network v19...
link_ids=[1, 2, 3, 4, 5]
intersection_ids=[1, 2, 3, 4]
signal_ids=[87,88,89,89]
origin_ids=[101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]
destination_ids=[201, 203, 204, 205, 206, 207, 208, 209, 210, 211]
driveways=[106,206,104,204]
# time_range=[1118935680200, 1118936800600] #FIRST HALF
# time_range=[1118936700000, 1118937747000] #SECOND HALF
# time_range=[1118935680200, 1118937747000]
time_range=[1118935680000, 1118937747000] #TOTAL. These timestamps are in local time...
time_range=[1118935800000, 1118937600000] #0830-0900 ONLY 
data_to_scenario = {
                    1: { '2SB':{'T': [1], 'R': None, 'L': None}, 
                         '101':{'T':[10], 'R': None, 'L': None},
                         '102':{'T':None, 'R': [8], 'L':[7]}       
                    },
                    2: { '2NB':{'T':[6,38,17], 'R':[39], 'L':[31,17]}, 
                         '3SB':{'T':[45,40], 'R':[47,46], 'L':[44]},
                         '103':{'T':[3] , 'R': [11], 'L':[2] },
                         '111':{'T':[22] , 'R':[20] , 'L':[21] }
                    },
                    3: { '3NB':{'T':[32,18,60], 'R':[15], 'L':[16,60]}, 
                         '4SB':{'T':[33,35,34], 'R':[37], 'L':[36,34]},
                          '105':{'T': [26], 'R': [24], 'L':[25] },
                          '110':{'T':[30] , 'R':[28] , 'L':[27] }    
                    },
                    4: { '4NB':{'T':[14,61,5], 'R':[13], 'L':[4,5]},
                         '108':{'T': [48], 'R':[51] , 'L':[50] },
                         '107':{'T': [52], 'R':[53] , 'L':[54]},
                         '109':{'T': [56], 'R':[57] , 'L':[58]}    
                    } 
}
#for network v5-v9, these are the output linkids that EXIT at the corresponding ngsim intersections:
output_to_scenario = {
                      1: { '201':{'T': [9], 'R': None, 'L': None}    
                      },
                      2: { '211':{'T':[19] , 'R': None, 'L':None },
                           '203':{'T':[12] , 'R':None , 'L':None }
                      },
                      3: { '210':{'T': [29], 'R': None, 'L':None },
                           '205':{'T': [23] , 'R':None , 'L':None }    
                      },
                      4: { '208':{'T':[49], 'R':None, 'L':None},
                           '209':{'T': [59], 'R':None , 'L':None},
                           '207':{'T': [55], 'R':None , 'L':None}
                      }
}
shared_lanes = {17:{'T':6, 'L':31}, 46:{'T':45,'R': 47}, 60:{'T':32, 'L':16}, 34:{'T':35, 'L':36}, 5:{'T':14,'L':4}}