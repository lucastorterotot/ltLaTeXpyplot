#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.PlotVectField2d import ltPlotVectField2d
from ltLaTeXpyplot.module.utils import normalize_3d

import numpy as np
from scipy.integrate import odeint

class ltPlotVectField3d(ltPlotVectField2d):
    def __init__(self,
                 x, y, z,
                 vx_fct, vy_fct, vz_fct,
                 label = None,
                 color = defaults.color,
                 cmap = defaults.cmap,
                 use_cmap = False,
                 C_fct = None,
                 cmap_low = None,
                 cmap_high = None,
                 norm_xy = True,
                 norm_xyz = False,
                 label_fieldline = None,
                 color_fieldline = defaults.color,
                 dashes_fieldline = defaults.dashes,
                 linewidth = defaults.linewidths['vectfield'],
                 linewidth_fieldline = defaults.linewidths['vectfieldline']
                ):
        ltPlotVectField2d.__init__(self,
                                   x, y,
                                   vx_fct, vy_fct,
                                   label = label,
                                   color = color,
                                   cmap = cmap,
                                   use_cmap = use_cmap,
                                   C_fct = C_fct,
                                   cmap_low = cmap_low,
                                   cmap_high = cmap_high,
                                   norm_xy = norm_xy,
                                   label_fieldline = label_fieldline,
                                   color_fieldline = color_fieldline,
                                   dashes_fieldline = dashes_fieldline,
                                   linewidth = linewidth,
                                   linewidth_fieldline = linewidth_fieldline
                                  )
        self.z = z
        self.vz_fct = vz_fct
        self.norm_xy = norm_xy or norm_xyz
        self.norm_xyz = norm_xyz

    def plot(self, fig, graph):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        elif self.use_cmap:
            fig.color_theme_candidate = False
        fig.graphs[graph].test_graph_3d()
        xs, ys, zs = np.meshgrid(self.x, self.y, self.z)
        normalize_3d(self, fig.graphs[graph], xs, ys, zs)
        vx, vy, vz = self.vx_fct, self.vy_fct, self.vz_fct
        if callable(self.vx_fct) and callable(self.vy_fct) and callable(self.vz_fct):
            vx = self.vx_fct(xs, ys, zs)
            vy = self.vy_fct(xs, ys, zs)
            vz = self.vz_fct(xs, ys, zs)
        color = self.color
        if self.use_cmap:
            C_fct_eff = self.C_fct
            if callable(self.C_fct):
                C_fct_eff = self.C_fct(xs, ys, zs).flatten()
            if self.C_fct is None:
                C_fct_eff = ((vx**2+vy**2+vz**2)**.5).flatten()
            cmap_low, cmap_high = self.cmap_low, self.cmap_high
            if cmap_low is None:
                cmap_low = C_fct_eff.min()
            if cmap_high is None:
                cmap_high = C_fct_eff.max()
            norm = mpl.colors.Normalize(vmin = cmap_low, vmax = cmap_high)
            norm.autoscale(C_fct_eff)
            color = getattr(mpl.cm, self.cmap)(norm(C_fct_eff))
        fig.graphs[graph].graph.quiver(xs, ys, zs,
                                       vx, vy, vz,
                                       length = 0.1,
                                       normalize = True,
                                       linewidth = self.linewidth,
                                       label = self.label,
                                       color = color
                                      )
        if fig.graphs[graph].show_cmap_legend:
            m = mpl.cm.ScalarMappable(cmap = getattr(mpl.cm, self.cmap), norm = norm)
            m.set_array([])
            add_colorbar(m, fig.graphs[graph])

    def plot_fieldline(self, fig, graph, point, startT, endT, stepT, color = None, label = None, dashes = None):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        fig.graphs[graph].test_graph_3d()
        if color is None:
            color = self.color_fieldline
        if label is None:
            label = self.label_fieldline
        if dashes is None:
            dashes = self.dashes_fieldline
        T = np.linspace(startT, endT, stepT)
        def _field(p, t):
            x, y, z = p
            return self.vx_fct(x, y, z), self.vy_fct(x, y, z), self.vz_fct(x, y, z)
        line_xyz = odeint(_field, point, T).transpose()
        normalize_3d(self, fig.graphs[graph], line_xyz[0], line_xyz[1], line_xyz[2])
        fig.graphs[graph].graph.plot(line_xyz[0],
                                     line_xyz[1],
                                     line_xyz[2],
                                     label = label,
                                     color = color,
                                     dashes = dashes,
                                     linewidth = self.linewidth_fieldline
                                    )
