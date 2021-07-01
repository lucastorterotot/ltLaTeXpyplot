#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.utils import add_colorbar

import numpy as np
from scipy.integrate import odeint
import matplotlib as mpl

class ltPlotVectField2d:
    def __init__(self,
                 x, y,
                 vx_fct, vy_fct,
                 label = None,
                 color = defaults.color, cmap = defaults.cmap, use_cmap = False, C_fct = None,
                 cmap_low = None, cmap_high = None,
                 norm_xy = True,
                 label_fieldline = None, color_fieldline = defaults.color, dashes_fieldline = defaults.dashes,
                 linewidth = defaults.linewidths['vectfield'], linewidth_fieldline = defaults.linewidths['vectfieldline']):
        self.label = label
        self.x = x
        self.y = y
        self.vx_fct = vx_fct
        self.vy_fct = vy_fct
        self.color = color
        self.norm_xy = norm_xy
        self.linewidth = linewidth

        self.label_fieldline = label_fieldline
        self.color_fieldline = color_fieldline
        self.dashes_fieldline = dashes_fieldline
        self.linewidth_fieldline = linewidth_fieldline

        self.cmap = cmap
        self.use_cmap = use_cmap
        self.C_fct = C_fct
        self.cmap_low = cmap_low
        self.cmap_high = cmap_high

    def plot(self, fig, graph):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        elif self.use_cmap:
            fig.color_theme_candidate = False
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable = 'box')
        vx, vy = self.vx_fct, self.vy_fct
        xs, ys = self.x, self.y
        if callable(self.vx_fct) and callable(self.vy_fct):
            xs, ys = np.meshgrid(xs, ys)
            vx = self.vx_fct(xs, ys)
            vy = self.vy_fct(xs, ys)
        color = self.color
        if self.use_cmap:
            C_fct_eff = self.C_fct
            if callable(self.C_fct):
                C_fct_eff = self.C_fct(xs, ys).flatten()
            if self.C_fct is None:
                C_fct_eff = ((vx**2+vy**2)**.5).flatten()
            cmap_low, cmap_high = self.cmap_low, self.cmap_high
            if cmap_low is None:
                cmap_low = C_fct_eff.min()
            if cmap_high is None:
                cmap_high = C_fct_eff.max()
            norm = mpl.colors.Normalize(vmin = cmap_low, vmax = cmap_high)
            norm.autoscale(C_fct_eff)
            color = getattr(mpl.cm, self.cmap)(norm(C_fct_eff))
        fig.graphs[graph].graph.quiver(xs, ys, vx, vy, linewidth = self.linewidth, label = self.label, color = color)
        if fig.graphs[graph].show_cmap_legend:
            m = mpl.cm.ScalarMappable(cmap = getattr(mpl.cm, self.cmap), norm = norm)
            m.set_array([])
            add_colorbar(m, fig.graphs[graph])

    def plot_fieldline(self, fig, graph, point, startT, endT, stepT, color = None, label = None, dashes = None):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        if color is None:
            color = self.color_fieldline
        if label is None:
            label = self.label_fieldline
        if dashes is None:
            dashes = self.dashes_fieldline
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable = 'box')
        T = np.linspace(startT, endT, stepT)
        def _field(p, t):
            x, y = p
            return self.vx_fct(x, y), self.vy_fct(x, y)
        line_xy = odeint(_field, point, T).transpose()
        fig.graphs[graph].graph.plot(line_xy[0],
                                     line_xy[1],
                                     label = label,
                                     color = color,
                                     dashes = dashes,
                                     linewidth = self.linewidth_fieldline
                                    )

    def plot_streamplot(self, fig, graph, start_points = None, density = 'undef', color = None, linewidth = None, **kwargs):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        if color is None:
            color = self.color_fieldline
        if linewidth is None:
            linewidth = self.linewidth_fieldline
        if density == 'undef':
            density = 1
            if start_points is not None:
                density = len(start_points)
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable = 'box')
        vx, vy = self.vx_fct, self.vy_fct
        xs, ys = self.x, self.y
        if callable(self.vx_fct) and callable(self.vy_fct):
            xs, ys = np.meshgrid(xs, ys)
            vx = self.vx_fct(xs, ys)
            vy = self.vy_fct(xs, ys)
        if callable(color):
            color = color(xs, ys)
        if callable(linewidth):
            linewidth = linewidth(xs, ys)
        strm = fig.graphs[graph].graph.streamplot(xs, ys,
                                                  vx, vy,
                                                  start_points = start_points,
                                                  density = density,
                                                  color = color,
                                                  linewidth = linewidth,
                                                  **kwargs
                                                 )
        if fig.graphs[graph].show_cmap_legend:
            add_colorbar(strm.lines, fig.graphs[graph])
