#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot as lt

# Create figure
fig1 = lt.ltFigure(name='fig1')
fig2 = lt.ltFigure(name='fig2')

# Define what to plot
time = np.linspace(0,100,100)
x = np.sin(time/10)
y = np.cos(time/10)
z = time/time.max()

fct1 = lt.ltPlotFct3d(x, y, z, label='F1', color='C3', norm_xyz=True)
fct2 = lt.ltPlotFct3d(x, y, z, label='F1', color='C3', norm_xyz=False)

# Define graphs
fig1.addgraph('graph1', projection='3d')
fig2.addgraph('graph1', projection='3d')

# Insert object in plots
fct1.plot(fig1, 'graph1')
fct2.plot(fig2, 'graph1')

# Save figure
fig1.save(format='pdf')
fig2.save(format='pdf')
