#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.PlotPts import ltPlotPts
from ltLaTeXpyplot.module.utils import normalize_3d

class ltPlotPts3d(ltPlotPts):
    def __init__(self,
                 x, y, z,
                 label = None,
                 color = defaults.color,
                 marker = defaults.marker_pts,
                 markersize = defaults.marker_size,
                 cmap = None,
                 norm_xy = True,
                 norm_xyz = False,
                 surface = None,
                 alpha = None
                ):
        ltPlotPts.__init__(self,
                           x, y,
                           label = label,
                           color = color,
                           cmap = cmap,
                           marker = marker,
                           markersize = markersize,
                           surface = surface,
                           alpha = alpha
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
        markersize = self.markersize
        if self.surface is not None:
            markersize = self.surface
        ax.scatter(x, y, z,
                   c = self.color,
                   marker = self.marker,
                   s = markersize,
                   label = self.label,
                   cmap = self.cmap,
                   alpha = self.alpha
                  )
