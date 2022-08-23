#!/usr/bin/python3
import pandas as pd
import pprint
# import numpy as np
from assign import fulfillment
from core import route

class dataframe(object):
    def __init__(self, data, size):
        self.data = data
        self.size = size
        self.data['BinNumber'] = self.data['BinNumber'].apply(lambda x: [x])
        self.df = self.data.groupby('FulfillmentID', sort=False, as_index=False).agg({'BinNumber': 'sum'})
        
        self.f = fulfillment(self.df['BinNumber'].tolist())

    def sort_order(self):
        job = self.f.assign()
        job_list = list(job.values())
        self.df['joblist'] = job_list
        self.df = self.df.set_index('joblist')
        self.df = self.df.sort_index(ascending = False)

    def get_index(self):
        return self.df.index.tolist()

    def get_grouped_fullfillment(self):
        index_list = self.f.group(self.get_index(), self.size)
        res = []
        for l in index_list:
            temp = self.df.iloc[l].FulfillmentID.tolist()
            res.append(temp)
        return res

    def get_grouped_racks(self):
        index_list = self.f.group(self.get_index(), self.size)
        res = []
        for l in index_list:
            templist = self.df.iloc[l].BinNumber.tolist()
            flat_list = [item for sublist in templist for item in sublist]
            res.append(flat_list)
        # print(res)
        return res

    def plan_route(self):
        assigned_list = self.get_grouped_racks()
        ret = []
        for l in assigned_list:
            print(l)
            r = route(l)
            ret.append(r.run())
        return ret

    def run_without_shortest_plan(self):
        self.sort_order()
        return self.get_grouped_fullfillment()

    def run_with_shortest_plan(self):
        self.sort_order()
        return self.plan_route()

if __name__ == "__main__":
    data = pd.read_csv('~/AI-LAB/Warehouse/unittest.csv')
    # data = pd.read_excel('Warehouse/5.1-8.4 Fulfillment.xlsx')
    d = dataframe(data,5)
    d.sort_order()
    # pprint.pprint(d.get_grouped_fullfillment())
    lines = d.get_grouped_fullfillment()
    # print(lines)
    print(d.plan_route())
    print("*******************************************")
    print(d.plan_route())
    # with open('unittest-1day-id.txt', 'w') as f:
    # with open('unittest-1day-aisle.txt', 'w') as f:
    # with open('unittest-3month-id.txt', 'w') as f:
    # # with open('unittest-3month-aisle.txt', 'w') as f:
    #     for line in lines:
    #         f.write(f'{line}\n')