#!/usr/bin/env python3
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
fig.addgraph('graph1', show_cmap_legend=True, position=211, title='Scalar field plot')
fig.addgraph('graph2', show_cmap_legend=True, position=212, title='Scalar field plot contourf')
cmap = 'PiYG'

# Insert object in plots
field = lt.ltPlotScalField(x, y, z_fct=z_fct, norm_xy=False, cmap=cmap, Nlevels=15)
field.plot(fig, 'graph1')
field.plot_contourf(fig, 'graph2')

# Save figure
fig.save(format='pdf')
