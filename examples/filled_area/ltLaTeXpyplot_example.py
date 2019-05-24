#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot.core as lt

# Create figure
fig = lt.ltFigure(name='fig')

# Define what to plot
x = np.array([1.0,2.1,3.1,3.9])
y = np.array([2.1,3.9,6.1,7.8])
y2 = np.array([3.0,6.1,8.3,10.5])

fct1 = lt.ltPlotFct(x, y, label='F1', color='C3')
fct2 = lt.ltPlotPts(x, y2, label='F2')

# Define graphs
fig.addgraph('graph1')

# Insert object in plots
fct1.plot(fig, 'graph1')
fct2.plot(fig, 'graph1')

# Fill area
fig.graphs['graph1'].fill_between(x, y, y2, label='Area', color='C2')

# Save figure
fig.save(format='pdf')  
