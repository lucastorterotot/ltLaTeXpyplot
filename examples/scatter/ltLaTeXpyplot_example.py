#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import ltLaTeXpyplot as lt

# Create figure
fig = lt.ltFigure(name='fig', height_width_ratio=.725, width_frac=120.59/112.05)

# Define what to plot
price_data = np.load('goog.npz')['price_data'].view(np.recarray)
price_data = price_data[-250:]  # get the most recent 250 trading days

delta1 = np.diff(price_data.adj_close) / price_data.adj_close[:-1]

# Marker size in units of points^2
volume = (15 * price_data.volume[:-2] / price_data.volume[0])**2
close = 0.003 * price_data.close[:-2] / 0.003 * price_data.open[:-2]
    
# Define graphs
fig.addgraph('graph1', x_label='$\Delta_i$', y_label='$\Delta_{i+1}$', title='Volume and percent change', show_grid=True)

# Insert object in plots
fig.addplot(lt.ltPlotPts(delta1[:-1], delta1[1:], surface=volume, color=close, marker='o', alpha=0.5, cmap=None), 'graph1')

# Save figure
fig.save(format='pdf')
