#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.PlotFct import ltPlotFct

class ltPlotPts(ltPlotFct):
    def __init__(self,
                 x, y,
                 xerr = None,
                 yerr = None,
                 label = None,
                 color = defaults.color,
                 cmap = defaults.cmap,
                 marker = defaults.marker_pts,
                 markersize = defaults.marker_size,
                 linewidth = defaults.linewidths['plotpts'],
                 elinewidth = defaults.linewidths['plotpts_e'],
                 capsize = defaults.linewidths['capsize'],
                 capthick = defaults.linewidths['capthick'],
                 surface = None,
                 alpha = None
                ):
        ltPlotFct.__init__(self,
                           x, y,
                           label = label,
                           color = color,
                           marker = marker,
                           markersize = markersize,
                           linewidth = linewidth
                          )
        self.xerr = xerr
        self.yerr = yerr
        self.elinewidth = elinewidth
        self.capthick = capthick
        self.capsize = capsize
        self.surface = surface
        self.alpha = alpha
        self.cmap = cmap

    def plot(self, fig, graph):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        if self.surface is None:
            fig.graphs[graph].graph.errorbar(self.x,
                                             self.y,
                                             xerr = self.xerr,
                                             yerr = self.yerr,
                                             marker = self.marker,
                                             markersize = self.markersize,
                                             fmt = ' ',
                                             linewidth = self.linewidth,
                                             elinewidth = self.elinewidth,
                                             capsize = self.capsize,
                                             capthick = self.capthick,
                                             color = self.color,
                                             label = self.label
                                            )
        else :
            fig.graphs[graph].graph.scatter(self.x,
                                            self.y,
                                            s = self.surface,
                                            c = self.color,
                                            marker = self.marker,
                                            cmap = self.cmap,
                                            alpha = self.alpha
                                           )

    def plot_density(self, fig, graph, bins = [100, 100]):
        # Calculate the point density
        from matplotlib.colors import Normalize
        from scipy.interpolate import interpn

        data , x_e, y_e = np.histogram2d(self.x, self.y, bins, density = True)
        z = interpn(
            ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ),
            data,
            np.vstack([self.x, self.y]).T,
            method = "splinef2d",
            bounds_error = False
        )
        z[np.where(np.isnan(z))] = 0.0
        idx = z.argsort()
        x, y, z = self.x[idx], self.y[idx], z[idx]
        fig.graphs[graph].graph.scatter(x, y,
                                        c = z,
                                        marker = self.marker,
                                        edgecolor = '',
                                        label = self.label,
                                        cmap = self.cmap,
                                        alpha = self.alpha
                                       )
