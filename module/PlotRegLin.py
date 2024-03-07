#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.PlotPts import ltPlotPts
from ltLaTeXpyplot.module.PlotFct import ltPlotFct

import numpy as np
from ltLaTeXpyplot.module.utils import calcule_une_droite
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
                 dashes = defaults.dashes,
                 nb_ch_u = 2,
                 give_info = True,
                 info_placement = 'upper left',
                 verbose = False,
                 from_MC = False,
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
        self.nb_ch_u = nb_ch_u
        self.from_MC = from_MC

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
        
        self.xerr_for_reg = xerr_for_reg
        self.yerr_for_reg = yerr_for_reg

        if not from_MC:
            self.compute()

    def compute(self):
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
            return (y-f(x,p))/np.sqrt(self.yerr_for_reg**2 + (Dx_f(x,p)*self.xerr_for_reg)**2)

        # initial estimation
        # usually OK but sometimes one need to give a different
        # starting point to make it converge
        a0, b0 = calcule_une_droite(self.x, self.y)
        p0 = np.array([a0, b0])

        # minimizing algorithm
        result = spo.leastsq(residual, p0, args = (self.y, self.x), full_output = True)

        # Result:
        # optimized parameters a and b
        exact_popt = result[0]
        # variance-covariance matrix
        pcov = result[1]
        # uncetainties on parameters (1 sigma)
        exact_uopt = np.sqrt(np.abs(np.diagonal(pcov)))

        a, b = exact_popt[0], exact_popt[1]
        u_a, u_b = exact_uopt[0], exact_uopt[1]
        round_param_a = int(self.nb_ch_u - np.log10(u_a))
        round_param_b = int(self.nb_ch_u - np.log10(u_b))

        popt = (np.round(a, round_param_a), np.round(b, round_param_b))
        uopt = (np.round(u_a, round_param_a), np.round(u_b, round_param_b))

        # reduced chi2 for a and b
        chi2r = np.sum(np.square(residual(exact_popt,self.y,self.x)))/(self.x.size-exact_popt.size)

        # R2
        y_mean = self.y.mean()
        SS_tot = ((self.y - y_mean)**2).sum()
        SS_res = ((self.y - (exact_popt[0]*self.x+exact_popt[1]))**2).sum()
        R2 = 1 - SS_res/SS_tot

        if self.verbose:
            print('  Linear regression :')
            print('    f(x) = a * x + b')
            print('    a = {} +/- {} ;'.format(popt[0], uopt[0]))
            print('    b = {} +/- {} ;'.format(popt[1], uopt[1]))
            print('    r^2 = {}.'.format(R2))
            print(' ')

        self.x_aj = np.linspace(min(self.x),max(self.x),100)
        self.y_aj = exact_popt[0]*np.linspace(min(self.x),max(self.x),100)+exact_popt[1]

        self.result = result
        self.popt = popt
        self.exact_popt = exact_popt
        self.pcov = pcov
        self.uopt = uopt
        self.exact_uopt = exact_uopt
        self.chi2r = chi2r
        self.R2 = R2

        self.points = ltPlotPts(
            self.x, self.y, self.xerr, self.yerr,
            label = self.label,
            color = self.color,
            marker = self.marker,
            markersize = self.markersize,
            linewidth = self.linewidth,
            elinewidth = self.elinewidth,
            capsize = self.capsize,
            capthick = self.capthick
        )
        self.reglin = ltPlotFct(
            self.x_aj, self.y_aj,
            label = self.label_reg,
            color = self.color_reg,
            dashes = self.dashes,
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

            reglintxt = "Linear regression"
            if lang == 'FR':
                reglintxt = "R\\'egression lin\\'eaire"
            if self.from_MC:
                reglintxt += " (MC)"
            if lang == 'FR':
                reglintxt += " :"
            else:
                reglintxt += ":"

            infos = [
                '{} $f(x) = ax+b$'.format(reglintxt),
            ]

            pow_a = 0
            a = self.popt[0]
            while abs(a) < 1:
                pow_a -= 1
                a *= 10
            while abs(a) >= 10:
                pow_a += 1
                a /= 10

            if pow_a == 0:
                infos.append(
                    '$a = \\num{{ {0} }} \\pm \\num{{ {1} }}$'.format(
                        a,
                        self.uopt[0],
                    )
                )
            else:
                infos.append(
                    '$a = \\num{{ {0}e{1} }} \\pm \\num{{ {2:.1e} }}$'.format(
                        np.round(a, 10),
                        pow_a,
                        self.uopt[0],
                    ),
                )

            pow_b = 0
            b = self.popt[1]
            while abs(b) < 1:
                pow_b -= 1
                b *= 10
            while abs(b) >= 10:
                pow_b += 1
                b /= 10


            if pow_b == 0:
                infos.append(
                    '$b = \\num{{ {0} }} \\pm \\num{{ {1} }}$'.format(
                        b,
                        self.uopt[1],
                    )
                )
            else:
                infos.append(
                    '$b = \\num{{ {0}e{1} }} \\pm \\num{{ {2:.1e} }}$'.format(
                        np.round(b, 10),
                        pow_b,
                        self.uopt[1],
                    )
                )

            if not self.from_MC:
                infos.append('$r^2 = \\num{{ {0:.4} }}$'.format(self.R2))
            ax.text(x_info, y_info,
                    '\n'.join(infos),
                    transform = ax.transAxes,
                    multialignment = multialignment,
                    verticalalignment = verticalalignment,
                    horizontalalignment = horizontalalignment
                   )

    def plot_pts(self, fig, graph):
        self.points.plot(fig, graph)
