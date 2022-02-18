#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tempfile
import numpy as np
import pandas as pd
from bashplotlib.scatterplot import plot_scatter
from ascii_graph import Pyasciigraph


data = pd.read_csv("results.csv")

download = data["Download (bits/s)"] / 1e6
upload = data["Upload (bits/s)"] / 1e6
ping = data["Ping (ms)"]
timestamps = pd.to_datetime(data["Timestamp"])

#  print(ping.describe())
#  print(download.describe())
#  print(upload.describe())


def reject_outliers(data, m=5.189):
    """https://stackoverflow.com/a/16562028"""
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0
    cleaned = data[s < m]
    outliers = data[s > m]
    return cleaned, outliers


def hist(data, label):
    data, outliers = reject_outliers(data)
    outlier_msg = "{} outliers rejected: {}"
    outlier_str = ["{:.3f}".format(x) for x in sorted(list(outliers))]
    #  print(outlier_msg.format(len(outliers), outlier_str))
    count, division = np.histogram(data, bins=8)
    hist_data = [(str(d), c) for d, c in zip(division, count)]
    graph = Pyasciigraph()
    for line in graph.graph(label, hist_data):
        print(line)
    print()


def scatter(x_data, y_data, title, n_points=None):
    """
    x_data: iterable of floats
        X data to plot
    y_data: iterable of floats
        Y data to plot
    title: string
        Title of the graph
    n_points: int
        How many of points (most recent) to plot. If None, plot all.
    """
    # bashplotlib.scatter.plot_scatter only accepts **files** (well, the pypi
    # release only accepts files. [PR43](https://github.com/glamp/bashplotlib/pull/43)
    # was merged but not released on pypi.
    # So we fake it. The code for `plot_scatter` will call `open(xs)`, so we just
    # write things to a temp file. /shrug.

    x_stream = tempfile.NamedTemporaryFile()
    y_stream = tempfile.NamedTemporaryFile()

    for i, ts in enumerate(x_data[-n_points:]):
        # timestamps are pd.datetime64 objects which store the number of
        # nanoseconds since the Unix epoch in the `value` attribute.
        ns = ts.value
        ms = ts.value / 1000
        x_stream.write((str(i) + "\n").encode("utf-8"))
    x_stream.seek(0)

    for yval in y_data[-n_points:]:
        y_stream.write((str(yval) + "\n").encode("utf-8"))
    y_stream.seek(0)

    plot_scatter(
        f=None,
        xs=x_stream.name,
        ys=y_stream.name,
        size=20,
        pch="x",
        colour="red",
        title=title,
    )

    # bashplotlib does not close files...
    x_stream.close()
    y_stream.close()


# A histogram of Ping
hist(ping, "Ping")
hist(download, "Download (Mbits/s)")
hist(upload, "Upload (Mbits/s)")

n = 10
scatter(timestamps, download, "download", n)

# Yeah, there's a better way to do this but I don't care right now.
print(f"last {n} download points:")
last_n_data = data.tail(n).loc[:, ["Timestamp", "Download (bits/s)", "Upload (bits/s)"]]
last_n_data["Download (bits/s)"] = last_n_data["Download (bits/s)"] / 1e6
last_n_data["Upload (bits/s)"] = last_n_data["Upload (bits/s)"] / 1e6
last_n_data.rename(
    columns={
        "Download (bits/s)": "Download (Mbits/s)",
        "Upload (bits/s)": "Upload (Mbits/s)",
    },
    inplace=True,
)
print(last_n_data)
