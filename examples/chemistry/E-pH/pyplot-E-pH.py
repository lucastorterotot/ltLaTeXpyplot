#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot.core as lt

# Create figure
fig = lt.ltFigure(name='EpH-fig')

# Define what to plot
C_tr = 0.01

EpHplt = lt.ltPlotEpH('Fe', C_tr) # uses the EpH data of this package

# Define graphs
fig.addgraph('graph1', x_label='pH', y_label='$E$ ($\\SI{}{V}$)', show_legend=True, legend_on_side=False)

# Insert objects in graphs
fig.addplot(EpHplt, 'graph1')

# Save figure
fig.save(format='pdf')
