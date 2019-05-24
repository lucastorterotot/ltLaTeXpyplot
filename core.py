#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Importing packages

import numpy as np
import scipy as sc

from scipy.constants import golden
import scipy.optimize as spo
from scipy.integrate import odeint

import matplotlib as mpl
mpl.use('pgf')
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

from matplotlib.patches import FancyArrowPatch

from mpl_toolkits.mplot3d import Axes3D


### Defining global variables for this package

lang = 'FR'

marker_size_default = 4
color_default = 'C0'
marker_pts_default = '+'
dashes_default=[]
cmap_default = 'plasma'

linewidths = {
    'grid' : .5,
    'gridaxis' : .75,
    'majorticks' : .7,
    'minorticks' : .35,
    'plotfct' : 1,
    'plotpts' : .4,
    'plotpts_e' : 1,
    'capsize' : 3,
    'capthick' : .4,
    'contour2d' : 1,
    'surface' : 0,
    'scalfield' : 0,
    'vectfield' : .5,
    'vectfieldline' : .5,
    'NMR' : .25,
    'NMR integral' : .25,
    }

inches_per_cm = 0.3937007874 # Convert cm to inch

### LaTeX parameters

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
    "figure.figsize": figsize(0.9,1./golden),     # default fig size of 0.9 textwidth
    "pgf.preamble": [                       # plots will be generated using this preamble
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts because your computer can handle it :)
        r"\usepackage[T1]{fontenc}",   
        r"\usepackage{sistyle}",        
        ]
    }

pgf_with_latex['pgf.preamble'] += [r"\SIproductsign{\!\times\!}\SIunitsep{\,}\SIunitdot{{\fontfamily{cmr}\cdot}}"]
if lang == 'FR':
    pgf_with_latex['pgf.preamble'] += [r"\SIdecimalsign{,}\SIthousandsep{\,}"]

mpl.rcParams.update(pgf_with_latex)

### Defining usefull tools

def axes_comma(x, pos):  # formatter function takes tick label and tick position
    s = str(x)
    string = '\\num{{'
    if '.' in s:
        ind = s.index('.')
        int_part = s[:ind]
        dec_part = s[ind+1:]
        string += int_part
        if dec_part is not '0':
            string += '.'+dec_part
    else:
        string += s    
    string += '}}'
    return string

def ltPlotPieautopct(x, unit='%', maxdec=1):
    return '\\SI{{'+str(round(x,maxdec))+'}}{'+unit+'}'

axes_format_comma = tkr.FuncFormatter(axes_comma)  # make formatter

def add_colorbar(plot, ltGraph):
    if ltGraph.projection == '3d':
        shrink = .75
    else:
        shrink = 1.
    clb = plt.colorbar(plot, shrink=shrink, ax=ltGraph.graph)
    clb_FR_ticks = []
    for tick in clb.get_ticks():
        clb_FR_ticks.append('\\num{'+str(tick)+'}')
    clb.set_ticks(clb.get_ticks())
    clb.set_ticklabels(clb_FR_ticks)
    clb.ax.tick_params(labelsize=pgf_with_latex['xtick.labelsize'])
    if ltGraph.cmap_label is not None:
        clb.ax.set_title(ltGraph.cmap_label, fontsize=pgf_with_latex['axes.labelsize'])
          
def factorial (x):
    result = 1
    if x > 1:
        for k in range(1,x+1):
            result*=k
    return result

### Package core

class ltFigure:
    def __init__(self, name='fig', title=None, page_width_cm=17, width_frac=.8, height_width_ratio=1./golden, tight_layout=False):
        self.name = name
        self.title = title
        self.page_width_cm = page_width_cm
        self.width_frac = width_frac
        self.height_width_ratio = height_width_ratio

        self.fig_width_inches = page_width_cm * width_frac * inches_per_cm
        self.fig_height_inches= self.fig_width_inches * height_width_ratio

        self.figsize = [self.fig_width_inches, self.fig_height_inches]

        plt.clf() # TODO check that there is no conflict with other figures
        self.fig = plt.figure(figsize=self.figsize)
        self.graphs = {}
        self.tight_layout = tight_layout

    def update(self):
        if self.title is not None:
            self.fig.suptitle(self.title, fontsize=pgf_with_latex["font.size"]+.95)
        for graph in self.graphs.keys():
            self.graphs[graph].update()
        if self.tight_layout :
            self.fig.tight_layout()

    def save(self, format='pgf'):
        self.update()
        self.fig.savefig('{}-pyplot.{}'.format(self.name, format),bbox_inches='tight')

    def addgraph(self, name, **kwargs):
        if not name in self.graphs.keys():
            self.graphs[name] = ltGraph(self, name, **kwargs)
        else:
            raise NameError('Figure {} already has a graph named {}.'.format(self.name, name))

    def addtwingraph(self, name, twin_of, axis='x', **kwargs):
        self.addgraph(name, twin_of=twin_of, twin_common_axis=axis, **kwargs)

    def testgraph(self, name, position=111):
        if not name in self.graphs.keys():
            self.addgraph(name, position=position)
            print('Warning, auto-generated graph at position {}'.format(position))
            print('with name {}'.format(name))

    def addplot(self, plot, name):
        self.testgraph(name)
        plot.plot(self, name)

        
