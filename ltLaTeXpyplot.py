import numpy as np
import scipy as sc

import matplotlib as mpl
mpl.use('pgf')
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

from mpl_toolkits.mplot3d import Axes3D

inches_per_cm = 0.3937007874 # Convert cm to inch

def figsize(scale,ratio):
    fig_width = 17*inches_per_cm*scale    # width in inches
    fig_height = fig_width*ratio              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

pgf_with_latex = {                      # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",        # change this if using xetex or luatex
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 10,               # LaTeX default is 10pt font.
    "font.size": 10,
    "legend.fontsize": 9,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.figsize": figsize(0.9,((5.0)**0.5-1.0)/2.0),     # default fig size of 0.9 textwidth
    "pgf.preamble": [                       # plots will be generated using this preamble
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts because your computer can handle it :)
        r"\usepackage[T1]{fontenc}",   
        r"\usepackage{sistyle}",        
        ]
    }
mpl.rcParams.update(pgf_with_latex)

def axes_virgule(x, pos):  # formatter function takes tick label and tick position
    s = str(x)
    ind = s.index('.')
    return s[:ind] + ',' + s[ind+1:]   # change dot to comma

axes_format_virgule = tkr.FuncFormatter(axes_virgule)  # make formatter

def factorial (x):
    result = 1
    if x > 1:
        for k in range(1,x+1):
            result*=k
    return result

marker_size_default = 4
color_default = 'C0'
marker_pts_default = '+'

