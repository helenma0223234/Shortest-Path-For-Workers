#!/usr/bin/python3
from flask import Flask, request, jsonify
import pandas as pd
from core import route
from data import dataframe
import re

app = Flask(__name__)
pattern = r"^R\d{2}-[A-D]\d{2}-\d{5}\d*"

@app.route('/test', methods=['GET'])
def test():
    return 'Server Ok.'

@app.route('/shortestRoute', methods=['GET', 'POST'])
def routeAPI():
    if request.method == 'POST':
        # try:
        content = request.get_json()
        passed = []
        v = content['BinNumber']
        bins = []
        for _ in v:
            if re.search(pattern, _):
                bins.append(_.strip())
            else:
                passed.append(_.strip())
        r = route(bins)
        ret = r.run()

        try:
            map = jsonify({'route': mapping(ret, True), 'unsort': mapping(passed, False)})
            return map
        except:
            return 'Please parse in correct json form'
    else:
        return 'Please use post method and parse json in body as input.'

@app.route('/fulfillmentGrouping', methods=['GET', 'POST'])
def group():
    if request.method == 'POST':
        try:
            content = request.get_json()
            df = pd.DataFrame(content['Fulfillments'])
            d = dataframe(df, content['GroupSize'])
            ret = d.run_with_shortest_plan()
            return jsonify([{"Group": line, "GroupID": i} for i, line in enumerate(ret)])
        except:
            return 'Please parse in correct json form'
    else:
        return 'Please use post method and parse json in body as input.'


def mapping(li, flag):
    return [{'BinNumber': bins, 'Sort': i} for i, bins in enumerate(li)] if flag else [{'BinNumber': bins, 'Sort': None}
                                                                                       for i, bins in enumerate(li)]


if __name__ == '__main__':
    app.run()