class ltGraph:
    def __init__(self, fig, name, title=None,
                 twin_of=None, twin_common_axis='x', 
                 x_label=None, y_label=None, z_label=None,
                 x_scaling='linear', y_scaling='linear', z_scaling='linear', projection='rectilinear',
                 x_min=None, x_max=None, y_min=None, y_max=None, z_min=None, z_max=None,
                 x_ticks=True, x_ticks_min=None, x_ticks_max=None, x_ticks_step=None,
                 y_ticks=True, y_ticks_min=None, y_ticks_max=None, y_ticks_step=None,
                 z_ticks=True, z_ticks_min=None, z_ticks_max=None, z_ticks_step=None,
                 minorticks=True,
                 comma_x_major=(lang == 'FR'), comma_x_minor=False,
                 comma_y_major=(lang == 'FR'), comma_y_minor=False,
                 comma_z_major=(lang == 'FR'), comma_z_minor=False,
                 show_grid=False, show_x_axis=False, show_y_axis=False,
                 show_legend=False, legend_location='best', legend_on_side=False,
                 show_cmap_legend=False, cmap_label=None,
                 position=111,
                 share_x=None, share_y=None):
        self.fig = fig
        self.name = name
        self.twin_of = twin_of
        self.twin_common_axis = twin_common_axis
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.z_label = z_label
        self.x_scaling = x_scaling
        self.y_scaling = y_scaling
        self.z_scaling = z_scaling
        self.projection = projection
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max
        self.x_ticks = x_ticks
        self.x_ticks_min = x_ticks_min
        self.x_ticks_max = x_ticks_max
        self.x_ticks_step = x_ticks_step
        self.y_ticks = y_ticks
        self.y_ticks_min = y_ticks_min
        self.y_ticks_max = y_ticks_max
        self.y_ticks_step = y_ticks_step
        self.z_ticks = z_ticks
        self.z_ticks_min = z_ticks_min
        self.z_ticks_max = z_ticks_max
        self.z_ticks_step = z_ticks_step
        self.minorticks = minorticks
        self.comma_x_major = comma_x_major
        self.comma_x_minor = comma_x_minor
        self.comma_y_major = comma_y_major
        self.comma_y_minor = comma_y_minor
        self.comma_z_major = comma_z_major
        self.comma_z_minor = comma_z_minor
        self.show_grid = show_grid
        self.show_x_axis = show_x_axis
        self.show_y_axis = show_y_axis
        self.show_legend = show_legend
        self.legend_location = legend_location
        self.legend_on_side = legend_on_side
        self.position = position
        self.show_cmap_legend = show_cmap_legend
        self.cmap_label = cmap_label
        self.share_x = share_x
        self.share_y = share_y

        if self.twin_of is None:
            self.graph = fig.fig.add_subplot(position, projection=projection, sharex=share_x, sharey=share_y)
        elif self.twin_of in self.fig.graphs.keys():
            if self.twin_common_axis == 'x':
                self.graph = fig.graphs[self.twin_of].graph.twinx()
            elif self.twin_common_axis == 'y':
                self.graph = fig.graphs[self.twin_of].graph.twiny()
        else:
            error_string = '\n' + '  You tried to make a twin graph but it failed. Aborting...'\
                           + '\n'\
                           + '    Graph name: '+self.name\
                           + '\n'\
                           + '    Supposed twin of: '+self.twin_of\
                           + '\n'\
                           + '    Can be twin of: '
            for key in self.fig.graphs.keys():
                error_string += '\n\t'+key
            raise RuntimeError(error_string)
        
        if show_grid:
            self.graph.grid(linewidth=linewidths['grid'])
        if show_x_axis and not (projection=='3d' or x_min is None or x_max is None):
            self.graph.plot([x_min,x_max], [0,0], color='black', linewidth=linewidths['gridaxis'])
        if show_y_axis and not (projection=='3d' or y_min is None or y_max is None):
            self.graph.plot([0,0], [y_min,y_max], color='black', linewidth=linewidths['gridaxis'])

        if not x_ticks:
            plt.setp(self.graph.get_xticklabels(), visible=False)
        if not y_ticks:
            plt.setp(self.graph.get_yticklabels(), visible=False)
        if not z_ticks:
            plt.setp(self.graph.get_zticklabels(), visible=False)

        for ticks_category in ['major', 'minor']:
            if self.projection == 'polar':
                self.graph.tick_params(direction='in', which=ticks_category, width=linewidths[ticks_category+'ticks'])
            else:
                self.graph.tick_params(
                    direction='in',
                    which=ticks_category,
                    bottom=(self.twin_of is None or self.twin_common_axis is not 'y'),
                    top=1,
                    left=(self.twin_of is None or self.twin_common_axis is not 'x'),
                    right=1,
                    width=linewidths[ticks_category+'ticks']
                )

    def update(self):
        if self.title is not None:
            self.graph.set_title(self.title, fontsize=pgf_with_latex["font.size"])
        self.graph.set_xscale(self.x_scaling)
        self.graph.set_yscale(self.y_scaling)
        if self.projection == '3d':
            self.graph.set_zscale(self.z_scaling)

        if self.x_label is not None :
            self.graph.set_xlabel(self.x_label)
        if self.y_label is not None and self.projection is not 'polar':
            self.graph.set_ylabel(self.y_label)
        if self.z_label is not None and self.projection == '3d':
            self.graph.set_zlabel(self.z_label)

        if self.show_legend :
            if self.legend_on_side:
                self.graph.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            else :
                self.graph.legend(loc=self.legend_location)

        if self.x_min is not None and self.x_max is not None :
            self.graph.set_xlim([self.x_min,self.x_max])
        if self.y_min is not None and self.y_max is not None :
            self.graph.set_ylim([self.y_min,self.y_max])
        if self.z_min is not None and self.z_max is not None and self.projection=='3d':
            self.graph.set_zlim([self.z_min,self.z_max])

        if self.x_ticks_step is not None :
            if self.x_ticks_min is None:
                self.x_ticks_min = self.x_min
            if self.x_ticks_max is None:
                self.x_ticks_max = self.x_max
            if self.x_ticks_min is not None and self.x_ticks_max is not None :
                self.graph.xaxis.set_ticks(np.arange(self.x_ticks_min,self.x_ticks_max+self.x_ticks_step/10.,self.x_ticks_step))
        if self.y_ticks_step is not None :
            if self.y_ticks_min is None:
                self.y_ticks_min = self.y_min
            if self.y_ticks_max is None:
                self.y_ticks_max = self.y_max
            if self.y_ticks_min is not None and self.y_ticks_max is not None :
                self.graph.yaxis.set_ticks(np.arange(self.y_ticks_min,self.y_ticks_max+self.y_ticks_step/10.,self.y_ticks_step))
        if self.z_ticks_step is not None and projection=='3d' :
            if self.z_ticks_min is None:
                self.z_ticks_min = self.z_min
            if self.z_ticks_max is None:
                self.z_ticks_max = self.z_max
            if self.z_ticks_min is not None and self.z_ticks_max is not None :
                self.graph.zaxis.set_ticks(np.arange(self.z_ticks_min,self.z_ticks_max+self.z_ticks_step/10.,self.z_ticks_step))

        if self.minorticks :
            self.graph.minorticks_on()
        if self.comma_y_major :
            self.graph.yaxis.set_major_formatter(axes_format_comma)
        if self.comma_y_minor :
            self.graph.yaxis.set_minor_formatter(axes_format_comma)
        if self.comma_x_major :
            self.graph.xaxis.set_major_formatter(axes_format_comma)
        if self.comma_x_minor :
            self.graph.xaxis.set_minor_formatter(axes_format_comma)
        if hasattr(self.graph, 'zaxis'):
            if self.comma_z_major :
                self.graph.zaxis.set_major_formatter(axes_format_comma)
            if self.comma_z_minor :
                self.graph.zaxis.set_minor_formatter(axes_format_comma)

    def fill_between(self, x, y1, y2, alpha=.5, **kwargs):
        self.graph.fill_between(x, y1, y2, alpha=alpha, **kwargs)

    def addarrow(self, x, y, vx, vy):
        self.graph.add_patch(FancyArrowPatch(posA=(x, y), posB=(x+vx, y+vy),
                                             arrowstyle='->', lw=1, 
                                             mutation_scale=7, mutation_aspect=None))

    def test_graph_3d(self):
        if not self.projection == '3d' :
            raise RuntimeError('\n' + '  You tried to draw a 3d object on a non-3d graph. Aborting...'\
                               + '\n'\
                               + '    Graph name: '+self.name\
                               + '\n'\
                               + '    Graph projection: '+self.projection
            )

            
