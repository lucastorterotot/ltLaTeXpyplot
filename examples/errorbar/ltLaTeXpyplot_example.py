#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot as lt

# Create figure
fig = lt.ltFigure(name='fig', tight_layout=True, height_width_ratio=.725)

# Define what to plot
# example data
x = np.arange(0.1, 4, 0.5)
y = np.exp(-x)

# example error bar values that vary with x-position
error = 0.1 + 0.2 * x

# Define graphs
fig.addgraph('graph1', position=211, title='variable, symmetric error', x_ticks = False)
fig.addgraph('graph2', position=212, title='variable, asymmetric error',
             share_x='graph1', y_scaling = 'log')

# Insert object in plots
pts1 = lt.ltPlotPts(x, y, yerr = error, marker='o')
fct1 = lt.ltPlotFct(x, y)
pts1.plot(fig, 'graph1')
fct1.plot(fig, 'graph1')

lower_error = 0.4 * error
upper_error = error
asymmetric_error = [lower_error, upper_error]

fct2 = lt.ltPlotPts(x, y, xerr = asymmetric_error, marker='o')
fct2.plot(fig, 'graph2')

# Save figure
fig.save(format='pdf')
