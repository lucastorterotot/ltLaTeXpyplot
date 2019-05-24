#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Example taken from
# https://www.physique-experimentale.com/python/ajustement_de_courbe.py

import numpy as np
import scipy as sc

import ltLaTeXpyplot.core as lt

# Create figure
fig = lt.ltFigure(name='reglin-fig')

# Define what to plot
# data
x = np.array([1.0,2.1,3.1,3.9])
y = np.array([2.1,3.9,6.1,7.8])
# uncertainties (1 sigma)
ux = np.array([0.2,0.3,0.2,0.2])
uy = np.array([0.3,0.3,0.2,0.3])

reg = lt.ltPlotRegLin(x, y, ux, uy, info_placement='lower right', label='Data', label_reg='Regression')

# Définir le graphique
fig.addgraph('graph1', x_label='$\\varepsilon$', y_label='$f(\\varepsilon)$', show_legend=True)

# Insérer les objets à tracer dans le plot
reg.plot(fig, 'graph1', lang='EN')

# Sauvegarder la figure
fig.save()

fig.save(format='pdf')