class ltPlotFct:
    def __init__(self,
                 x, y,
                 label=None,
                 color=color_default,
                 dashes=dashes_default,
                 marker=None, markersize=marker_size_default,
                 linewidth=linewidths['plotfct'],
                 Fs=1,
                 Nfft=256,
                 pad_to=None,
                 noverlap=None,
                 cmap=cmap_default):
        self.label = label
        self.x = x
        if callable(y):
            self.y = y(x)
        else:
            self.y = y
        self.color = color
        self.dashes = dashes
        self.marker = marker
        self.markersize = marker_size_default if marker is not None else None
        self.TF_computed = False
        self.linewidth = linewidth
        self.Fs = Fs
        self.Nfft = Nfft
        self.pad_to = pad_to
        self.noverlap = noverlap
        self.cmap = cmap

    def plot(self, fig, graph):
        fig.graphs[graph].graph.plot(self.x, self.y, color=self.color, linewidth=self.linewidth, label=self.label, marker=self.marker, markersize=self.markersize, dashes=self.dashes)

    def compute_TF(self, **kwargs):
        ''' This code has been adapted from
        https://www.physique-experimentale.com/python/transformee_de_fourier.py
        '''
        tf_to_sort = np.fft.fft(self.y)
        f_to_sort = np.fft.fftfreq(n=self.x.shape[-1], d=np.mean(np.diff(self.x)))
        ind = int(len(f_to_sort)/2)
        tf_deb = tf_to_sort[ind:]
        tf_fin = tf_to_sort[:ind]
        self.tf = np.concatenate((tf_deb, tf_fin))
        f_deb = f_to_sort[ind:]
        f_fin = f_to_sort[:ind]
        self.f = np.concatenate((f_deb, f_fin))
        self.psd = np.square(np.abs(self.tf))
        self.psdn = self.psd/self.psd.max()
        self.TF = ltPlotFct(self.f, self.psd, **kwargs)
        self.TF_computed = True

    def plot_TF(self, fig, graph, **kwargs):
        if not self.TF_computed:
            self.compute_TF(**kwargs)
        self.TF.plot(fig, graph)

    def plot_TFrp(self, fig, graph, **kwargs):
        ax = fig.graphs[graph].graph
        if self.pad_to is None:
            self.pad_to = self.Nfft
        if self.noverlap is None:
            self.noverlap = int(self.Nfft/2)
        ax.specgram(self.y, Fs=self.Fs, cmap=self.cmap, NFFT=self.Nfft, pad_to=self.pad_to, noverlap=self.noverlap, **kwargs)
        
class ltPlotFct3d(ltPlotFct):
    def __init__(self, x, y, z, label=None, color=color_default, dashes=dashes_default, marker=None, markersize=marker_size_default, linewidth=linewidths['plotfct'], norm_xy=True, norm_xyz=True):
        ltPlotFct.__init__(self, x, y, label=label, color=color, dashes=dashes, marker=marker, markersize=markersize, linewidth=linewidth)
        if callable(z):
            self.z = z(x,y)
        else:
            self.z = z
        self.norm_xy = norm_xy or norm_xyz
        self.norm_xyz = norm_xyz

    def plot(self, fig, graph):
        fig.graphs[graph].test_graph_3d()
        x = self.x
        y = self.y
        z = self.z
        ax = fig.graphs[graph].graph
        if self.norm_xy :
            ax.set_aspect('equal', adjustable='box')
        if self.norm_xyz :
            max_range = np.array([x.max(), -x.min(), y.max(), -y.min(), z.max(), -z.min()]).max()
            Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(x.max()+x.min())
            Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(y.max()+y.min())
            Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(z.max()+z.min())
            for xb, yb, zb in zip(Xb, Yb, Zb):
                ax.plot([xb], [yb], [zb], 'w')
        ax.plot(x, y, z, color=self.color, linewidth=self.linewidth, label=self.label, marker=self.marker, markersize=self.markersize, dashes=self.dashes)

        
class ltPlotPts(ltPlotFct):
    def __init__(self, x, y, xerr=None, yerr=None, label=None, color=color_default, cmap=cmap_default, marker=marker_pts_default, markersize=marker_size_default, linewidth=linewidths['plotpts'], elinewidth=linewidths['plotpts_e'], capsize=linewidths['capsize'], capthick=linewidths['capthick'], surface=None, alpha=None):
        ltPlotFct.__init__(self, x, y, label=label, color=color, marker=marker, markersize=markersize, linewidth=linewidth)
        self.xerr = xerr
        self.yerr = yerr
        self.elinewidth = elinewidth
        self.capthick = capthick
        self.capsize = capsize
        self.surface = surface
        self.alpha = alpha
        self.cmap = cmap

    def plot(self, fig, graph):
        if self.surface is None:
            fig.graphs[graph].graph.errorbar(self.x, self.y, xerr=self.xerr, yerr=self.yerr, marker=self.marker, markersize=self.markersize, fmt=' ', linewidth=self.linewidth, elinewidth=self.elinewidth,capsize=self.capsize,capthick=self.capthick,color=self.color,label=self.label)
        else :
            fig.graphs[graph].graph.scatter(self.x, self.y, s=self.surface, c=self.color, marker=self.marker, cmap=self.cmap, alpha=self.alpha)
        

