#!/usr/bin/python3
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque
import heapq
import pandas as pd
import numpy as np
from itertools import cycle

R_AISLE = [3, 6]

class fulfillment(object):
    # intput: 
    # bins: list of bin numbers from one single fulfillment
    # nums: number of pickers of the day
    # mode: s or d
    # s: static span of different aisles
    # d: dynamic spans
    def __init__(self, bins, mode = 's'):
        self.bins = bins
        self.__file = 'Warehouse/lastyear.csv'
        if mode == 'd': self.__create_map()
        else: self.FINAL_ARRAY = [3] * 14
        self.joblist = defaultdict(list)
        
    # create dynamic span array
    def __create_map(self):
        data = pd.read_csv(self.__file)
        # print(data)
        data.Aisle = [self.__mod(bin) for bin in data.Aisle]
        newdata = data.groupby(['Aisle'], as_index=False, sort=False).agg('sum')
        # print(newdata)
        total = np.array(newdata.Fulfillment)
        target = 2 * np.mean(total)
        self.FINAL_ARRAY = [0] * 14
        for i in range(len(self.FINAL_ARRAY)):
            temp = i
            cnt = total[i]
            while cnt < target and temp < 13:
                temp += 1
                cnt += total[temp]
            self.FINAL_ARRAY[i] = temp - i
        self.FINAL_ARRAY.reverse()

    # modification of bin number
    # from rack to aisle
    # e.g. 
    #   R27-XXXXX => 13 
    #   R01-XXXXX => 0
    def __mod(self, bin):
        return int(bin[1:3]) // 2
        
    # # classification of fulfillment to serial 1,2 or 3
    # # for future assigning
    # def classify(self, bins):
    #     temp = [self.__mod(bin) for bin in bins]
    #     bin_max = max(temp)
    #     ret = [0, 13-bin_max]
    #     if bin_max - min(temp) <= self.FINAL_ARRAY[bin_max]:
    #         ret[0] = 1
    #     elif bin_max - min(temp) <= 2 * self.FINAL_ARRAY[bin_max]:
    #         ret[0] = 2
    #     else:
    #         ret[0] = 3
    #     return ret

    # # assign picking orders to different pickers
    # def assign(self, nums=1):
    #     for i, bins in enumerate(self.bins):
    #         self.joblist[i].extend(self.classify(bins))
    #     # print(self.joblist)
    #     # for x, y in zip(sorted(self.joblist.keys(), key = self.joblist.get), cycle(list(range(nums)))):
    #     #     self.joblist[x].append(y)
    #     return self.joblist
    def classify(self, bins):
        temp = [self.__mod(bin) for bin in bins]
        bin_max = max(temp)
        bin_min = min(temp)
        ret = [bin_max, bin_min]
        # if bin_max - bin_min <= self.FINAL_ARRAY[bin_max]:
        #     ret[0] = 1
        # elif bin_max - bin_min <= 2 * self.FINAL_ARRAY[bin_max]:
        #     ret[0] = 2
        # else:
        #     ret[0] = 3
        return ret

    # assign picking orders to different pickers
    def assign(self):
        for i, bins in enumerate(self.bins):
            self.joblist[i].extend(self.classify(bins))
        # for x, y in zip(sorted(self.joblist.keys(), key = self.joblist.get), cycle(list(range(nums)))):
        #     self.joblist[x].append(y)
        # print(self.joblist)
        return self.joblist

    # r: numbr of aisle to split
    def group(self, joblist, GROUP_SIZE = 5):
        # print(joblist)
        s1 = list(range(len(joblist)))
        s2 = []
        res = []
        g = deque([])
        temp = []
        for r in R_AISLE:
            while s1:
                if len(g) < GROUP_SIZE:
                    if g and joblist[s1[0]][0] < joblist[g[0]][0] - r:
                        heapq.heappush(s2, g.popleft())
                        while temp:
                            heapq.heappush(s1, temp.pop())
                        continue
                        
                    ful = heapq.heappop(s1)
                    binMax, binMin = joblist[ful]
                    
                    if self.__valid(r, binMax, binMin):
                        if g:
                            headMax = joblist[g[0]][0]
                            if self.__valid_next(headMax, r, binMax, binMin):
                                g.append(ful)
                            else:
                                temp.append(ful)
                        else:
                            g.append(ful)
                    else:
                        heapq.heappush(s2, ful)
                else:
                    res.append(list(g.copy()))
                    g.clear()
                    while temp:
                        heapq.heappush(s1, temp.pop())
            while g:    
                heapq.heappush(s2, g.pop())
            while temp:
                heapq.heappush(s2, temp.pop())
            s1, s2 = s2, s1
        s1.sort()
        res.extend([s1[i:i + GROUP_SIZE] for i in range(0, len(s1), GROUP_SIZE)])
        return res
        
    def __valid(self, range, binMax, binMin):
        return (binMax-binMin) <= range
    
    # headMax 每组第一个，即该组标准值的Bin_max
    def __valid_next(self, headMax, range, binMax, binMin):
        return headMax >= binMax >= binMin >= (headMax - range)


if __name__ == "__main__":
    binlist = [[ "R27-A01-XXXXXXX ", "R26-A03-XXXXXXX ", "R25-B04-XXXXXXX "], ["R26-A01-XXXXXXX ","R00-B11-XXXXXXX ", "R00-A12-XXXXXXX "],[ "R25-A01-XXXXXXX ", "R25-A03-XXXXXXX ", "R24-B04-XXXXXXX "], ["R23-C04-XXXXXXX ","R13-D01-XXXXXXX "]]
    f1 = fulfillment(binlist)
    # f2 = fulfillment(binlist[1], -1)
    # f3 = fulfillment(binlist[2], -1)
    f_d = fulfillment(binlist, mode='d')

    # should return 1
    job = f1.assign(2)
    print(job)
    print(sorted(job.keys(), key=job.get))
    # # should return 2
    # print(f2.classify())
    # # should return 3
    # print(f3.classify())
    # should print ordered map
    # print(f_d.FINAL_ARRAY)