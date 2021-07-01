#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ltLaTeXpyplot.module.default_mpl_settings as defaults

import numpy as np

class ltPlotHist:
    def __init__(self,
                 data = None,
                 weights = None,
                 bins = None, range = None,
                 cumulative = False,
                 color = defaults.color, label = None,
                 show_uncert = False, fill = True,
                 show_bins = False,
                 linewidth = defaults.linewidths['plotfct']):
        self.entries = []
        self.weights = []
        self.bins = bins
        self.range = range
        self.cumulative = cumulative
        self.color = color
        self.label = label
        self.show_uncert = show_uncert
        self.show_bins = show_bins
        self.fill = fill
        self.linewidth = linewidth
        self.x = None
        self.y = None
        self.yerr_up = None
        self.yerr_down = None
        self.xerr_up = None
        self.xerr_down = None
        self.entries_in_bin = None
        self.weights_in_bin = None
        self._set_binning()
        if data is not None:
            self.Fill(data, weights)
        self._stacked_hist = None

    def _set_binning(self):
        self.binning = self.bins
        if not (isinstance(self.bins, list) or isinstance(self.bins, np.ndarray)) and self.bins is not None:
            if getattr(self,  'range', None) is None:
                x_min = self.x[0][0]
                x_max = self.x[0][0]
                for x in self.x:
                    x_min = min([x_min, x.min()])
                    x_max = max([x_max, x.max()])
                    self.binning = np.linspace(x.min(), x.max(), self.bins+1)
            else:
                self.binning = np.linspace(self.range[0], self.range[1], self.bins+1)
        if not isinstance(self.binning, np.ndarray):
            self.binning = np.array(self.binning)
        if self.y is None:
            self.y = np.zeros(len(self.binning)-1)
        if self.yerr_up is None:
            self.yerr_up = np.zeros(len(self.binning)-1)
        if self.yerr_down is None:
            self.yerr_down = np.zeros(len(self.binning)-1)
        if self.entries_in_bin is None:
            self.entries_in_bin = np.zeros(len(self.binning)-1)
        if self.weights_in_bin is None:
            self.weights_in_bin = np.zeros(len(self.binning)-1)
        self.x = (self.binning[1:]+self.binning[:-1])/2
        self.xerr_up = (self.binning[1:]-self.binning[:-1])/2
        self.xerr_down = (self.binning[1:]-self.binning[:-1])/2

    def Fill(self, xs, weights = None):
        self.entries += [val for val in xs]
        if weights is None:
            weights = [1 for val in xs]
        self.weights += [w for w in weights]
        hist, bin_edges = np.histogram(self.entries,
                                       bins = self.bins,
                                       range = self.range,
                                       weights = self.weights,
                                       density = False
                                      )
        if self.cumulative:
            for k in range(1,len(hist)):
                hist[k] += hist[k-1]
        self.y = np.array(hist, dtype = 'float')
        self.entries_in_bin = np.zeros(len(hist))
        self.weights_in_bin = np.zeros(len(hist))
        self.yerr_up = np.zeros(len(hist))
        self.yerr_down = np.zeros(len(hist))
        self.bins = bin_edges
        self._set_binning()
        for k in range(len(hist)):
            Nyerr = 0
            Wyerr = 0
            for l in range(len(self.entries)):
                value = self.entries[l]
                weight = self.weights[l]
                if value >= self.binning[k] and value < self.binning[k+1]:
                    Nyerr += 1
                    Wyerr += weight
                if self.cumulative and value < self.binning[k]:
                    Nyerr += 1
                    Wyerr += weight
            self.entries_in_bin[k] = Nyerr
            self.weights_in_bin[k] = Wyerr
            if Nyerr == 0 :
                self.yerr_up[k] = 0
                self.yerr_down[k] = 0
            else:
                self.yerr_up[k] = np.sqrt(hist[k]*Wyerr/Nyerr)
                self.yerr_down[k] = np.sqrt(hist[k]*Wyerr/Nyerr)

    def SetBinContent(self, bin, value):
        self.y[bin] = value

    def SetBinError(self, bin, value):
        self.SetBinErrorUp(bin, value)
        self.SetBinErrorDown(bin, value)

    def SetBinErrorUp(self, bin, value):
        self.yerr_up[bin] = value

    def SetBinErrorDown(self, bin, value):
        self.yerr_down[bin] = value

    def GetBinContent(self, bin):
        return self.y[bin]

    def GetBinEntries(self, bin):
        return self.entries_in_bin[bin]

    def GetBinError(self, bin):
        return max(
            self.GetBinErrorUp(bin),
            self.GetBinErrorDown(bin)
        )

    def GetBinErrorUp(self, bin):
        return self.yerr_up[bin]

    def GetBinErrorDown(self, bin):
        return self.yerr_down[bin]
        
    def Integral(self):
        self._set_binning()
        result = 0
        for k in range(len(self.weights)):
            value = self.entries[k]
            if value >= self.binning[-1]:
                index = len(self.binning)-1
            else:
                index = next(x[0] for x in enumerate(self.binning) if x[1] >= value)
            bin_width = self.binning[index]-self.binning[index-1]
            result += self.weights[k] * bin_width
        return result

    def Scale(self, value):
        for k in range(len(self.weights)):
            self.weights[k] *= value
        self.y *= value
        self.weights_in_bin *= value
        self.yerr_up *= abs(value)
        self.yerr_down *= abs(value)

    def SetIntegral(self, value):
        self.Scale(value/self.Integral())

    def NormalizeToBinWidth(self):
        self._set_binning()
        for k in range(len(self.weights)):
            value = self.entries[k]
            if value >= self.binning[-1]:
                index = len(self.binning)-1
            else:
                index = next(x[0] for x in enumerate(self.binning) if x[1] >= value)
            bin_width = self.binning[index]-self.binning[index-1]
            self.weights[k] *= 1/bin_width
        for k in range(len(self.y)):
            bin_width = self.binning[k+1]-self.binning[k]
            self.y[k] *= 1/bin_width
            self.weights_in_bin[k] *= 1/bin_width
            self.yerr_up[k] *= 1/bin_width
            self.yerr_down[k] *= 1/bin_width

    def plot(self, fig, graph):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        _min = 0
        if fig.graphs[graph].y_scaling == 'log':
            if fig.graphs[graph].y_min is not None:
                _min = fig.graphs[graph].y_min
            else:
                _min = min([value-1 for value in self.y if not value == 0 ])
                if _min <= 0:
                    _min = 1
        if self.fill:
            linewidth = 0
        else:
            linewidth = defaults.linewidths['plotfct']
        binning_seq = [self.binning[-1],self.binning[0]]
        mini = min([max([self.y.min(), _min]), _min])
        y_sequence = [mini, mini]
        for k in range(len(self.y)):
            binning_seq += [self.binning[k], self.binning[k+1]]
            y_sequence += [max([self.y[k], _min]), max([self.y[k], _min])]
        fig.graphs[graph].graph.fill(binning_seq,
                                     y_sequence,
                                     color = self.color,
                                     linewidth = linewidth,
                                     clip_path = None,
                                     label = self.label,
                                     fill = self.fill
                                    )
        if self.show_bins:
            for k in range(0, len(binning_seq), 2):
                xpos = binning_seq[k]
                y1 = mini
                y2 = y_sequence[k]
                if y2 > mini:
                    ltPlotFct([xpos, xpos], [y1, y2], color = 'black', linewidth = .5).plot(fig, graph)
            ltPlotFct(binning_seq+[binning_seq[-1]],
                      y_sequence+[mini],
                      color = 'black',
                      linewidth = .5).plot(fig, graph)
        if self.show_uncert:
            self._plot_uncerts(fig, graph)

    def _stack(self, others):
        import copy
        self._stacked_hist = copy.copy(self)
        for other in others:
            self._stacked_hist.entries.append(other.entries)
            self._stacked_hist.weights.append(other.weights)
            if (len(self.y) != len(other.y)):
                raise ValueError('You try to stack two histograms with different number of bins!')
            elif any(self.x[k] != other.x[k] for k in range(len(self.x))):
                raise ValueError('You try to stack two histograms with different binning!')
            else:
                for k in range(len(self.y)):
                    self._stacked_hist.y[k] += other.y[k]
                    self._stacked_hist.entries_in_bin[k] += other.entries_in_bin[k]
                    self._stacked_hist.weights_in_bin[k] += other.weights_in_bin[k]
                    self._stacked_hist.yerr_up[k] = ((self._stacked_hist.yerr_up[k])**2 + (other.yerr_up[k])**2)**.5
                    self._stacked_hist.yerr_down[k] = ((self._stacked_hist.yerr_down[k])**2 + (other.yerr_down[k])**2)**.5
                    

    def plot_stack(self, fig, graph, others, SetIntegral = None, scale = None):
        do_uncert, self.show_uncert = self.show_uncert, False
        histos = others
        if self not in others:
            histos = [self]+others
        if SetIntegral is not None:
            integral_stacked = 0
            for hist in histos:
                integral_stacked += hist.Integral()
            scale = SetIntegral/integral_stacked
        if scale is not None:
            for hist in histos:
                hist.Scale(scale)
        for hist in histos:
            index = histos.index(hist)
            hist._stack(histos[index+1:])
            hist._stacked_hist.plot(fig, graph)
        if do_uncert:
            self._stacked_hist._plot_uncerts(fig, graph)
        self.show_uncert = do_uncert

    def _plot_uncerts(self, fig, graph):
        for k in range(len(self.y)):
            if not(self.y[k] == 0 and fig.graphs[graph].y_scaling == 'log'):
                up_unc = self.y[k]+self.yerr_up[k]
                down_unc = self.y[k]-self.yerr_down[k]
                if fig.graphs[graph].y_scaling == 'log' and down_unc <= 0:
                    down_unc = _min
                fig.graphs[graph].graph.fill(
                    [self.binning[k+1],self.binning[k],self.binning[k],self.binning[k+1]],
                    [down_unc, down_unc, up_unc, up_unc],
                    fill = False,
                    hatch = 'xxxxx',
                    linewidth = 0,
                    clip_path = None
                )
            
    def plot_pts(self, fig, graph, yerr = True, xerr = True, marker = 'o'):
        if not isinstance(self.color, str):
            fig.color_theme_candidate = False
        elif self.color != defaults.color:
            fig.color_theme_candidate = False
        if yerr:
            yerr_up = self.yerr_up
            yerr_down = self.yerr_down
        else:
            yerr_up = [None for y in self.yerr_up]
            yerr_down = [None for y in self.yerr_down]
        if xerr:
            xerr_up = self.xerr_up
            xerr_down = self.xerr_down
        else:
            xerr_up = [None for x in self.xerr_up]
            xerr_down = [None for x in self.xerr_down]
        label_passed = False
        for k in range(len(self.y)):
            if not(self.y[k] == 0 and fig.graphs[graph].y_scaling == 'log'):
                label = None
                if not label_passed:
                    label = self.label
                    label_passed = True
                fig.addplot(
                    ltPlotPts(
                        [self.x[k]], [self.y[k]],
                        yerr = [[yerr_down[k]], [yerr_up[k]]],
                        xerr = [[xerr_down[k]], [xerr_up[k]]],
                        marker = marker, color = self.color,
                        capsize = 0, label = label
                    ), graph)
