#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot.core as lt

# Create figure
fig = lt.ltFigure(name='fig')

# Define what to plot
k = np.arange(1e5)
x = np.sin(2*np.pi*k*k/k.max()*k/k.max()/10)+.5*np.sin(2*np.pi*k/5)

fct = lt.ltPlotFct(k, x, Nfft = 1024)

# Define graphs
fig.addgraph('graph3', x_label='time', y_label='$f$ (Hz)')

# Insérer les objets à tracer dans le plot
fct.plot_TFrp(fig, 'graph3')

# Sauvegarder la figure
fig.save(format='pdf')
