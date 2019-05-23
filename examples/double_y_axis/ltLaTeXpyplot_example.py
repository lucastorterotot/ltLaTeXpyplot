#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot.core as lt

# Create figure
fig = lt.ltFigure(name='fig', tight_layout=True)

# Define what to plot
t = np.arange(0.01, 10.0, 0.01)
s1 = np.exp(t)
s2 = np.sin(2 * np.pi * t)

# Define graphs
fig.addgraph('graph1', x_label='time (s)', y_label='exp')
fig.addtwingraph('graph2', 'graph1', y_label='sin', axis='x')

# Insert object in plots
exp = lt.ltPlotFct(t, s1, color='b')
sin = lt.ltPlotPts(t, s2, color='r', marker='.')

# Add fit line
sin.plot(fig, 'graph2')
exp.plot(fig, 'graph1')

ax1 = fig.graphs['graph1'].graph
ax1.set_ylabel(fig.graphs['graph1'].y_label, color='b')
ax1.tick_params('y', colors='b', which='major')
ax1.tick_params('y', colors='b', which='minor')
ax2 = fig.graphs['graph2'].graph
ax2.set_ylabel(fig.graphs['graph2'].y_label, color='r')
ax2.tick_params('y', colors='r', which='major')
ax2.tick_params('y', colors='r', which='minor')

# Save figure
fig.save(format='pdf')  
