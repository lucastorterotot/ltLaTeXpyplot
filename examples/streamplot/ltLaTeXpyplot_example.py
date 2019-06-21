#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot as lt

# Create figure
fig = lt.ltFigure(name='fig', height_width_ratio = 9/7, tight_layout=True)

# Define what to plot
dim=3
size=100
x = np.linspace(-dim, dim, size)
y = np.linspace(-dim, dim, size)
def vx(x, y):
    return -1 - x**2 + y
def vy(x, y):
    return 1 + x - y**2
def speed(x, y):
    return (vx(x, y)**2+vy(x,y)**2)**.5
def lw (X, Y):
    return 5*speed(X,Y)/speed(x,y).max()
Vect_field = lt.ltPlotVectField2d(x, y, vx, vy, norm_xy=False)

seed_points = np.array([[-2, -1, 0, 1, 2, -1], [-2, -1,  0, 1, 2, 2]])
    
# Define graphs
fig.addgraph('graph1', position=421, show_cmap_legend=False, title='Varying Density')
fig.addgraph('graph2', position=422, show_cmap_legend=True, title='Varying Color')
fig.addgraph('graph3', position=423, show_cmap_legend=False, title='Varying Line Width')
fig.addgraph('graph4', position=424, show_cmap_legend=True, title='Controlling Starting Points')
fig.addgraph('graph5', position=212, title='Streamplot with Masking')

# Insert object in plots
Vect_field.plot_streamplot(fig, 'graph1', linewidth=1, density=[0.5,1])

Vect_field.plot_streamplot(fig, 'graph2', color=vx, linewidth=1, cmap='autumn')

Vect_field.plot_streamplot(fig, 'graph3', density=0.6, color='k', linewidth=lw)

Vect_field.plot_streamplot(fig, 'graph4', color=vx, linewidth=2, cmap='autumn', start_points=seed_points.T)
lt.ltPlotPts(seed_points[0], seed_points[1], color='b', marker='o').plot(fig, 'graph4')

mask = np.zeros((size,size), dtype=bool)
X, Y = np.meshgrid(Vect_field.x,Vect_field.y)
mask[40:60, 40:60] = True
U = Vect_field.vx_fct(X, Y)
U[:20, :20] = np.nan
Vect_field.vx_fct = np.ma.array(U, mask=mask)
Vect_field.vy_fct = Vect_field.vy_fct(X,Y)

Vect_field.plot_streamplot(fig, 'graph5', color='r')

fig.graphs['graph5'].graph.imshow(~mask, extent=(-dim, dim, -dim, dim), alpha=0.5, interpolation='nearest', cmap='gray', aspect='auto')
fig.graphs['graph5'].graph.set_aspect('equal')

# Save figure
fig.save(format='pdf')
