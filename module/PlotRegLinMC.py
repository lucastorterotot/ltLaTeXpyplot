#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.PlotPts import ltPlotPts
from ltLaTeXpyplot.module.PlotFct import ltPlotFct
from ltLaTeXpyplot.module.PlotRegLin import ltPlotRegLin

import numpy as np
from ltLaTeXpyplot.module.utils import creation_liste_droites, calcule_une_droite

class ltPlotRegLinMC(ltPlotRegLin):
    def __init__(self,
                 x, y, xerr, yerr,
                 N = 10000,
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
        ltPlotRegLin.__init__(self,
                            x, y, xerr, yerr,
                            label = label,
                            label_reg = label_reg,
                            color = color,
                            color_reg = color_reg,
                            marker = marker,
                            markersize = markersize,
                            linewidth = linewidth,
                            elinewidth = elinewidth,
                            capsize = capsize,
                            capthick = capthick,
                            dashes = dashes,
                            nb_ch_u = nb_ch_u,
                            give_info = give_info,
                            info_placement = info_placement,
                            verbose = verbose,
                            from_MC = True,
                           )
        xerr_for_reg = self.xerr_for_reg
        yerr_for_reg = self.yerr_for_reg

        self.N = N

        if distrib_x is None:
            distrib_x = distrib
        if distrib_y is None:
            distrib_y = distrib
        self.distrib_x = distrib_x
        self.distrib_y = distrib_y

        self.compute()

    def compute(self):
        lst_a, lst_b = creation_liste_droites(self.x, self.y, self.xerr_for_reg, self.yerr_for_reg, self.N, self.distrib_x, self.distrib_y)
        a, b = calcule_une_droite(self.x, self.y)
        u_a = np.std(lst_a)
        u_b = np.std(lst_b)

        round_param_a = int(self.nb_ch_u - np.log10(u_a))
        round_param_b = int(self.nb_ch_u - np.log10(u_b))
        
        # optimized parameters a and b
        exact_popt = (a, b)
        popt = (np.round(a, round_param_a), np.round(b, round_param_b))
        # uncetainties on parameters (1 sigma)
        exact_uopt = (u_a, u_b)
        uopt = (np.round(u_a, round_param_a), np.round(u_b, round_param_b))

        if self.verbose:
            print('  Linear regression (MC) :')
            print('    f(x) = a * x + b')
            print('    a = {} +/- {} ;'.format(popt[0], uopt[0]))
            print('    b = {} +/- {} ;'.format(popt[1], uopt[1]))
            print(' ')

        self.x_aj = np.linspace(min(self.x),max(self.x),100)
        self.y_aj = exact_popt[0]*np.linspace(min(self.x),max(self.x),100)+exact_popt[1]

        self.popt = popt
        self.exact_popt = exact_popt
        self.uopt = uopt
        self.exact_uopt = exact_uopt

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
        
