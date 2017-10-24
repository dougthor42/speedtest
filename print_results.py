#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from bashplotlib.scatterplot import plot_scatter
from ascii_graph import Pyasciigraph


data = pd.read_csv('results.csv')

download = data['Download (bits/s)'] / 1e6
upload = data['Upload (bits/s)'] / 1e6
ping = data['Ping (ms)']

#  print(ping.describe())
#  print(download.describe())
#  print(upload.describe())

def hist(data, label):
    count, division = np.histogram(data, bins=5)
    hist_data = [(str(d), c) for d, c in zip(division, count)]
    graph = Pyasciigraph()
    for line in graph.graph(label, hist_data):
        print(line)
    print()


# A histogram of Ping
hist(ping, 'Ping')
hist(download, 'Download (Mbits/s)')
hist(upload, 'Upload (Mbits/s)')


#  plot_scatter(f=zip(range(6), ping), xs=None, ys=None, size=50, pch='x', colour='red', title='ping')