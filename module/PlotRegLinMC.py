#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.PlotPts import ltPlotPts
from ltLaTeXpyplot.module.PlotFct import ltPlotFct

import numpy as np
from ltLaTeXpyplot.module.utils import creation_liste_droites

class ltPlotRegLinMC(ltPlotPts):
    def __init__(self,
                 x, y, xerr, yerr,
                 N = 1000,
                 distrib = "uniform",
                 distrib_x = None,
                 distrib_y = None,
                 label = None,
                 label_reg = None,
                 color = defaults.color,
                 color_reg = 'C3',
                 marker = defaults.marker_pts,
                 markersize = defaults.marker_size,
                 linewidth = defaults.linewidths['plotfct'],
                 elinewidth = defaults.linewidths['plotpts_e'],
                 capsize = defaults.linewidths['capsize'],
                 capthick = defaults.linewidths['capthick'],
                 dashes = defaults.dashes,
                 nb_ch_u = 2,
                 give_info = True,
                 info_placement = 'upper left',
                 verbose = False
                ):
        ltPlotPts.__init__(self,
                           x, y, xerr, yerr,
                           label = label,
                           color = color,
                           marker = marker,
                           markersize = markersize,
                           linewidth = linewidth,
                           elinewidth = elinewidth,
                           capsize = capsize,
                           capthick = capthick
                          )
        self.N = N
        self.label_reg = label_reg
        self.color_reg = color_reg
        self.dashes = dashes
        self.give_info = give_info
        self.info_placement = info_placement
        self.verbose = verbose

        if distrib_x is None:
            distrib_x = distrib
        if distrib_y is None:
            distrib_y = distrib
        self.distrib_x = distrib_x
        self.distrib_y = distrib_y

        xerr_for_reg = xerr
        if type(xerr) == list:
            xerr_for_reg = np.array(xerr)
        elif type(xerr) in [int, float]:
            xerr_for_reg = np.ones(len(x)) * xerr

        yerr_for_reg = yerr
        if type(yerr) == list:
            yerr_for_reg = np.array(yerr)
        elif type(yerr) in [int, float]:
            yerr_for_reg = np.ones(len(y)) * yerr

        try:
            if len(xerr_for_reg) == 2:
                    if len(xerr_for_reg[0]) == len(x) and len(xerr_for_reg[1]) == len(x):
                        xerr_for_reg = (
                            np.array(xerr_for_reg[0])
                            + np.array(xerr_for_reg[1])
                        )/2
        except:
            pass
        try:
            if len(yerr_for_reg) == 2:
                    if len(yerr_for_reg[0]) == len(y) and len(yerr_for_reg[1]) == len(y):
                        yerr_for_reg = (
                            np.array(yerr_for_reg[0])
                            + np.array(yerr_for_reg[1])
                        )/2
        except:
            pass
            
        lst_a, lst_b = creation_liste_droites(x, y, xerr_for_reg, yerr_for_reg, N, distrib_x, distrib_y)
        a = np.mean(lst_a)
        u_a = np.std(lst_a)#/N**.5
        b = np.mean(lst_b)
        u_b = np.std(lst_b)#/N**.5

        round_param_a = int(nb_ch_u - np.log10(u_a))
        round_param_b = int(nb_ch_u - np.log10(u_b))
        self.nb_ch_u = nb_ch_u
        
        # optimized parameters a and b
        exact_popt = (a, b)
        popt = (np.round(a, round_param_a), np.round(b, round_param_b))
        # uncetainties on parameters (1 sigma)
        exact_uopt = (u_a, u_b)
        uopt = (np.round(u_a, round_param_a), np.round(u_b, round_param_b))

        if self.verbose:
            print('  Linear regression :')
            print('    f(x) = a * x + b')
            print('    a = {} +/- {} ;'.format(popt[0], uopt[0]))
            print('    b = {} +/- {} ;'.format(popt[1], uopt[1]))
            print(' ')

        x_aj = np.linspace(min(x),max(x),100)
        y_aj = popt[0]*np.linspace(min(x),max(x),100)+popt[1]

        self.popt = popt
        self.exact_popt = popt
        self.uopt = uopt
        self.exact_uopt = uopt
        self.x_aj = x_aj
        self.y_aj = y_aj

        self.points = ltPlotPts(
            x, y, xerr, yerr,
            label = label,
            color = color,
            marker = marker,
            markersize = markersize,
            linewidth = self.linewidth,
            elinewidth = self.elinewidth,
            capsize = self.capsize,
            capthick = self.capthick
        )
        self.reglin = ltPlotFct(
            x_aj, y_aj,
            label = label_reg,
            color = color_reg,
            dashes = dashes,
            linewidth = self.linewidth
        )
        
    def plot(self, fig, graph, lang = None):
        fig.color_theme_candidate = False
        if lang is None:
            lang = fig.lang
        self.plot_reg(fig, graph, lang = lang)
        self.plot_pts(fig, graph)

    def plot_reg(self, fig, graph, lang = None):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        if lang is None:
            lang = fig.lang
        self.reglin.plot(fig, graph)
        if self.give_info:
            x_info = 0.5
            y_info = 0.5
            multialignment = 'center'
            verticalalignment = 'center'
            horizontalalignment = 'center'
            if 'left' in self.info_placement :
                x_info = 0.025
                multialignment = 'left'
                horizontalalignment = 'left'
            if 'right' in self.info_placement :
                x_info = 0.975
                multialignment = 'right'
                horizontalalignment = 'right'
            if 'upper' in self.info_placement :
                y_info = 0.95
                verticalalignment = 'top'
            if 'lower' in self.info_placement :
                y_info = 0.05
                verticalalignment = 'bottom'
            else :
                pass
            ax = fig.graphs[graph].graph

            reglintxt = "Linear regression (MC):"
            if lang == 'FR':
                reglintxt = "R\\'egression lin\\'eaire (MC) :"
            ax.text(x_info, y_info,
                    '\n'.join([
                        '{} $f(x) = ax+b$'.format(reglintxt),
                        '$a = \\num{{ {0}e{1} }} \\pm \\num{{ {2:.1e} }}$'.format(
                            np.round(self.popt[0]*10**(-int(np.log10(abs(self.popt[0])))), 10),
                            int(np.log10(abs(self.popt[0]))),
                            self.uopt[0],
                        ),
                        '$b = \\num{{ {0}e{1} }} \\pm \\num{{ {2:.1e} }}$'.format(
                            np.round(self.popt[1]*10**(-int(np.log10(abs(self.popt[1])))+1), 10),
                            int(np.log10(abs(self.popt[1]))-1),
                            self.uopt[1],
                        ),
                        ]),
                    transform = ax.transAxes,
                    multialignment = multialignment,
                    verticalalignment = verticalalignment,
                    horizontalalignment = horizontalalignment
                   )

    def plot_pts(self, fig, graph):
        self.points.plot(fig, graph)
