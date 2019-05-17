#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

import ltLaTeXpyplot.core as lt
import ltLaTeXpyplot.data.orbitals.orbitals_data as data # uses the orbital data of this package

r_on_a0 = np.arange(0,data.r_on_a0_MAX,0.1)

radius = r_on_a0*data.a0

for key in data.R_fcts.keys():
    figs = {
        'R' : lt.ltFigure(name='fig-R'+key, width_frac=.25),
        'R2' : lt.ltFigure(name='fig-R'+key+'_squared', width_frac=.25),
        'p' : lt.ltFigure(name='fig-R'+key+'_proba', width_frac=.25),
        }
    R_fct = data.R_fcts[key]
    x = r_on_a0
    ys = {
        'R' : R_fct(radius),
        'R2' : R_fct(radius)**2,
        'p' : 4 * np.pi * (radius)**2 * R_fct(radius)**2,
        }
    for subkey in figs.keys():
        figs[subkey].addgraph('graph1', x_min=0, x_max=data.r_on_a0_max[key[0]+'x'], y_ticks=False, show_x_axis=True)
        if subkey is not 'R' or key in ['10', '21', '32']:
            figs[subkey].graphs['graph1'].y_min = 0
            figs[subkey].graphs['graph1'].y_max = 1
        figs[subkey].addplot(lt.ltPlotFct(x, ys[subkey]/max(ys[subkey])), 'graph1')
        figs[subkey].save(format='pdf')
