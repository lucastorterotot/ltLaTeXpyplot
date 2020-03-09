#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import ltLaTeXpyplot as lt
import ltLaTeXpyplot.data.orbitals.orbitals_data as data # uses the orbital data of this package

r_on_a0 = np.arange(0,data.r_on_a0_MAX,0.1)

radius = r_on_a0*data.a0

Rnl = data.Rnl

for n,l in [(3,0),(2,1)]:
    figs = {
        'R' : lt.ltFigure(name='fig-R{}{}'.format(n,l), width_frac=.25),
        'R2' : lt.ltFigure(name='fig-R{}{}_squared'.format(n,l), width_frac=.25),
        'p' : lt.ltFigure(name='fig-R{}{}_proba'.format(n,l), width_frac=.25),
        }
    x = r_on_a0
    ys = {
        'R' : Rnl(radius,n,l),
        'R2' : Rnl(radius,n,l)**2,
        'p' : 4 * np.pi * (radius)**2 * Rnl(radius,n,l)**2,
        }
    for subkey, fig in figs.items():
        fig.addgraph('graph1', x_min=0, x_max=data.r_on_a0_max['{}x'.format(n)], y_ticks=False, show_x_axis=True)
        if subkey != 'R' or n == l+1:
            fig.graphs['graph1'].y_min = 0
            fig.graphs['graph1'].y_max = 1
        fig.addplot(lt.ltPlotFct(x, ys[subkey]/max(ys[subkey])), 'graph1')
        fig.save(format='pdf')
