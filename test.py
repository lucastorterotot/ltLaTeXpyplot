#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

import ltLaTeXpyplot.core as lt

figure = lt.ltFigure(name='test_fig')

x = np.arange(-20,20,0.1)
y = np.sin(x)
y2 = np.cos(x)

f1 = lt.ltPlotFct(x, y, label='$y=\\sin(x)$', color='C3')
f2 = lt.ltPlotFct(x, y2, label='$y=\\cos(x)$')

figure.addgraph('graph1', x_label='$\\varepsilon$', y_label='$f(\\varepsilon)$')
for plot in [f1, f2]:
    figure.addplot(plot, 'graph1')

figure.save(format='pdf')