class ltPlotPts3d(ltPlotPts):
    def __init__(self, x, y, z, label=None, color=color_default, marker=marker_pts_default, markersize=marker_size_default, cmap=None, norm_xy=True, norm_xyz=True, surface=None, alpha=None):
        ltPlotPts.__init__(self, x, y, label=label, color=color, cmap=cmap, marker=marker, markersize=markersize, surface=surface, alpha=alpha)
        if callable(z):
            self.z = z(x,y)
        else:
            self.z = z
        self.norm_xy = norm_xy or norm_xyz
        self.norm_xyz = norm_xyz

    def plot(self, fig, graph):
        fig.graphs[graph].test_graph_3d()
        x = self.x
        y = self.y
        z = self.z
        ax = fig.graphs[graph].graph
        if self.norm_xy :
            ax.set_aspect('equal', adjustable='box')
        if self.norm_xyz :
            max_range = np.array([x.max(), -x.min(), y.max(), -y.min(), z.max(), -z.min()]).max()
            Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(x.max()+x.min())
            Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(y.max()+y.min())
            Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(z.max()+z.min())
            for xb, yb, zb in zip(Xb, Yb, Zb):
                ax.plot([xb], [yb], [zb], 'w')
        markersize = self.markersize
        if self.surface is not None:
            markersize = self.surface
        ax.scatter(x, y, z, c=self.color, marker=self.marker, s=markersize, label=self.label, cmap=self.cmap, alpha=self.alpha)

        
class ltPlotRegLin(ltPlotPts):
    ''' This code has been taken from
    https://www.physique-experimentale.com/python/ajustement_de_courbe.py
    '''
    def __init__(self, x, y, xerr, yerr, label=None, label_reg=None, color=color_default, color_reg='C3', marker=marker_pts_default, markersize=marker_size_default, linewidth=linewidths['plotfct'], elinewidth=linewidths['plotpts_e'], capsize=linewidths['capsize'], capthick=linewidths['capthick'],
                 p0_x=0, p0_y=0, dashes=dashes_default, give_info=True, info_placement='upper left',
                 verbose=False):
        ltPlotPts.__init__(self,x, y, xerr, yerr, label=label, color=color, marker=marker, markersize=markersize, linewidth=linewidth, elinewidth=elinewidth, capsize=capsize, capthick=capthick)
        self.label_reg = label_reg
        self.color_reg = color_reg
        self.dashes = dashes
        self.give_info = give_info
        self.info_placement = info_placement
        self.verbose = verbose
        
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
            return (y-f(x,p))/np.sqrt(yerr**2 + (Dx_f(x,p)*xerr)**2)

        # initial estimation
        # usually OK but sometimes one need to give a different
        # starting point to make it converge
        p0 = np.array([p0_x,p0_y])

        # minimizing algorithm
        result = spo.leastsq(residual, p0, args=(y, x), full_output=True)

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
            if lang == 'FR':
                print('  Regression lineaire :')
            else :
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
        self.chi2r= chi2r
        self.x_aj = x_aj
        self.y_aj = y_aj

        self.points = ltPlotPts(x, y, xerr, yerr, label=label, color=color, marker=marker, markersize=markersize, linewidth=self.linewidth, elinewidth=self.elinewidth, capsize=self.capsize, capthick=self.capthick)
        self.reglin = ltPlotFct(x_aj, y_aj, label=label_reg, color=color_reg, dashes=dashes, linewidth=self.linewidth)
        
    def plot(self, fig, graph):
        self.plot_reg(fig, graph)
        self.plot_pts(fig, graph)

    def plot_reg(self, fig, graph):
        self.reglin.plot(fig, graph)
        if self.give_info:
            x_info = 0.5
            y_info = 0.5
            multialignment='center'
            verticalalignment='center'
            horizontalalignment='center'
            if 'left' in self.info_placement :
                x_info = 0.025
                multialignment='left'
                horizontalalignment='left'
            if 'right' in self.info_placement :
                x_info = 0.975
                multialignment='right'
                horizontalalignment='right'
            if 'upper' in self.info_placement :
                y_info = 0.95
                verticalalignment='top'
            if 'lower' in self.info_placement :
                y_info = 0.05
                verticalalignment='bottom'
            else :
                pass
            ax = fig.graphs[graph].graph

            reglintxt = "Linear regression:"
            if lang == 'FR':
                reglintxt = "R\\'egression lin\\'eaire :"
            ax.text(x_info, y_info,
                    reglintxt + " $f(x) = ax+b$" + "\n" + '$a = \\num{{ {0:.2e} }} \pm \\num{{  {1:.2e} }}$'.format(self.popt[0],self.uopt[0]) + "\n" + '$b = \\num{{ {0:.2e} }} \pm \\num{{ {1:.2e} }}$'.format(self.popt[1],self.uopt[1]),
                    transform = ax.transAxes, multialignment=multialignment, verticalalignment=verticalalignment, horizontalalignment=horizontalalignment)

    def plot_pts(self, fig, graph):
        self.points.plot(fig, graph)
    
class ltPlotPie:
    def __init__(self, sizes, explode=None, labels=None, colors=None, autopct=None, pctdistance=.6, shadow=True, labeldistance=1.1, startangle=90, counterclock=True, wedgeprops=None, textprops=None, frame=False, rotatelabels=False, norm_xy=True):
        self.sizes = sizes
        self.explode = explode
        self.labels = labels
        self.colors = colors
        if autopct is not None:
            self.autopct = autopct
        else:
            self.autopct = ltPlotPieautopct
        self.pctdistance = pctdistance
        self.shadow = shadow
        self.labeldistance = labeldistance
        self.startangle = startangle
        self.counterclock = counterclock
        self.wedgeprops = wedgeprops
        self.textprops = textprops
        self.frame = frame
        self.rotatelabels = rotatelabels
        self.norm_xy = norm_xy

    def plot(self, fig, graph):
        ax = fig.graphs[graph].graph
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        for ticks_category in ['major', 'minor']:
            ax.tick_params(direction='in', which=ticks_category, bottom=0, top=0, left=0, right=0, width=linewidths[ticks_category+'ticks'])
        if self.norm_xy:
            ax.axis('equal')
        ax.pie(self.sizes, explode = self.explode, labels = self.labels, colors = self.colors, autopct = self.autopct, pctdistance = self.pctdistance, shadow = self.shadow, labeldistance = self.labeldistance, startangle = self.startangle, counterclock = self.counterclock, wedgeprops = self.wedgeprops, textprops = self.textprops, frame = self.frame, rotatelabels = self.rotatelabels)
        

