#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.PlotFct import ltPlotFct
from ltLaTeXpyplot.module.utils import normalize_3d

class ltPlotFct3d(ltPlotFct):
    def __init__(self,
                 x, y, z,
                 label = None,
                 color = defaults.color,
                 dashes = defaults.dashes,
                 marker = None,
                 markersize = defaults.marker_size,
                 linewidth = defaults.linewidths['plotfct'],
                 norm_xy = True,
                 norm_xyz = False
                ):
        ltPlotFct.__init__(self,
                           x, y,
                           label = label,
                           color = color,
                           dashes = dashes,
                           marker = marker,
                           markersize = markersize,
                           linewidth = linewidth
                          )
        if callable(z):
            self.z = z(x,y)
        else:
            self.z = z
        self.norm_xy = norm_xy or norm_xyz
        self.norm_xyz = norm_xyz

    def plot(self, fig, graph):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        fig.graphs[graph].test_graph_3d()
        x = self.x
        y = self.y
        z = self.z
        ax = fig.graphs[graph].graph
        normalize_3d(self, fig.graphs[graph], x, y, z)
        ax.plot(x, y, z,
                color = self.color,
                linewidth = self.linewidth,
                label = self.label,
                marker = self.marker,
                markersize = self.markersize,
                dashes = self.dashes
               )
