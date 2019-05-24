#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot.core as lt

# Create figure
fig = lt.ltFigure(name='fig', tight_layout=True)

# Define what to plot
X = np.arange(-.8, 1, 0.1)
Y = np.arange(-.8, 1, 0.1)
Z = np.arange(-.8, 1, 0.8)

def Vect3d_x(x,y,z):
    return np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
def Vect3d_y(x,y,z):
    return -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
def Vect3d_z(x,y,z):
    return np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) * np.sin(np.pi * z)

def Vect2d_x(x,y):
    return Vect3d_x(x,y,0)
def Vect2d_y(x,y):
    return Vect3d_y(x,y,0)
    
def C_fct(x, y):
    return (Vect2d_x(x,y)**2 + Vect2d_y(x,y)**2)**.5
    
Vtr2D = lt.ltPlotVectField2d(X, Y, Vect2d_x, Vect2d_y, C_fct=C_fct)
Vtr3D = lt.ltPlotVectField3d(X, Y, Z, Vect3d_x, Vect3d_y, Vect3d_z)

# Define graphs
fig.addgraph('g1', position=221)
fig.addgraph('g2', position=223)
fig.addgraph('g3', position=122, projection='3d')

# Insert object in plots
Vtr2D.plot(fig, 'g1')
Vtr2D.plot_fieldline(fig, 'g1', (.2, .4), 0, 10, 100, color='C3')

Vtr2D.use_cmap = True
Vtr2D.plot(fig, 'g2')


Vtr3D.plot(fig, 'g3')
Vtr3D.plot_fieldline(fig, 'g3', (.2, .4, .2), 0, 10, 100, color='C3')

# Save figure
fig.save(format='pdf')
