#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot.core as lt

# Create figure
fig = lt.ltFigure(name='fig')

# Define what to plot
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

Pie = lt.ltPlotPie(sizes, labels=labels, explode=explode)
    
# Define graphs
fig.addgraph('graph1')

# Insert object in plots
Pie.plot(fig, 'graph1')

# Save figure
fig.save(format='pdf')
