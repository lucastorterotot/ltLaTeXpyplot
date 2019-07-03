#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot as lt

# Create figure
fig = lt.ltFigure(name='RMN-fig')

# Define what to plot
# signals = [signal1, signal2, ...]
# signalX = [deltaX, integral, multiplet, Js(Hz)]
signals = [[4.999,3,[4],[6.40]],[1.374,9,[2],[5.85]]]

spectrum = lt.ltPlotNMR(delta_min=.5, delta_max=6, Freq_MHz=90, show_integral=True)
for signal in signals:
    spectrum.addsignal(signal[0], signal[1], signal[2], signal[3])

# Define graphs
fig.addgraph('graph1')

# Insert objects in graphs
fig.addplot(spectrum, 'graph1')

# Save figure
fig.save(format='pdf')
