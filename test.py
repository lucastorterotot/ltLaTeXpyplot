#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc

from ltLaTeXpyplot import *

figure = ltFigure(name='new')

x = np.arange(-20,20,0.1)
y = np.sin(x)
y2 = np.cos(x)

f1 = ltPlotFct(x, y, label='$y=\\sin(x)$', color='C3')
f2 = ltPlotFct(x, y2, label='$y=\\cos(x)$')

figure.addgraph('graph1')
for plot in [f1, f2]:
    figure.addplot(plot, 'graph1')

figure.save(format='pdf')