class ltPlotHist:
    def __init__(self, x, bins=None, range=None, weights=None, cumulative=False, color=color_default, label=None, show_uncert=False, fill=True, linewidth=linewidths['plotfct']):
        self.x = [x]
        self.bins = bins
        self.set_binning()
        self.range = range
        if weights is None:
            weights = np.zeros(len(x))
            weights += 1
        self.weights = [weights]
        self.cumulative = cumulative
        self.color = color
        self.label = label
        self.show_uncert = show_uncert
        self.y = None
        self.erry = None
        self.fill = fill
        self.linewidth = linewidth

    def set_binning(self):
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

    def stack(self, others):
        for attr_key in ['x', 'weights']:
            attr = getattr(self, attr_key)
            for other in others:
                attr += getattr(other, attr_key)
            setattr(self, attr_key, attr)
        self.set_binning()

    def plot_stack(self, fig, graph, others, set_integral=None, scale=None):
        do_uncert, self.show_uncert = self.show_uncert, False
        histos = [self]+others
        if set_integral is not None:
            integral_stacked = 0
            for hist in histos:
                integral_stacked += hist.get_integral()
            scale = set_integral/integral_stacked
        if scale is not None:
            for hist in histos:
                hist.scale(scale)
        for hist in histos:
            index = histos.index(hist)
            hist.stack(histos[index+1:])
            hist.plot(fig, graph)
        if do_uncert:
            self._plot_uncerts(fig, graph)
        self.show_uncert = do_uncert

    def _plot_uncerts(self, fig, graph):
        for k in range(len(self.y)):
            if not(self.y[k] == 0 and fig.graphs[graph].y_scaling=='log'):
                up_unc =self.y[k]+self.erry[k]
                down_unc = self.y[k]-self.erry[k]
                if fig.graphs[graph].y_scaling=='log' and down_unc <= 0:
                    down_unc = _min
                fig.graphs[graph].graph.fill([self.binning[k+1],self.binning[k],self.binning[k],self.binning[k+1]], [down_unc, down_unc, up_unc, up_unc], fill=False, hatch='xxxxx', linewidth=0, clip_path=None)
        
    def get_integral(self):
        self.set_binning()
        result = 0
        for k in range(len(self.weights)):
            for l in range(len(self.weights[k])):
                x_value = self.x[k][l]
                if x_value >= self.binning[-1]:
                    index = len(self.binning)-1
                else:
                    index = next(x[0] for x in enumerate(self.binning) if x[1] >= x_value)
                bin_width = self.binning[index]-self.binning[index-1]
                result += self.weights[k][l] * bin_width
        return result

    def scale(self, value):
        for k in range(len(self.weights)):
            self.weights[k] *= value

    def set_integral(self, value):
        integral = self.get_integral()
        self.scale(value/integral)

    def norm_bins(self):
        self.set_binning()
        for k in range(len(self.weights)):
            for l in range(len(self.weights[k])):
                x_value = self.x[k][l]
                if x_value >= self.binning[-1]:
                    index = len(self.binning)-1
                else:
                    index = next(x[0] for x in enumerate(self.binning) if x[1] >= x_value)
                bin_width = self.binning[index]-self.binning[index-1]
                self.weights[k][l] *= 1/bin_width

    def compute(self):
        values = []
        weights = []
        for x in self.x:
            values = values + [val for val in x]
        for w in self.weights:
            weights = weights + [val for val in w]
        hist, bin_edges = np.histogram(values, bins=self.bins, range=self.range, weights=weights, density=False)
        if self.cumulative:
            for k in range(1,len(hist)):
                hist[k] += hist[k-1]
        self.y = hist
        self.bins = bin_edges
        self.set_binning()
        erry = np.zeros(len(hist))
        for k in range(len(hist)):
            Nerry = 0
            Werry = 0
            for l in range(len(values)):
                value = values[l]
                weight = weights[l]
                if value >= self.binning[k] and value < self.binning[k+1]:
                    Nerry += 1
                    Werry += weight
                if self.cumulative and value < self.binning[k]:
                    Nerry += 1
                    Werry += weight
            if Nerry == 0 :
                erry[k] = 0
            else:
                erry[k] = np.sqrt(hist[k]*Werry/Nerry)
        self.erry = erry

    def plot(self, fig, graph):
        self.compute()
        _min = 0
        if fig.graphs[graph].y_scaling=='log':
            if fig.graphs[graph].y_min is not None:
                _min = fig.graphs[graph].y_min
            else:
                _min = min([value-1 for value in self.y if not value ==0 ])
                if _min <= 0:
                    _min = 1
        if self.fill:
            linewidth=0
        else:
            linewidth=linewidths['plotfct']
        binning_seq = [self.binning[-1],self.binning[0]]
        mini = min([max([self.y.min(), _min]), _min])
        y_sequence = [mini, mini]
        for k in range(len(self.y)):
            binning_seq += [self.binning[k], self.binning[k+1]]
            y_sequence += [max([self.y[k], _min]), max([self.y[k], _min])]
        fig.graphs[graph].graph.fill(binning_seq, y_sequence, color=self.color, linewidth=linewidth, clip_path=None, label=self.label, fill=self.fill)
        if self.show_uncert:
            self._plot_uncerts(fig, graph)
            
    def plot_pts(self, fig, graph, yerr=True, xerr=True, marker='o'):
        self.compute()
        erry = self.erry
        xs = np.zeros(len(self.y))
        errx = np.zeros(len(self.y))
        for k in range(len(xs)):
            xs[k] = (self.binning[k+1]+self.binning[k])/2
            errx[k] = (self.binning[k+1]-self.binning[k])/2
            if not xerr:
                errx[k] = None
            if not yerr:
                erry[k] = None
        label_passed = False
        for k in range(len(self.y)):
            if not(self.y[k] == 0 and fig.graphs[graph].y_scaling=='log'):
                label = None
                if not label_passed:
                    label = self.label
                    label_passed = True
                fig.addplot(ltPlotPts(xs[k], self.y[k], yerr=erry[k], xerr=errx[k], marker=marker, color=self.color, capsize=0, label=label), graph)
        
