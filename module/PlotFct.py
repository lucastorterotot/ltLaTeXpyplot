#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults

import numpy as np

class ltPlotFct:
    def __init__(self,
                 x, y,
                 label = None,
                 color = defaults.color,
                 dashes = defaults.dashes,
                 marker = None, markersize = defaults.marker_size,
                 linewidth = defaults.linewidths['plotfct'],
                 Fs = 1,
                 Nfft = 256,
                 pad_to = None,
                 padding = 0,
                 noverlap = None,
                 cmap = defaults.cmap):
        self.label = label
        self.x = x
        if type(x) == list:
            self.x = np.array(x)
        if callable(y):
            self.y = y(x)
        else:
            self.y = y
        if type(y) == list:
            self.y = np.array(y)
        self.color = color
        self.dashes = dashes
        self.marker = marker
        self.markersize = defaults.marker_size if marker is not None else None
        self.TF_computed = False
        self.linewidth = linewidth
        self.Fs = Fs
        self.Nfft = Nfft
        self.pad_to = pad_to
        self.padding = padding
        self.noverlap = noverlap
        self.cmap = cmap

    def plot(self, fig, graph):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        fig.graphs[graph].graph.plot(self.x,
                                     self.y,
                                     color = self.color,
                                     linewidth = self.linewidth,
                                     label = self.label,
                                     marker = self.marker,
                                     markersize = self.markersize,
                                     dashes = self.dashes
                                    )

    def compute_TF(self, **kwargs):
        ys = self.y

        if self.padding > 0:
            ys = np.pad(self.y, int(self.padding/2), mode = 'constant')

        self.tf = np.fft.fftshift(np.fft.fft(ys))
        self.f = np.arange(len(self.tf)) * self.Fs/len(self.tf) - .5*self.Fs

        self.TF = ltPlotFct(
            self.f,
            np.square(np.abs(self.tf)),
            **kwargs
        )

        self.TF_computed = True

    def plot_TF(self, fig, graph, **kwargs):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        if not self.TF_computed:
            self.compute_TF(**kwargs)
        self.TF.plot(fig, graph)

    def plot_TFrp(self, fig, graph, **kwargs):
        fig.color_theme_candidate = False
        ax = fig.graphs[graph].graph
        if self.pad_to is None:
            self.pad_to = self.Nfft
        if self.noverlap is None:
            self.noverlap = int(self.Nfft/2)
        ax.specgram(self.y,
                    Fs = self.Fs,
                    cmap = self.cmap,
                    NFFT = self.Nfft,
                    pad_to = self.pad_to,
                    noverlap = self.noverlap,
                    **kwargs
                   )
