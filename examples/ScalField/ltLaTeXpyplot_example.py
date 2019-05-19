#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot.core as lt

# Create figure
fig = lt.ltFigure(name='fig', tight_layout=True, height_width_ratio=.725)

# Define what to plot
# make these smaller to increase the resolution
dx = 0.05
dy = dx

# generate 2 2d grids for the x & y bounds
x = np.arange(1,5,dx)
y = np.arange(1,5,dy)

def z_fct(x, y):
    return np.sin(x)**10 + np.cos(10 + y*x) * np.cos(x)
    
# Define graphs
fig.addgraph('graph1', show_cmap_legend=True, position=221, title='Scalar field plot')
fig.addgraph('graph2', show_cmap_legend=False, position=222, projection='3d', title='Scalar field plot in 3d')
fig.addgraph('graph3', show_cmap_legend=True, position=223, title='Scalar field plot contourf')
fig.addgraph('graph4', show_cmap_legend=False, position=224, title='Scalar field plot contour')
cmap = 'PiYG'

# Insert object in plots
field = lt.ltPlotScalField(x, y, z_fct=z_fct)
field.plot(fig, 'graph1')
field.plot(fig, 'graph2')
field.plot_contourf(fig, 'graph3')
field.plot_contour(fig, 'graph4')

# Save figure
fig.save(format='pdf')