class ltPlotScalField:
    def __init__(self, x, y, z_fct, C_fct=None, cmap=cmap_default, levels=None, Nlevels=None, color=color_default, label=None, clabel=False, norm_xy=True, norm_xyz=False, alpha=1, alpha_3d=0.5, use_cmap=True, linewidth=linewidths['scalfield'], linewidths=linewidths['contour2d']):
        self.label = label
        self.x = x
        self.y = y
        self.z_fct = z_fct
        self.cmap = cmap
        self.clabel = clabel
        self.levels = levels
        self.Nlevels = Nlevels
        self.color = color
        self.alpha = alpha
        self.alpha_3d = alpha_3d
        self.norm_xy = norm_xy or norm_xyz
        self.norm_xyz = norm_xyz
        self.use_cmap = use_cmap
        self.linewidth = linewidth
        self.linewidths = linewidths
        self.C_fct = C_fct

    def plot(self, fig, graph):
        if fig.graphs[graph].projection == '3d':
            self._plot3d(fig, graph)
        else :
            self._plot2d(fig, graph)

    def plot_field(self, fig, graph):
        self.plot(fig, graph)

    def _plot_contour_init(self, fig, graph):
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        z_fct = self.z_fct
        xs, ys = self.x, self.y
        if callable(self.z_fct):
            xs, ys = np.meshgrid(xs, ys)
            z_fct = self.z_fct(xs, ys)
        if self.levels is None and self.Nlevels is not None:
            self.levels = mpl.ticker.MaxNLocator(nbins=self.Nlevels).tick_values(z_fct.min(), z_fct.max())
        return xs, ys, z_fct

    def plot_contour(self, fig, graph):
        xs, ys, z_fct = self._plot_contour_init(fig, graph)
        if self.levels is not None :
            current_contour=fig.graphs[graph].graph.contour(xs, ys, z_fct, origin='lower', linewidths=self.linewidths, cmap=self.cmap, levels=self.levels)
        else:
            current_contour=fig.graphs[graph].graph.contour(xs, ys, z_fct, origin='lower', linewidths=self.linewidths, cmap=self.cmap)
        if fig.graphs[graph].show_cmap_legend:
            add_colorbar(current_contour, fig.graphs[graph])
        if self.clabel :
            fig.graphs[graph].graph.clabel(current_contour, inline=1, fmt=r'${value}$'.format(value='%1.1f'), fontsize=pgf_with_latex['legend.fontsize']-1)
        current_contour=0 

    def plot_contourf(self, fig, graph): 
        xs, ys, z_fct = self._plot_contour_init(fig, graph)
        if self.levels is not None:
            imshow = fig.graphs[graph].graph.contourf(xs, ys, z_fct, cmap = self.cmap, levels = self.levels)
        else:
            imshow = fig.graphs[graph].graph.contourf(xs, ys, z_fct, cmap = self.cmap)
        if fig.graphs[graph].show_cmap_legend:
            add_colorbar(imshow, fig.graphs[graph])   
            
    def _plot2d(self, fig, graph):
        aspect='auto'
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
            aspect='equal'
        z_fct = self.z_fct
        xs, ys = self.x, self.y
        if callable(self.z_fct):
            xs, ys = np.meshgrid(xs, ys)
            z_fct = self.z_fct(xs, ys)
        imshow = fig.graphs[graph].graph.imshow(z_fct, cmap=self.cmap, extent=(min(self.x), max(self.x), min(self.y), max(self.y)), origin='lower', alpha=self.alpha, aspect=aspect)
        if fig.graphs[graph].show_cmap_legend:
            add_colorbar(imshow, fig.graphs[graph])

    def _plot3d(self, fig, graph):
        if self.alpha == 1 :
            self.alpha = self.alpha_3d
        _ScalField3d = ltPlotSurf(self.x, self.y, z_fct=self.z_fct, C_fct=self.C_fct, label=self.label, alpha=self.alpha, color=self.color, cmap=self.cmap, norm_xy=self.norm_xy, norm_xyz=self.norm_xyz, use_cmap=self.use_cmap, linewidth=self.linewidth)
        _ScalField3d.plot(fig, graph)