class ltFigure:
    def __init__(self, name='fig', title=None, page_width_cm=17, width_frac=.8, height_width_ratio=((5.0)**0.5-1.0)/2.0, tight_layout=False):
        self.name = name
        self.title = title
        self.page_width_cm = page_width_cm
        self.width_frac = width_frac
        self.height_width_ratio = height_width_ratio

        self.fig_width_inches = page_width_cm * width_frac * inches_per_cm
        self.fig_height_inches= self.fig_width_inches * height_width_ratio

        self.figsize = [self.fig_width_inches, self.fig_height_inches]

        plt.clf()
        self.fig = plt.figure(figsize=self.figsize)
        if tight_layout :
            self.fig.tight_layout()
        self.graphs = {}

    def save(self, format='pgf'):
        plt.title = self.title
        plt.savefig('{}-pyplot.{}'.format(self.name, format),bbox_inches='tight')

    def addgraph(self, name,
                 x_label=None, y_label=None, z_label=None,
                 x_scaling='linear', y_scaling='linear', z_scaling='linear', projection='rectilinear',
                 x_min=None, x_max=None, y_min=None, y_max=None, z_min=None, z_max=None,
                 x_ticks=True, x_ticks_min=None, x_ticks_max=None, x_ticks_step=None,
                 y_ticks=True, y_ticks_min=None, y_ticks_max=None, y_ticks_step=None,
                 z_ticks=True, z_ticks_min=None, z_ticks_max=None, z_ticks_step=None,
                 minorticks=True,
                 comma_x_major=False, comma_x_minor=False,
                 comma_y_major=False, comma_y_minor=False,
                 comma_z_major=False, comma_z_minor=False,
                 show_grid=False, show_x_axis=False, show_y_axis=False,
                 show_legend=False, legend_on_side=False,
                 position=111,
                 share_x=None, share_y=None):
    
        graph = plt.subplot(position, projection=projection, sharex=share_x, sharey=share_y)

        self.graphs[name] = graph

        if show_grid:
            plt.grid(inewidth=.5)
        if show_x_axis and not (projection=='3d' or x_min is None or x_max is None):
            plt.plot([x_min,x_max], [0,0], color='black', linewidth=.75)
        if show_y_axis and not (projection=='3d' or y_min is None or y_max is None):
            plt.plot([0,0], [y_min,y_max], color='black', linewidth=.75)

        if not x_ticks:
            plt.setp(graph.get_xticklabels(), visible=False)
        if not y_ticks:
            plt.setp(graph.get_yticklabels(), visible=False)
        if not z_ticks:
            plt.setp(graph.get_zticklabels(), visible=False)
    
        if projection == 'polar':
            graph.tick_params(direction='in',which='major', width=0.7)
            graph.tick_params(direction='in',which='minor', width=0.35)
        else:
            graph.tick_params(direction='in',which='major',bottom=1, top=1, left=1, right=1, width=0.7)
            graph.tick_params(direction='in',which='minor',bottom=1, top=1, left=1, right=1, width=0.35)

        graph.set_xscale(x_scaling)
        graph.set_yscale(y_scaling)
        if projection == '3d':
            graph.set_zscale(z_scaling)

        if x_label is not None :
            graph.set_xlabel(x_label)
        if y_label is not None and projection is not 'polar':
            graph.set_ylabel(y_label)
        if z_label is not None and projection == '3d':
            graph.set_zlabel(z_label)

        if show_legend :
            if legend_on_side:
                plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            else :
                plt.legend()

        if x_min is not None and x_max is not None :
            graph.set_xlim([x_min,x_max])
        if y_min is not None and y_max is not None :
            graph.set_ylim([y_min,y_max])
        if z_min is not None and z_max is not None and projection=='3d':
            graph.set_zlim([z_min,z_max])

        if x_ticks and x_ticks_step is not None :
            if x_ticks_min is None:
                x_ticks_min = x_min
            if x_ticks_max is None:
                x_ticks_max = x_max
            if x_ticks_min is not None and x_ticks_max is not None :
                graph.xaxis.set_ticks(np.arange(x_ticks_min,x_ticks_max+x_ticks_step/10.,x_ticks_step))
        if y_ticks and y_ticks_step is not None :
            if y_ticks_min is None:
                y_ticks_min = y_min
            if y_ticks_max is None:
                y_ticks_max = y_max
            if y_ticks_min is not None and y_ticks_max is not None :
                graph.yaxis.set_ticks(np.arange(y_ticks_min,y_ticks_max+y_ticks_step/10.,y_ticks_step))
        if z_ticks and z_ticks_step is not None and projection=='3d' :
            if z_ticks_min is None:
                z_ticks_min = z_min
            if z_ticks_max is None:
                z_ticks_max = z_max
            if z_ticks_min is not None and z_ticks_max is not None :
                graph.zaxis.set_ticks(np.arange(z_ticks_min,z_ticks_max+z_ticks_step/10.,z_ticks_step))

        if minorticks :
            graph.minorticks_on()
        if comma_y_major :
            graph.yaxis.set_major_formatter(axes_format_virgule)
        if comma_y_minor :
            graph.yaxis.set_minor_formatter(axes_format_virgule)
        if comma_x_major :
            graph.xaxis.set_major_formatter(axes_format_virgule)
        if comma_x_minor :
            graph.xaxis.set_minor_formatter(axes_format_virgule)
        if comma_z_major :
            graph.zaxis.set_major_formatter(axes_format_virgule)
        if comma_z_minor :
            graph.zaxis.set_minor_formatter(axes_format_virgule)

    def testgraph(self, name, position=111):
        if not self.graphs[name]:
            self.addgraph(name, position=position)
            print 'Warning, auto-generated graph at position {}'.format(position)
            print 'with name {}'.format(name)

    def addplot(self, plot, name, position=111):
        self.testgraph(name, position=position)
        plot.plot(self, name)

    def addarrow(self, x, y, vx, vy, head_width=0.05, head_length=0.1, fc='k', ec='k'):
        plt.arrow(x, y, vx, vy, head_width=0.05, head_length=0.1, fc='k', ec='k')

    def fill_area(self, x, y1, y2, name, position=111, alpha=.5):
        self.testgraph(name, position)
        self.graphs[name].fill_between(x, y1, y2, alpha=alpha)
        
