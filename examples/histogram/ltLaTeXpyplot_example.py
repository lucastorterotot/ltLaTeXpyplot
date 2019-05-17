#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot.core as lt

# Create figure
fig = lt.ltFigure(name='fig', height_width_ratio = .7)

# Define what to plot
np.random.seed(19680801)

# example data
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution
x = mu + sigma * np.random.randn(437)

num_bins = 50
    
# Define graphs
fig.addgraph('graph1', x_label='Smarts', y_label='Probability density', title='Histogram of IQ: $\mu=100$, $\sigma=15$', y_scaling='log', y_min=.75e-4, y_max=0.05, comma_y_major = False)

# Insert object in plots
hist = lt.ltPlotHist(x, bins=num_bins, range=[50,150], fill=True)
hist.set_integral(1) # get a probability
hist.plot(fig, 'graph1')

# Add fit line
bins = hist.bins
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))

fct = lt.ltPlotFct(bins, y, color='C1', dashes=[4,1.5])

fig.addplot(fct, 'graph1')

# Save figure
fig.save(format='pdf')
