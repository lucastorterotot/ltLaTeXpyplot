#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.utils import ltPlotPieautopct

import matplotlib.pyplot as plt

class ltPlotPie:
    def __init__(self,
                 sizes,
                 explode = None,
                 labels = None,
                 colors = None,
                 autopct = None,
                 pctdistance = .6,
                 shadow = True,
                 labeldistance = 1.1,
                 startangle = 90,
                 counterclock = True,
                 wedgeprops = None,
                 textprops = None,
                 frame = False,
                 rotatelabels = False,
                 norm_xy = True
                ):
        self.sizes = sizes
        self.explode = explode
        self.labels = labels
        self.colors = colors
        if autopct is not None:
            self.autopct = autopct
        else:
            self.autopct = ltPlotPieautopct
        self.pctdistance = pctdistance
        self.shadow = shadow
        self.labeldistance = labeldistance
        self.startangle = startangle
        self.counterclock = counterclock
        self.wedgeprops = wedgeprops
        self.textprops = textprops
        self.frame = frame
        self.rotatelabels = rotatelabels
        self.norm_xy = norm_xy

    def plot(self, fig, graph):
        fig.color_theme_candidate = False
        ax = fig.graphs[graph].graph
        plt.setp(ax.get_xticklabels(), visible = False)
        plt.setp(ax.get_yticklabels(), visible = False)
        for ticks_category in ['major', 'minor']:
            ax.tick_params(direction = 'in',
                           which = ticks_category,
                           bottom = 0, top = 0, left = 0, right = 0,
                           width = defaults.linewidths[ticks_category+'ticks']
                          )
        if self.norm_xy:
            ax.axis('equal')
        ax.pie(self.sizes,
               explode = self.explode,
               labels = self.labels,
               colors = self.colors,
               autopct = self.autopct,
               pctdistance = self.pctdistance,
               shadow = self.shadow,
               labeldistance = self.labeldistance,
               startangle = self.startangle,
               counterclock = self.counterclock,
               wedgeprops = self.wedgeprops,
               textprops = self.textprops,
               frame = self.frame,
               rotatelabels = self.rotatelabels
              )
