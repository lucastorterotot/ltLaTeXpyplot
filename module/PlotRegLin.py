#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.PlotPts import ltPlotPts
from ltLaTeXpyplot.module.PlotFct import ltPlotFct

import numpy as np
import scipy.optimize as spo

class ltPlotRegLin(ltPlotPts):
    ''' This code has been taken from
    https://www.physique-experimentale.com/python/ajustement_de_courbe.py
    '''
    def __init__(self,
                 x, y, xerr, yerr,
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
                 p0_x = 0,
                 p0_y = 0,
                 dashes = defaults.dashes,
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
        self.label_reg = label_reg
        self.color_reg = color_reg
        self.dashes = dashes
        self.give_info = give_info
        self.info_placement = info_placement
        self.verbose = verbose

        xerr_for_reg = xerr
        yerr_for_reg = yerr

        if len(xerr_for_reg) == 2:
                if len(xerr_for_reg[0]) == len(x) and len(xerr_for_reg[1]) == len(x):
                    xerr_for_reg = (
                        np.array(xerr_for_reg[0])
                        + np.array(xerr_for_reg[1])
                    )/2

        if len(yerr_for_reg) == 2:
                if len(yerr_for_reg[0]) == len(x) and len(yerr_for_reg[1]) == len(x):
                    yerr_for_reg = (
                        np.array(yerr_for_reg[0])
                        + np.array(yerr_for_reg[1])
                    )/2
        
        # linear function to adjust
        def f(x,p):
            a,b = p 
            return a*x+b
        
        # its derivative
        def Dx_f(x,p):
            a,b = p
            return a

        # difference to data
        def residual(p, y, x):
            return (y-f(x,p))/np.sqrt(yerr_for_reg**2 + (Dx_f(x,p)*xerr_for_reg)**2)

        # initial estimation
        # usually OK but sometimes one need to give a different
        # starting point to make it converge
        p0 = np.array([p0_x,p0_y])

        # minimizing algorithm
        result = spo.leastsq(residual, p0, args = (y, x), full_output = True)

        # Result:
        # optimized parameters a and b
        popt = result[0];
        # variance-covariance matrix
        pcov = result[1];
        # uncetainties on parameters (1 sigma)
        uopt = np.sqrt(np.abs(np.diagonal(pcov)))

        # reduced chi2 for a and b
        chi2r = np.sum(np.square(residual(popt,y,x)))/(x.size-popt.size)

        if self.verbose:
            print('  Linear regression :')
            print('    f(x) = a * x + b')
            print('    a = {} ;'.format(popt[0]))
            print('    b = {}.'.format(popt[1]))
            print(' ')

        x_aj = np.linspace(min(x),max(x),100)
        y_aj = popt[0]*np.linspace(min(x),max(x),100)+popt[1]

        self.result = result
        self.popt = popt
        self.pcov = pcov
        self.uopt = uopt
        self.chi2r = chi2r
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

            reglintxt = "Linear regression:"
            if lang == 'FR':
                reglintxt = "R\\'egression lin\\'eaire :"
            ax.text(x_info, y_info,
                    '\n'.join([
                        '{} $f(x) = ax+b$'.format(reglintxt),
                        '$a = \\num{{ {0:.2e} }} \\pm \\num{{  {1:.2e} }}$'.format(self.popt[0],self.uopt[0]),
                        '$b = \\num{{ {0:.2e} }} \\pm \\num{{ {1:.2e} }}$'.format(self.popt[1],self.uopt[1])
                        ]),
                    transform = ax.transAxes,
                    multialignment = multialignment,
                    verticalalignment = verticalalignment,
                    horizontalalignment = horizontalalignment
                   )

    def plot_pts(self, fig, graph):
        self.points.plot(fig, graph)