class ltPlotSurf:
    def __init__(self, theta, phi, x_fct=None, y_fct=None, z_fct=None, R_fct=None, C_fct=None, label=None, alpha=0.5, color=color_default, cmap=cmap_default, norm_xy=True, norm_xyz=True, use_cmap=False, linewidth=linewidths['surface']):
        if R_fct is not None:
            def x_fct(t, p):
                return R_fct(t, p) * np.sin(t) * np.cos(p)
            def y_fct(t, p):
                return R_fct(t, p) * np.sin(t) * np.sin(p)
            def z_fct(t, p):
                return R_fct(t, p) * np.cos(t)
        elif z_fct is not None and x_fct is None and y_fct is None :
            def x_fct(t, p):
                return t
            def y_fct(t, p):
                return p
        self.theta = theta
        self.phi = phi
        self.x_fct = x_fct
        self.y_fct = y_fct
        self.z_fct = z_fct
        self.R_fct = R_fct
        self.label = label
        self.alpha = alpha
        self.color = color
        self.cmap = cmap
        self.norm_xy = norm_xy or norm_xyz
        self.norm_xyz = norm_xyz
        self.use_cmap = use_cmap
        self.linewidth = linewidth
        self.C_fct = C_fct

    def plot(self, fig, graph):
        if fig.graphs[graph].projection == '3d':
            self._plot3d(fig, graph)
        else :
            self._plot2d(fig, graph)

    def _plot2d(self, fig, graph):
        _Surf2d = ltPlotScalField(self.theta, self.phi, z_fct=self.z_fct, cmap=self.cmap, color=self.color, label=self.label, norm_xy=self.norm_xy, norm_xyz=self.norm_xyz, alpha=self.alpha, use_cmap=self.use_cmap, linewidth=self.linewidth)
        _Surf2d.plot(fig, graph)

    def _plot3d(self, fig, graph):
        fig.graphs[graph].test_graph_3d()
        x, y, z = self.x_fct, self.y_fct, self.z_fct
        theta, phi = np.meshgrid(self.theta, self.phi)
        if callable(x) :
            x = x(theta, phi)
        if callable(y) :
            y = y(theta, phi)
        if callable(z) :
            z = z(theta, phi)
        ax = fig.graphs[graph].graph
        if self.norm_xy :
            ax.set_aspect('equal', adjustable='box')
        if self.norm_xyz :
            max_range = np.array([x.max(), -x.min(), y.max(), -y.min(), z.max(), -z.min()]).max()
            Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(x.max()+x.min())
            Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(y.max()+y.min())
            Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(z.max()+z.min())
            for xb, yb, zb in zip(Xb, Yb, Zb):
                ax.plot([xb], [yb], [zb], 'w')
        method = ax.plot_surface
        if self.use_cmap:
            C_fct_eff = z
            if callable(self.C_fct):
                C_fct_eff = self.C_fct(theta, phi)
            norm = mpl.colors.Normalize(vmin=C_fct_eff.min().min(), vmax=C_fct_eff.max().max())
            facecolors = getattr(mpl.cm, self.cmap)(norm(C_fct_eff))
            surf = method(x, y, z, rstride=1, cstride=1, linewidth=self.linewidth, alpha=self.alpha, cmap=self.cmap, facecolors=facecolors)
        else:
            surf = method(x, y, z, rstride=1, cstride=1, linewidth=self.linewidth, alpha=self.alpha, color=self.color, edgecolors=self.color)
        if not self.linewidth == 0 :
            surf.set_facecolor((1,1,1,0))
        if fig.graphs[graph].show_cmap_legend and self.use_cmap:
            m = mpl.cm.ScalarMappable(cmap=getattr(mpl.cm, self.cmap), norm=norm)
            m.set_array([])
            add_colorbar(m, fig.graphs[graph])
        
class ltPlotVectField2d:
    def __init__(self, x, y, vx_fct, vy_fct, label=None, color=color_default, cmap=cmap_default, use_cmap=False, C_fct=None, norm_xy=True, label_fieldline=None, color_fieldline=color_default, dashes_fieldline=dashes_default, linewidth=linewidths['vectfield'], linewidth_fieldline=linewidths['vectfieldline']):
        self.label = label
        self.x = x
        self.y = y
        self.vx_fct = vx_fct
        self.vy_fct = vy_fct
        self.color = color
        self.norm_xy = norm_xy
        self.linewidth = linewidth

        self.label_fieldline = label_fieldline
        self.color_fieldline = color_fieldline
        self.dashes_fieldline = dashes_fieldline
        self.linewidth_fieldline = linewidth_fieldline

        self.cmap = cmap
        self.use_cmap = use_cmap
        self.C_fct = C_fct

    def plot(self, fig, graph):
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        vx, vy = self.vx_fct, self.vy_fct
        xs, ys = self.x, self.y
        if callable(self.vx_fct) and callable(self.vy_fct):
            xs, ys = np.meshgrid(xs, ys)
            vx = self.vx_fct(xs, ys)
            vy = self.vy_fct(xs, ys)
        color = self.color
        if self.use_cmap:
            C_fct_eff = self.C_fct
            if callable(self.C_fct):
                C_fct_eff = self.C_fct(xs, ys).flatten()
            if self.C_fct is None:
                C_fct_eff = ((vx**2+vy**2)**.5).flatten()
            norm = mpl.colors.Normalize()
            norm.autoscale(C_fct_eff)
            color = getattr(mpl.cm, self.cmap)(norm(C_fct_eff))
        fig.graphs[graph].graph.quiver(xs, ys, vx, vy, linewidth=self.linewidth, label=self.label, color=color)
        if fig.graphs[graph].show_cmap_legend:
            m = mpl.cm.ScalarMappable(cmap=getattr(mpl.cm, self.cmap), norm=norm)
            m.set_array([])
            add_colorbar(m, fig.graphs[graph])

    def plot_fieldline(self, fig, graph, point, startT, endT, stepT, color=None, label=None, dashes=None):
        if color is None:
            color = self.color_fieldline
        if label is None:
            label = self.label_fieldline
        if dashes is None:
            dashes = self.dashes_fieldline
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        T = np.linspace(startT, endT, stepT)
        def _field(p, t):
            x, y = p
            return self.vx_fct(x, y), self.vy_fct(x, y)
        line_xy = odeint(_field, point, T).transpose()
        fig.graphs[graph].graph.plot(line_xy[0], line_xy[1], label=label, color=color, dashes=dashes, linewidth=self.linewidth_fieldline)

    def plot_streamplot(self, fig, graph, start_points=None, density='undef', color=None, linewidth=None, **kwargs):
        if color is None:
            color = self.color_fieldline
        if linewidth is None:
            linewidth = self.linewidth_fieldline
        if density == 'undef':
            density=1
            if start_points is not None:
                density = len(start_points)
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        vx, vy = self.vx_fct, self.vy_fct
        xs, ys = self.x, self.y
        if callable(self.vx_fct) and callable(self.vy_fct):
            xs, ys = np.meshgrid(xs, ys)
            vx = self.vx_fct(xs, ys)
            vy = self.vy_fct(xs, ys)
        if callable(color):
            color = color(xs, ys)
        if callable(linewidth):
            linewidth = linewidth(xs, ys)
        strm = fig.graphs[graph].graph.streamplot(xs, ys, vx, vy, start_points=start_points, density=density, color=color, linewidth=linewidth, **kwargs)
        if fig.graphs[graph].show_cmap_legend:
            add_colorbar(strm.lines, fig.graphs[graph])
        
        
