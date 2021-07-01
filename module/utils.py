#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ltLaTeXpyplot.module.default_tex_settings import pgf_with_latex, inches_per_cm, figsize

import numpy as np
import matplotlib.ticker as tkr

import matplotlib.pyplot as plt

def num_format(value, pos):
    # formatter function takes tick label and tick position
    max_dec = 5
    min_exp = 6
    val_str = str(value)
    if 'e' in val_str:
        ind = val_str.index('e')
        signif = float(val_str[:ind])
        exponent = int(val_str[ind+1:])
    else:
        signif = value
        exponent = 0
    if signif > 10**(min_exp):
        signif *= 10**(-min_exp)
        exponent += min_exp
        while signif >= 10:
            signif *= .1
            exponent += 1
    signif = np.round(signif, max_dec)
    if int(signif) == signif:
        signif = int(signif)
    if exponent != 0:
        string = '{}e{}'.format(str(signif), str(exponent))
    else:
        string = str(signif)
    string = ''.join(['\\num{', string, '}'])
    return string

def ltPlotPieautopct(x, unit = '%', maxdec = 1):
    return ''.join(['\\SI{', str(round(x,maxdec)), '}{', unit, '}'])

num_formatter = tkr.FuncFormatter(num_format)  # make formatter

def add_colorbar(plot, ltGraph):
    if ltGraph.projection == '3d':
        shrink = .75
    else:
        shrink = 1.
    clb = plt.colorbar(plot, shrink = shrink, ax = ltGraph.graph)
    clb_FR_ticks = []
    for tick in clb.get_ticks():
        clb_FR_ticks.append(num_format(tick, 0))
    clb.set_ticks(clb.get_ticks())
    clb.set_ticklabels(clb_FR_ticks)
    clb.ax.tick_params(labelsize = pgf_with_latex['xtick.labelsize'])
    if ltGraph.cmap_label is not None:
        clb.ax.set_title(ltGraph.cmap_label, fontsize = pgf_with_latex['axes.labelsize'])

import six
def set_aspect(ax, aspect, adjustable = None, anchor = None):
    if (isinstance(aspect, six.string_types)
        and aspect in ('equal', 'auto')):
        ax._aspect = aspect
    else:
        ax._aspect = float(aspect)  # raise ValueError if necessary

    if adjustable is not None:
        ax.set_adjustable(adjustable)
    if anchor is not None:
        ax.set_anchor(anchor)
    ax.stale = True

def normalize_3d(plot, ltGraph, x, y, z):
    ax = ltGraph.graph
    if plot.norm_xy or plot.norm_xyz :
        max_range_xy = max([x.max() -x.min(), y.max() -y.min()])/2
        max_range_z = (z.max() -z.min())/2
        try:
            ax.set_aspect('equal')
        except NotImplementedError:
            set_aspect(ax, 'equal')
            ltGraph.fig.suppressNotImplementedError = True
        if plot.norm_xyz :
            max_range = max([max_range_xy, max_range_z])
            max_range_xy = max_range
            max_range_z = max_range
        Xb = max_range_xy*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(x.max()+x.min())
        Yb = max_range_xy*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(y.max()+y.min())
        Zb = max_range_z*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(z.max()+z.min())
        for xb, yb, zb in zip(Xb, Yb, Zb):
            ax.plot([xb], [yb], [zb], 'w')

def factorial (x):
    result = 1
    if x > 1:
        for k in range(1,x+1):
            result*= k
    return result
