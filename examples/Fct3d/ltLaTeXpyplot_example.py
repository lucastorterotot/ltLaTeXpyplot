#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot as lt

# Create figure
fig = lt.ltFigure(name='fig')

# Define what to plot
time = np.linspace(0,100,100)
x = np.sin(time/10)
y = np.cos(time/10)
z = time/time.max()

fct = lt.ltPlotFct3d(x, y, z, label='F1', color='C3')

# Define graphs
fig.addgraph('graph1', projection='3d')

# Insert object in plots
fct.plot(fig, 'graph1')

# Save figure
fig.save(format='pdf')  
