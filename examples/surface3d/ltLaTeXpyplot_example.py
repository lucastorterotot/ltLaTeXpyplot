#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot.core as lt

# Create figure
fig = lt.ltFigure(name='fig', page_width_cm=26, width_frac=1)

# Define what to plot
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
def z(x, y):
    return np.sin(np.sqrt(x**2+y**2))

surf = lt.ltPlotSurf(X, Y, z_fct=z, cmap='coolwarm', alpha=1, use_cmap=True, norm_xyz=False)
    
# Define graphs
fig.addgraph('graph1', show_cmap_legend=True, projection='3d')

# Insert objects in graphs
fig.addplot(surf, 'graph1')

# Save figure
fig.save(format='pdf')
