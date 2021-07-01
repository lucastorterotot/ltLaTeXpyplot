#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.utils import normalize_3d, add_colorbar

import numpy as np
import matplotlib as mpl

class ltPlotSurf:
    def __init__(self,
                 theta, phi,
                 x_fct = None, y_fct = None, z_fct = None,
                 R_fct = None, C_fct = None,
                 label = None,
                 alpha = 0.5, color = defaults.color, cmap = defaults.cmap, use_cmap = False,
                 cmap_low = None, cmap_high = None,
                 norm_xy = True, norm_xyz = False,
                 linewidth = defaults.linewidths['surface'], only_lines = None):
        if R_fct is not None:
            def x_fct(t, p):
                return R_fct(t, p) * np.sin(t) * np.cos(p)
            def y_fct(t, p):
                return R_fct(t, p) * np.sin(t) * np.sin(p)
            def z_fct(t, p):
                return R_fct(t, p) * np.cos(t)
        elif z_fct is not None and x_fct is None and y_fct is None :
            def x_fct(t, p):
                return t
            def y_fct(t, p):
                return p
        self.theta = theta
        self.phi = phi
        self.x_fct = x_fct
        self.y_fct = y_fct
        self.z_fct = z_fct
        self.R_fct = R_fct
        self.label = label
        self.alpha = alpha
        self.color = color
        self.cmap = cmap
        self.use_cmap = use_cmap
        self.norm_xy = norm_xy or norm_xyz
        self.norm_xyz = norm_xyz
        self.linewidth = linewidth
        self.C_fct = C_fct
        self.cmap_low = cmap_low
        self.cmap_high = cmap_high
        if only_lines is None:
            self.only_lines = (self.linewidth != 0)
        else:
            self.only_lines = only_lines
            

    def plot(self, fig, graph):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        elif self.use_cmap:
            fig.color_theme_candidate = False
        if fig.graphs[graph].projection == '3d':
            self._plot3d(fig, graph)
        else :
            self._plot2d(fig, graph)

    def _plot2d(self, fig, graph):
        _Surf2d = ltPlotScalField(self.theta,
                                  self.phi,
                                  z_fct = self.z_fct,
                                  cmap = self.cmap,
                                  color = self.color,
                                  label = self.label,
                                  norm_xy = self.norm_xy,
                                  norm_xyz = self.norm_xyz,
                                  alpha = self.alpha,
                                  use_cmap = self.use_cmap,
                                  linewidth = self.linewidth
                                 )
        _Surf2d.plot(fig, graph)

    def _plot3d(self, fig, graph):
        fig.graphs[graph].test_graph_3d()
        x, y, z = self.x_fct, self.y_fct, self.z_fct
        theta, phi = np.meshgrid(self.theta, self.phi)
        if callable(x) :
            x = x(theta, phi)
        if callable(y) :
            y = y(theta, phi)
        if callable(z) :
            z = z(theta, phi)
        ax = fig.graphs[graph].graph
        normalize_3d(self, fig.graphs[graph], x, y, z)
        method = ax.plot_surface
        if self.use_cmap:
            C_fct_eff = self.C_fct if self.C_fct is not None else z
            if callable(self.C_fct):
                C_fct_eff = self.C_fct(theta, phi)
            cmap_low, cmap_high = self.cmap_low, self.cmap_high
            if cmap_low is None:
                cmap_low = C_fct_eff.min().min()
            if cmap_high is None:
                cmap_high = C_fct_eff.max().max()
            norm = mpl.colors.Normalize(vmin = cmap_low, vmax = cmap_high)
            facecolors = getattr(mpl.cm, self.cmap)(norm(C_fct_eff))
            surf = method(x, y, z,
                          rstride = 1,
                          cstride = 1,
                          linewidth = self.linewidth,
                          alpha = self.alpha,
                          cmap = self.cmap,
                          facecolors = facecolors
                         )
        else:
            surf = method(x, y, z,
                          rstride = 1,
                          cstride = 1,
                          linewidth = self.linewidth,
                          alpha = self.alpha,
                          color = self.color,
                          edgecolors = self.color
                         )
        if self.only_lines:
            surf.set_facecolor((1,1,1,0))
        if fig.graphs[graph].show_cmap_legend and self.use_cmap:
            m = mpl.cm.ScalarMappable(cmap = getattr(mpl.cm, self.cmap), norm = norm)
            m.set_array([])
            add_colorbar(m, fig.graphs[graph])