class ltPlot:
    def __init__(self, x, y, label=None, color=color_default):
        self.label = label
        self.x = x
        self.y = y
        self.color = color
        
        
class ltPlot3d(ltPlot):
    def __init__(self, x, y, z, label=None, color=color_default):
        ltPlot.__init__(self, x, y, label=label, color=color)
        self.z = z

class ltPlotFct(ltPlot):
    def __init__(self, x, y, label=None, color=color_default, dashes=None, marker=None, markersize=marker_size_default):
        ltPlot.__init__(self, x, y, label=label, color=color)
        self.dashes = dashes
        self.marker = marker
        self.markersize = marker_size_default if marker is not None else None

    def plot(self, fig, graph):
        if self.dashes is not None:
            plt.plot(self.x, self.y, color=self.color, linewidth=1, label=self.label, marker=self.marker, markersize=self.markersize, dashes=self.dashes)
        else:
            plt.plot(self.x, self.y, color=self.color, linewidth=1, label=self.label, marker=self.marker, markersize=self.markersize)
            
        
class ltPlotFct3d(ltPlotFct):
    def __init__(self, x, y, z, label=None, color=color_default, dashes=None, marker=None, markersize=marker_size_default):
        ltPlotFct.__init__(self, x, y, label=label, color=color, dashes=dashes, marker=marker, markersize=markersize)
        self.z = z

    def plot(self, fig, graph):
        plt.plot(self.x, self.y, self.z, color=self.color, linewidth=1, label=self.label, marker=self.marker, markersize=self.markersize, dashes=self.dashes)

class ltPlotPts(ltPlotFct):
    def __init__(self, x, y, xerr=None, yerr=None, label=None, color=color_default, marker=marker_pts_default, markersize=marker_size_default):
        ltPlotFct.__init__(self, x, y, label=label, color=color, marker=marker, markersize=markersize)
        self.xerr = xerr
        self.yerr = yerr

    def plot(self, fig, graph):
        plt.errorbar(self.x, self.y, xerr=self.xerr, yerr=self.yerr, marker=self.marker, markersize=self.markersize, fmt=' ', linewidth=0.4, elinewidth=1,capsize=3,capthick=0.4,color=self.color,label=self.label)
        

class ltPlotPts3d(ltPlotPts):
    def __init__(self, x, y, z, label=None, color=color_default, marker=marker_pts_default, markersize=marker_size_default):
        ltPlotPts.__init__(self, x, y, label=label, color=color, marker=marker, markersize=markersize)
        self.z = z

    def plot(self, fig, graph):
        fig.graphs[graph].scatter(self.x, self.y, self.z, c=self.color, marker=self.marker, s=self.markersize, label=self.label)

class ltPlotContour2d:
    def __init__(self, x, y, h, cmap, levels, label=None, clabel=False):
        self.label = label
        self.x = x
        self.y = y
        self.h = h
        self.cmap = cmap
        self.levels = levels
        self.clabel = clabel

    def plot(self, fig, graph):
        current_contour=plt.contour(self.x, self.y, self.h, origin='lower', linewidths=1, cmap=self.cmap, levels=self.levels)
        if self.clabel :
            plt.clabel(current_contour, self.levels[1::2], inline=1, fmt='%1.1f', fontsize=8)
        current_contour=0
        
class ltPlotScalField2d:
    def __init__(self, x, y, V, cmap, label=None):
        self.label = label
        self.x = x
        self.y = y
        self.V = V
        self.cmap = cmap

    def plot(self, fig, graph):
        fig.graphs[graph].imshow(self.V, cmap=self.cmap, extent=(min(self.x), max(self.x), min(self.y), max(self.y)), origin='lower')

