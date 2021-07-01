#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.PlotSurf import ltPlotSurf
from ltLaTeXpyplot.module.utils import add_colorbar

from matplotlib.ticker import MaxNLocator
import numpy as np

class ltPlotScalField:
    def __init__(self,
                 x, y, z_fct,
                 C_fct = None,
                 cmap = defaults.cmap,
                 levels = None,
                 Nlevels = None,
                 color = defaults.color,
                 label = None,
                 clabel = False,
                 norm_xy = True,
                 norm_xyz = False,
                 alpha = 1,
                 alpha_3d = 0.5,
                 use_cmap = True,
                 linewidth = defaults.linewidths['scalfield'],
                 linewidths = defaults.linewidths['contour2d'],
                 only_lines = None
                ):
        self.label = label
        self.x = x
        self.y = y
        self.z_fct = z_fct
        self.cmap = cmap
        self.clabel = clabel
        self.levels = levels
        self.Nlevels = Nlevels
        self.color = color
        self.alpha = alpha
        self.alpha_3d = alpha_3d
        self.norm_xy = norm_xy or norm_xyz
        self.norm_xyz = norm_xyz
        self.use_cmap = use_cmap
        self.linewidth = linewidth
        self.linewidths = linewidths
        self.C_fct = C_fct
        if only_lines is None:
            self.only_lines = (self.linewidth != 0)
        else:
            self.only_lines = only_lines

    def plot(self, fig, graph):
        if fig.graphs[graph].projection == '3d':
            self._plot3d(fig, graph)
        else :
            self._plot2d(fig, graph)

    def plot_field(self, fig, graph):
        self.plot(fig, graph)

    def _plot_contour_init(self, fig, graph):
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable = 'box')
        z_fct = self.z_fct
        xs, ys = self.x, self.y
        if callable(self.z_fct):
            xs, ys = np.meshgrid(xs, ys)
            z_fct = self.z_fct(xs, ys)
        if self.levels is None and self.Nlevels is not None:
            self.levels = MaxNLocator(nbins = self.Nlevels).tick_values(z_fct.min(), z_fct.max())
        return xs, ys, z_fct

    def plot_contour(self, fig, graph):
        fig.color_theme_candidate = False
        xs, ys, z_fct = self._plot_contour_init(fig, graph)
        if self.levels is not None :
            current_contour = fig.graphs[graph].graph.contour(
                xs, ys, z_fct,
                origin = 'lower',
                linewidths = self.linewidths,
                cmap = self.cmap,
                levels = self.levels
            )
        else:
            current_contour = fig.graphs[graph].graph.contour(
                xs, ys, z_fct,
                origin = 'lower',
                linewidths = self.linewidths,
                cmap = self.cmap
            )
        if fig.graphs[graph].show_cmap_legend:
            add_colorbar(current_contour, fig.graphs[graph])
        if self.clabel :
            fig.graphs[graph].graph.clabel(
                current_contour,
                inline = 1,
                fmt = r'${value}$'.format(value = '%1.1f'),
                fontsize = pgf_with_latex['legend.fontsize']-1
            )
        current_contour = 0 

    def plot_contourf(self, fig, graph):
        fig.color_theme_candidate = False
        xs, ys, z_fct = self._plot_contour_init(fig, graph)
        if self.levels is not None:
            imshow = fig.graphs[graph].graph.contourf(
                xs, ys, z_fct, cmap = self.cmap, levels = self.levels
            )
        else:
            imshow = fig.graphs[graph].graph.contourf(
                xs, ys, z_fct, cmap = self.cmap
            )
        if fig.graphs[graph].show_cmap_legend:
            add_colorbar(imshow, fig.graphs[graph]) 
            
    def _plot2d(self, fig, graph):
        fig.color_theme_candidate = False
        aspect = 'auto'
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable = 'box')
            aspect = 'equal'
        z_fct = self.z_fct
        xs, ys = self.x, self.y
        if callable(self.z_fct):
            xs, ys = np.meshgrid(xs, ys)
            z_fct = self.z_fct(xs, ys)
        imshow = fig.graphs[graph].graph.imshow(z_fct,
                                                cmap = self.cmap,
                                                extent = (
                                                    min(self.x), max(self.x), min(self.y), max(self.y)
                                                ),
                                                origin = 'lower',
                                                alpha = self.alpha,
                                                aspect = aspect
                                               )
        if fig.graphs[graph].show_cmap_legend:
            add_colorbar(imshow, fig.graphs[graph])

    def _plot3d(self, fig, graph):
        fig.color_theme_candidate = False
        if self.alpha == 1 :
            self.alpha = self.alpha_3d
        _ScalField3d = ltPlotSurf(
            self.x, self.y, z_fct = self.z_fct,
            C_fct = self.C_fct,
            label = self.label,
            alpha = self.alpha,
            color = self.color,
            cmap = self.cmap,
            norm_xy = self.norm_xy,
            norm_xyz = self.norm_xyz,
            use_cmap = self.use_cmap,
            linewidth = self.linewidth,
            only_lines = self.only_lines
        )
        _ScalField3d.plot(fig, graph)
