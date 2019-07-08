#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import ltLaTeXpyplot as lt

# Create figure
fig = lt.ltFigure(name='fig')

# Define what to plot
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

function = lt.ltPlotFct(t, s)
    
# Define graphs
fig.addgraph('graph1', x_label='time (s)', y_label='voltage (mV)',
       title='About as simple as it gets, folks', show_grid=True)

# Insert object in plots
function.plot(fig, 'graph1')

# Save figure
fig.save(format='pdf')