class ltPlotVectField3d(ltPlotVectField2d):
    def __init__(self, x, y, z, vx_fct, vy_fct, vz_fct, label=None, color=color_default, cmap=cmap_default, use_cmap=False, C_fct=None, norm_xyz=True, label_fieldline=None, color_fieldline=color_default, dashes_fieldline=dashes_default, linewidth=linewidths['vectfield'], linewidth_fieldline=linewidths['vectfieldline']):
        ltPlotVectField2d.__init__(self, x, y, vx_fct, vy_fct, label=label, color=color, cmap=cmap, use_cmap=use_cmap, C_fct=C_fct, norm_xy=norm_xyz, label_fieldline=label_fieldline, color_fieldline=color_fieldline, dashes_fieldline=dashes_fieldline, linewidth=linewidth, linewidth_fieldline=linewidth_fieldline)
        self.z = z
        self.vz_fct = vz_fct

    def plot(self, fig, graph):
        fig.graphs[graph].test_graph_3d()
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        xs, ys, zs = self.x, self.y, self.z
        vx, vy, vz = self.vx_fct, self.vy_fct, self.vz_fct
        if callable(self.vx_fct) and callable(self.vy_fct) and callable(self.vz_fct):
            xs, ys, zs = np.meshgrid(xs, ys, zs)
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
            norm = mpl.colors.Normalize()
            norm.autoscale(C_fct_eff)
            color = getattr(mpl.cm, self.cmap)(norm(C_fct_eff))
        fig.graphs[graph].graph.quiver(xs, ys, zs, vx, vy, vz, length=0.1, normalize=True, linewidth=self.linewidth, label=self.label, color=color)
        if fig.graphs[graph].show_cmap_legend:
            m = mpl.cm.ScalarMappable(cmap=getattr(mpl.cm, self.cmap), norm=norm)
            m.set_array([])
            add_colorbar(m, fig.graphs[graph])

    def plot_fieldline(self, fig, graph, point, startT, endT, stepT, color=None, label=None, dashes=None):
        fig.graphs[graph].test_graph_3d()
        if color is None:
            color = self.color_fieldline
        if label is None:
            label = self.label_fieldline
        if dashes is None:
            dashes = self.dashes_fieldline
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        T = np.linspace(startT, endT, stepT)
        def _field(p, t):
            x, y, z = p
            return self.vx_fct(x, y, z), self.vy_fct(x, y, z), self.vz_fct(x, y, z)
        line_xyz = odeint(_field, point, T).transpose()
        fig.graphs[graph].graph.plot(line_xyz[0], line_xyz[1], line_xyz[2], label=label, color=color, dashes=dashes, linewidth=self.linewidth_fieldline)

        
class ltPlotNMR:
    def __init__(self, delta_min=0, delta_max=11, Freq_MHz=100, color=color_default, show_integral=True, dashes=dashes_default, linewidth=linewidths['NMR'], integral_linewidth=linewidths['NMR integral']):
        self.delta_min = delta_min
        self.delta_max = delta_max
        self.Freq_MHz = Freq_MHz
        self.color = color
        self.show_integral = show_integral
        self.dashes = dashes
        self.signals = []
        self.linewidth = linewidth
        self.integral_linewidth = integral_linewidth

    def addsignal(self, delta, nbH, mult, J_Hz):
        self.signals.append([delta, nbH, mult, J_Hz])

    def plot(self, fig, graph):
        plt.setp(fig.graphs[graph].graph.get_yticklabels(), visible=False)
        fig.graphs[graph].graph.minorticks_on()

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
        #     fig.fig.text(delta0, max(spectrum), '{}'.format(nbH))
    
        if self.show_integral :
            spectrum_integral = np.zeros(len(spectrum))
            for k in range(1,len(spectrum_integral)):
                spectrum_integral[k] = spectrum_integral[k-1] - spectrum[k]
            spectrum_integral *= -.75*max(spectrum)/min(spectrum_integral)
            spectrum_integral -= 1.25*min(spectrum_integral)
            
            fig.graphs[graph].graph.plot(delta, spectrum_integral, color='black', linewidth=self.integral_linewidth ,label=None)
        fig.graphs[graph].graph.plot(delta, spectrum, color=color, linewidth=self.linewidth , label=None, dashes=self.dashes)
        
        for ticks_category in ['major', 'minor']:
            fig.graphs[graph].graph.tick_params(
                direction='in',
                which=ticks_category,
                bottom=(fig.graphs[graph].twin_of is None or fig.graphs[graph].twin_common_axis is not 'y'),
                top=0,
                left=0,
                right=0,
                width=linewidths[ticks_category+'ticks']
            )
            
        if fig.graphs[graph].x_label is None :
            fig.graphs[graph].graph.set_xlabel("$\\delta$ (ppm)")

        fig.graphs[graph].graph.set_xlim([self.delta_min, self.delta_max])

        fig.graphs[graph].graph.invert_xaxis()

        
class ltPlotEpH:
    def __init__(self, element, C_tr, pH_min=0, pH_max=14, E_min=-.1, E_max=.1, color=color_default, text_color=None, show_species=True, linewidth=linewidths['plotfct']):
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
        try:
            self.data_file = __import__('ltLaTeXpyplot.data.EpH.'+self.element, fromlist=[''])
        except ModuleNotFoundError:
            print('\n' + 'Ouch, seems like there are no data file for element {}.'.format(self.element) + '\n')
            raise
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
        if not self.computed:
            self.compute()
            
        from ltLaTeXpyplot.data.EpH.EpHgeneric import EpHgeneric
        data = EpHgeneric(pH_min=self.pH_min, pH_max=self.pH_max, E_min=self.E_min, E_max=self.E_max, conc=self.C_tr)

        for sep in self.data_file.seps:
            data.addsep(sep)
        for spe in self.data_file.spes:
            data.addspe(spe)

        seps = []
        for sep in data.seps:
            seps.append(ltPlotFct(sep[0], sep[1], label=None, color=self.color, linewidth=self.linewidth))
        element=self.element
        if '_' in element:
            index = element.index('_')
            element = element[:index]
        seps[0].label = '{element}, $C_{{ {ind} }} = \\SI{{ {C} }}{{ {units} }}$'.format(element=element, ind='\\mathrm{{tr}}', C=self.C_tr, units='mol.L^{-1}')
        for sep in seps:
            sep.plot(fig, graph)
            
        if self.show_species:
            ax = fig.graphs[graph].graph
            for spe in data.spes:
                ax.text(spe[0], spe[1], spe[2], color=self.text_color, verticalalignment='center', horizontalalignment='center')
