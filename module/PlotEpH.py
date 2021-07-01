#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.PlotFct import ltPlotFct

import numpy as np

class ltPlotEpH:
    def __init__(self,
                 element,
                 C_tr,
                 pH_min = 0,
                 pH_max = 14,
                 E_min = -.1,
                 E_max = .1,
                 color = defaults.color,
                 text_color = None,
                 show_species = True,
                 linewidth = defaults.linewidths['plotfct']
                ):
        self.element = element

        self.C_tr = C_tr
        self.pH_min = pH_min
        self.pH_max = pH_max
        self.E_min = E_min
        self.E_max = E_max
        self.color = color
        self.text_color = color
        if text_color is not None :
            self.text_color = text_color
        self.linewidth = linewidth
        self.show_species = show_species
        self.data_file = __import__('ltLaTeXpyplot.data.EpH.{}'.format(self.element), fromlist = [''])
        self.computed = False

    def compute(self):
        E_min, E_max = self.E_min, self.E_max
        pH_min, pH_max = self.pH_min, self.pH_max
        pC = -np.log10(self.C_tr)
        for sep in self.data_file.seps:
            for pH in [sep.pHa, sep.pHb]:
                if type(pH) is not str:
                    pH_min = min([pH_min, pH(pC)])
                    pH_max = max([pH_max, pH(pC)])
            for Ep in [sep.Ea, sep.Eb]:
                if type(Ep) is not str:
                    list_E = [E_min, E_max]
                    for pH in [sep.pHa, sep.pHb]:
                        if type(pH) is not str:
                            list_E.append(Ep(pC, pH(pC)))
                        elif pH == 'min':
                            list_E.append(Ep(pC, pH_min))
                        elif pH == 'max':
                            list_E.append(Ep(pC, pH_max))
                    E_min = min(list_E)
                    E_max = max(list_E)
        self.E_min, self.E_max = E_min, E_max
        self.pH_min, self.pH_max = pH_min, pH_max
        self.computed = True

    def compute_with(self, others):
        if not self.computed:
            self.compute()
        E_min, E_max = self.E_min, self.E_max
        pH_min, pH_max = self.pH_min, self.pH_max
        for PlotEpH in others:
            PlotEpH.compute()
            E_min = min([E_min, PlotEpH.E_min])
            E_max = max([E_max, PlotEpH.E_max])
            pH_min = min([pH_min, PlotEpH.pH_min])
            pH_max = max([pH_max, PlotEpH.pH_max])
        for PlotEpH in [self]+others:
            PlotEpH.E_min, PlotEpH.E_max = E_min, E_max
            PlotEpH.pH_min, PlotEpH.pH_max = pH_min, pH_max

    def plot(self, fig, graph):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
            
        if not self.computed:
            self.compute()
            
        from ltLaTeXpyplot.module.EpHgeneric import EpHgeneric
        data = EpHgeneric(pH_min = self.pH_min,
                          pH_max = self.pH_max,
                          E_min = self.E_min,
                          E_max = self.E_max,
                          conc = self.C_tr
                         )

        for sep in self.data_file.seps:
            data.addsep(sep)
        for spe in self.data_file.spes:
            data.addspe(spe)

        seps = []
        for sep in data.seps:
            seps.append(
                ltPlotFct(sep[0], sep[1], label = None, color = self.color, linewidth = self.linewidth)
            )
        element = self.element
        if '_' in element:
            index = element.index('_')
            element = element[:index]
        seps[0].label = '{element}, $C_\\mathrm{{tr}} = \\SI{{{C}}}{{mol.L^{{-1}}}}$'.format(
            element = element,
            C = self.C_tr
        )
        for sep in seps:
            sep.plot(fig, graph)
            
        if self.show_species:
            ax = fig.graphs[graph].graph
            for spe in data.spes:
                ax.text(spe[0],
                        spe[1],
                        spe[2],
                        color = self.text_color,
                        verticalalignment = 'center',
                        horizontalalignment = 'center'
                       )
