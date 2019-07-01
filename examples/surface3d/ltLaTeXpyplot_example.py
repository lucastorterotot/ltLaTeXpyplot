#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot as lt

# Create figure
fig = lt.ltFigure(name='fig', page_width_cm=26, width_frac=.6, height_width_ratio=1)

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

################################################################################

# Create figure
fig2 = lt.ltFigure(name='fig2', height_width_ratio=.5, tight_layout=True)

# Define what to plot
X = np.arange(-3, 3, 0.125)
Y = np.arange(-3, 3, 0.125)

def z_fct(X, Y):
    return ( np.exp(-X**2 - Y**2) - np.exp(-(X - 1)**2 - (Y - 1)**2)) * 2

def C_fct(x, y):
    return x-y

surf1 = lt.ltPlotSurf(X, Y, z_fct=z_fct, C_fct=C_fct, norm_xyz=False, use_cmap=True)
surf2 = lt.ltPlotSurf(X, Y, z_fct=z_fct, C_fct=C_fct, norm_xyz=False, use_cmap=True, linewidth=.5, alpha=1)
    
# Define graphs
fig2.addgraph('graph1', position=121, projection='3d', show_cmap_legend=True, cmap_label='$x-y$')
fig2.addgraph('graph2', position=122, projection='3d', show_cmap_legend=True, cmap_label='$x-y$')

# Insert objects in graphs
fig2.addplot(surf1, 'graph1')
fig2.addplot(surf2, 'graph2')


# Save figure
fig2.save(format='pdf')
