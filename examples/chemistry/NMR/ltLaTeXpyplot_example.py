#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import ltLaTeXpyplot as lt

# Create figure
fig = lt.ltFigure(name='RMN-fig')

# Define what to plot
# signals = [signal1, signal2, ...]
# signalX = [deltaX, integral, multiplet, Js(Hz)]
signals = [
    lt.ltNMRsignal(4.999,3,[4],[6.40]),
    lt.ltNMRsignal(1.374,9,[2],[5.85])
]

spectrum = lt.ltPlotNMR(delta_min=.5, delta_max=6, Freq_MHz=90, show_integral=True)
for signal in signals:
    spectrum.addsignal(signal)

# Define graphs
fig.addgraph('graph1')

# Insert objects in graphs
fig.addplot(spectrum, 'graph1')

# Save figure
fig.save(format='pdf')