class ltPlotVectField2d:
    def __init__(self, x, y, vx, vy, cmap, label=None):
        self.label = label
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.cmap = cmap

    def plot(self, fig, graph):
        fig.graphs[graph].quiver(self.x, self.y, self.vx, self.vy, linewidth=.5, label=self.label, color=self.color)

class ltPlotVectField3d(ltPlotVectField2d):
    def __init__(self, x, y, z, vx, vy, vz, cmap, label=None):
        ltPlotVectField2d.__init__(self, x, y,vx, vy, cmap, label=label)
        self.z = z
        self.vz = vz

    def plot(self, fig, graph):
        fig.graphs[graph].quiver(self.x, self.y, self.z, self.vx, self.vy, self.vz, length=0.1, normalize=True, linewidth=.5, label=self.label, color=self.color)

class ltPlotNMR:
    def __init__(self, delta_min=0, delta_max=11, Freq_MHz=100, color=color_default, show_integral=True, dashes=[1]):
        self.delta_min = delta_min
        self.delta_max = delta_max
        self.Freq_MHz = Freq_MHz
        self.color = color
        self.show_integral = show_integral
        self.dashes = dashes
        self.signals = []

    def addsignal(self, delta, nbH, mult, J_Hz):
        self.signals.append([delta, nbH, mult, J_Hz])

    def plot(self, fig, graph):
        plt.setp(fig.graphs[graph].get_yticklabels(), visible=False)
        fig.graphs[graph].minorticks_on()

        delta = np.arange(self.delta_min, self.delta_max, 1e-5)
        spectrum = 0*delta
        for signal in self.signals:
            delta0 = signal[0]
            nbH = signal[1]
            mults = signal[2]
            Js = signal[3]
            freq = self.Freq_MHz
            color = self.color
            dashes = self.dashes
            nb_pikes = 1
            for k in mults :
                nb_pikes *= k
            
            pikes_deltas = [0]
            pikes_heights = [1]
        
            for k in range(0,len(mults)):
                new_pikes_deltas = []
                new_pikes_heights = []
                J_value = Js[k]
                mult = mults[k]
                coeffs_Js_max = .5*(mult-1)
                J_coeffs = np.arange(-coeffs_Js_max,coeffs_Js_max+1e-6,1)
                for l in range(0,len(pikes_deltas)):
                    for m in range(0,mult):
                        new_pikes_deltas.append(pikes_deltas[l]+J_value*1./(freq)*J_coeffs[m])
                        new_pikes_heights.append(pikes_heights[l]*factorial(mult-1)*1./(2**(mult-1)*factorial(m)*factorial(mult-1-m)))
                pikes_deltas = new_pikes_deltas
                pikes_heights = new_pikes_heights
                    
            for pike in range(0,nb_pikes):
                spectrum += 1./(1+(delta-delta0-pikes_deltas[pike])**2*freq**2/(1.5e0))*pikes_heights[pike]*nbH
            
        # for signal in signals:
        #     delta0 = signal[0]
        #     nbH = signal[1]
        #     plt.text(delta0, max(spectrum), '{}'.format(nbH))
    
        if self.show_integral :
            spectrum_integral = np.zeros(len(spectrum))
            for k in range(1,len(spectrum_integral)):
                spectrum_integral[k] = spectrum_integral[k-1] - spectrum[k]
            spectrum_integral *= -.75*max(spectrum)/min(spectrum_integral)
            spectrum_integral -= 1.25*min(spectrum_integral)
            
            plt.plot(delta, spectrum_integral, color='black', linewidth=.25 ,label=None)
        plt.plot(delta, spectrum, color=color, linewidth=.25 , label=None)
            
        fig.graphs[graph].tick_params(direction='in',which='major',bottom=1, top=0, left=0, right=0, width=0.7)
        fig.graphs[graph].tick_params(direction='in',which='minor',bottom=1, top=0, left=0, right=0, width=0.35)

        fig.graphs[graph].set_xlim([self.delta_min, self.delta_max])

        plt.gca().invert_xaxis()
