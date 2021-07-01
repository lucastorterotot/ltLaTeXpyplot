#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults
from ltLaTeXpyplot.module.utils import factorial

import numpy as np
import matplotlib.pyplot as plt

class ltPlotNMR:
    def __init__(self,
                 delta_min = 0,
                 delta_max = 11,
                 Freq_MHz = 100,
                 color = defaults.color,
                 show_integral = True,
                 dashes = defaults.dashes,
                 linewidth = defaults.linewidths['NMR'],
                 integral_linewidth = defaults.linewidths['NMR integral']
                ):
        self.delta_min = delta_min
        self.delta_max = delta_max
        self.Freq_MHz = Freq_MHz
        self.color = color
        self.show_integral = show_integral
        self.dashes = dashes
        self.signals = []
        self.linewidth = linewidth
        self.integral_linewidth = integral_linewidth

    def addsignal(self, NMRsignal):
        self.signals.append(NMRsignal)

    def removesignal(self, NMRsignal):
        self.signals.append(NMRsignal.inverse())

    def plot(self, fig, graph):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        plt.setp(fig.graphs[graph].graph.get_yticklabels(), visible = False)
        fig.graphs[graph].graph.minorticks_on()

        delta = np.arange(self.delta_min, self.delta_max, 1e-5)
        spectrum = 0*delta
        for signal in self.signals:
            delta0 = signal.delta
            nbH = signal.nbH
            mults = signal.mults
            Js = signal.J_Hz
            freq = self.Freq_MHz
            color = self.color
            dashes = self.dashes
            nb_pikes = 1
            for k in mults :
                nb_pikes *= k
            
            pikes_deltas = [0]
            pikes_heights = [1]
        
            for k in range(len(mults)):
                new_pikes_deltas = []
                new_pikes_heights = []
                J_value = Js[k]
                mult = mults[k]
                coeffs_Js_max = .5*(mult-1)
                J_coeffs = np.linspace(-coeffs_Js_max,coeffs_Js_max,mult)
                for pike_delta,pike_height in zip(pikes_deltas,pikes_heights):
                    for m in range(mult):
                        new_pikes_deltas.append(
                            pike_delta+J_value*1./(freq)*J_coeffs[m]
                        )
                        new_pikes_heights.append(
                            pike_height*factorial(mult-1)*1./(2**(mult-1)*factorial(m)*factorial(mult-1-m))
                        )
                pikes_deltas = new_pikes_deltas
                pikes_heights = new_pikes_heights
                    
            for pike_delta,pike_height in zip(pikes_deltas,pikes_heights):
                spectrum += 1./(1+(delta-delta0-pike_delta)**2*freq**2/(1.5e0))*pike_height*nbH
            
        # for signal in signals:
        #     delta0 = signal[0]
        #     nbH = signal[1]
        #     fig.fig.text(delta0, max(spectrum), '{}'.format(nbH))
    
        if self.show_integral :
            spectrum_integral = np.zeros(len(spectrum))
            for k in range(1,len(spectrum_integral)):
                spectrum_integral[k] = spectrum_integral[k-1] - spectrum[k]
            spectrum_integral *= -.75*max(spectrum)/min(spectrum_integral)
            spectrum_integral -= 1.25*min(spectrum_integral)
            
            fig.graphs[graph].graph.plot(delta,
                                         spectrum_integral,
                                         color = 'black',
                                         linewidth = self.integral_linewidth,
                                         label = None
                                        )
        fig.graphs[graph].graph.plot(delta,
                                     spectrum,
                                     color = color,
                                     linewidth = self.linewidth,
                                     label = None,
                                     dashes = self.dashes
                                    )
        
        for ticks_category in ['major', 'minor']:
            fig.graphs[graph].graph.tick_params(
                direction = 'in',
                which = ticks_category,
                bottom = (fig.graphs[graph].twin_of is None or fig.graphs[graph].twin_common_axis != 'y'),
                top = 0,
                left = 0,
                right = 0,
                width = defaults.linewidths[ticks_category+'ticks']
            )
            
        if fig.graphs[graph].x_label is None :
            fig.graphs[graph].graph.set_xlabel("$\\delta$ (ppm)")

        fig.graphs[graph].graph.set_xlim([self.delta_min, self.delta_max])

        fig.graphs[graph].graph.invert_xaxis()
