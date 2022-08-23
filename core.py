#!/usr/bin/python3
class route(object):
    # input:
    # inputBins: list of bin numbers
    # create dictionaries: bins, binItems
    # bins: k: original bin number -> v: modified bin number
    # binItems: k: modified bin number -> v: list of bins
    def __init__(self, inputBins):
        self.bins = {}
        self.binItems = {}
        self.inputBins = inputBins

    # modify bin numbers 
    # map rack number to aisle number
    # map bin numbers to count of bins
    # e.g 
    #   R27-B02 => 13-12
    def binModification(self):
        binModMap = {'A': 0, 'B': 10, 'C': 20, 'D': 30}
        for s in self.inputBins:
            rack = s[1:3]
            rackNum = int(rack) // 2
            formatted = f'{rackNum:02d}-'

            a = s[5:7]
            temp = int(s[5:7])
            if rack == '00':
                temp += 12 if s[4] != 'A' else 0
            else:
                temp += binModMap.get(s[4])
            formatted += f'{temp:02d}'
            self.bins[s] = formatted

    # split sorted modified list of bin by different aisles

    def modBinSplit(self):
        bin_memo = []
        for key in self.bins:
            bin_memo.append(key)
        # code to reverse bin_memo
        bin_memo.sort(reverse=True, key=self.bins.get)

        first = 0
        record = self.bins.get(bin_memo[first])[:2]
        for i in range(1, len(bin_memo)):
            rack_head = self.bins.get(bin_memo[i])[:2]
            if rack_head != record:
                self.binItems[record] = bin_memo[first:i]
                first = i
                record = rack_head
        self.binItems[record] = bin_memo[first:]

    # sort or reverse by last item of previous aisle
    def decideNextOrder(self):
        prekey = None
        for i in reversed(range(0, 14)):
            key = f'{i:02d}'
            if key in self.binItems:
                val = self.binItems.get(key)
                if prekey is None:
                    prekey = key
                else:
                    Item = self.binItems.get(prekey)
                    lastItem = int(self.bins.get(Item[-1])[3:])

                    first = int(self.bins.get(val[0])[3:])
                    second = int(self.bins.get(val[-1])[3:])
                    if abs(lastItem - first) > abs(lastItem - second):
                        self.binItems[key] = list(reversed(val))
                    prekey = key

    # output from dictionary to list of bins with shortest route
    def getFinalSequence(self):
        res = []
        for i in reversed(range(0, 14)):
            key = f'{i:02d}'
            if key in self.binItems:
                val = self.binItems.get(key)
                res += val
        return res

    def test(self):
        binlist = ["R27-A04-XXXXXXX ", "R27-A01-XXXXXXX ", "R26-A03-XXXXXXX ", "R25-B04-XXXXXXX ", "R25-B01-XXXXXXX ",
                   "R25-A01-XXXXXXX ", "R24-C01-XXXXXXX ", "R24-B02-XXXXXXX ", "R23-D04-XXXXXXX ", "R23-C04-XXXXXXX ",
                   "R23-B02-XXXXXXX ", "R22-D01-XXXXXXX ", "R22-C02-XXXXXXX ", "R22-A02-XXXXXXX ", "R01-C04-XXXXXXX ",
                   "R01-C03-XXXXXXX ", "R01-B04-XXXXXXX ", "R01-B02-XXXXXXX ", "R00-B16-XXXXXXX ", "R00-B12-XXXXXXX ",
                   "R00-B11-XXXXXXX ", "R00-A12-XXXXXXX ", "R00-A03-XXXXXXX ", "R00-A02-XXXXXXX ", "R00-A01-XXXXXXX"]
        self.binModification(binlist)
        print(self.bins)
        print()
        self.modBinSplit()
        print(self.binItems)
        print()
        self.decideNextOrder()
        print(self.binItems)
        print()
        ret = self.getFinalSequence()
        print(ret)

    def run(self):
        self.binModification()
        self.modBinSplit()
        self.decideNextOrder()
        return self.getFinalSequence()


if __name__ == '__main__':
    t = route()
    t.test()
