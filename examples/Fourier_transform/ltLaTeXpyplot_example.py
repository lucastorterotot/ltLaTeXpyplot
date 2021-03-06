#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import ltLaTeXpyplot as lt

# Create figure
fig = lt.ltFigure(name='fig')

# Define what to plot
tau = 10.
f0 = 1.
omega0 = 2*np.pi*f0
t = np.arange(0.,50.,0.01)
x = np.sin(omega0*t)*np.exp(-t/tau)

fct = lt.ltPlotFct(t, x, Fs = 1/t[1])

# Define graphs
fig.addgraph('graph1', x_label='$\\nu$ (Hz)', y_label='TF', show_legend=True, legend_on_side=False, x_min=0, x_max=2)

# Insert object in plots
fct.plot_TF(fig, 'graph1', label='Fourier tr.')

# Save figure
fig.save(format='pdf')
