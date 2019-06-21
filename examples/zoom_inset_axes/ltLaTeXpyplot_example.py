#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot as lt

# Create figure
fig = lt.ltFigure(name='fig', height_width_ratio = 1)

# Define what to plot

def get_demo_image():
    import numpy as np
    z = np.load('bivariate_normal.npy')
    # z is a numpy array of 15x15
    return z, (-3, 4, -4, 3)

# make data
Z, extent = get_demo_image()
Z2 = np.zeros([150, 150], dtype="d")
ny, nx = Z.shape
Z2[30:30 + ny, 30:30 + nx] = Z

xs = np.linspace(extent[0], extent[1], Z2.shape[0])
ys = np.linspace(extent[2], extent[3], Z2.shape[1])
zs = Z2

field = lt.ltPlotScalField(xs, ys, z_fct = zs, cmap='viridis')

# Define graphs
fig.addgraph('graph1')

x1, x2, y1, y2 = -1.5, -0.9, -2.5, -1.9
fig.addinsetgraph('graph2', 'graph1', inset_pos = 'upper right', x_min = x1, x_max = x2, y_min = y1, y_max = y2)

# Insert object in plots
field.plot(fig, 'graph1')
field.plot(fig, 'graph2')

# Save figure
fig.save(format='pdf')  
