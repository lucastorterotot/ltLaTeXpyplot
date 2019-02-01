#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Importing packages

from os.path import expanduser
homedir = expanduser("~")

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
cmap_default = 'inferno'

inches_per_cm = 0.3937007874 # Convert cm to inch

### Defining usefull tools

def axes_comma(x, pos):  # formatter function takes tick label and tick position
    s = str(x)
    ind = s.index('.')
    int_part = s[:ind]
    dec_part = s[ind+1:]
    string = '\\num{{' + int_part
    if dec_part is not '0':
        string += '.'+dec_part
    string += '}}'
    return string

axes_format_comma = tkr.FuncFormatter(axes_comma)  # make formatter

def factorial (x):
    result = 1
    if x > 1:
        for k in range(1,x+1):
            result*=k
    return result

def figsize(scale,ratio):
    fig_width = 17*inches_per_cm*scale    # width in inches
    fig_height = fig_width*ratio              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

### LaTeX parameters

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
mpl.rcParams.update(pgf_with_latex)

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
            self.fig.suptitle(self.title, fontsize=10.95)
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
                 x_label=None, y_label=None, z_label=None,
                 x_scaling='linear', y_scaling='linear', z_scaling='linear', projection='rectilinear',
                 x_min=None, x_max=None, y_min=None, y_max=None, z_min=None, z_max=None,
                 x_ticks=True, x_ticks_min=None, x_ticks_max=None, x_ticks_step=None,
                 y_ticks=True, y_ticks_min=None, y_ticks_max=None, y_ticks_step=None,
                 z_ticks=True, z_ticks_min=None, z_ticks_max=None, z_ticks_step=None,
                 minorticks=True,
                 comma_x_major=True, comma_x_minor=False,
                 comma_y_major=True, comma_y_minor=False,
                 comma_z_major=True, comma_z_minor=False,
                 show_grid=False, show_x_axis=False, show_y_axis=False,
                 show_legend=False, legend_location='best', legend_on_side=False,
                 position=111,
                 share_x=None, share_y=None):
        self.fig = fig
        self.name = name
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
        self.share_x = share_x
        self.share_y = share_y

        self.graph = fig.fig.add_subplot(position, projection=projection, sharex=share_x, sharey=share_y)        

        if show_grid:
            fig.fig.grid(linewidth=.5)
        if show_x_axis and not (projection=='3d' or x_min is None or x_max is None):
            fig.graphs[graph].graph.plot([x_min,x_max], [0,0], color='black', linewidth=.75)
        if show_y_axis and not (projection=='3d' or y_min is None or y_max is None):
            fig.graphs[graph].graph.plot([0,0], [y_min,y_max], color='black', linewidth=.75)

        if not x_ticks:
            plt.setp(self.graph.get_xticklabels(), visible=False)
        if not y_ticks:
            plt.setp(self.graph.get_yticklabels(), visible=False)
        if not z_ticks:
            plt.setp(self.graph.get_zticklabels(), visible=False)

        if self.projection == 'polar':
            self.graph.tick_params(direction='in',which='major', width=0.7)
            self.graph.tick_params(direction='in',which='minor', width=0.35)
        else:
            self.graph.tick_params(direction='in',which='major',bottom=1, top=1, left=1, right=1, width=0.7)
            self.graph.tick_params(direction='in',which='minor',bottom=1, top=1, left=1, right=1, width=0.35)


    def update(self):
        if self.title is not None:
            self.graph.set_title(self.title, fontsize=10)
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

        if self.x_ticks and self.x_ticks_step is not None :
            if self.x_ticks_min is None:
                self.x_ticks_min = self.x_min
            if self.x_ticks_max is None:
                self.x_ticks_max = self.x_max
            if self.x_ticks_min is not None and self.x_ticks_max is not None :
                self.graph.xaxis.set_ticks(np.arange(self.x_ticks_min,self.x_ticks_max+self.x_ticks_step/10.,self.x_ticks_step))
        if self.y_ticks and self.y_ticks_step is not None :
            if self.y_ticks_min is None:
                self.y_ticks_min = self.y_min
            if self.y_ticks_max is None:
                self.y_ticks_max = self.y_max
            if self.y_ticks_min is not None and self.y_ticks_max is not None :
                self.graph.yaxis.set_ticks(np.arange(self.y_ticks_min,self.y_ticks_max+self.y_ticks_step/10.,self.y_ticks_step))
        if self.z_ticks and self.z_ticks_step is not None and projection=='3d' :
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

    def addarrow(self, x, y, vx, vy, head_width=0.05, head_length=0.1, fc='k', ec='k', length_includes_head=True, **kwargs):
        self.graph.add_patch(FancyArrowPatch(posA=(x, y), posB=(x+vx, y+vy),
                                             arrowstyle='->', lw=1, 
                                             mutation_scale=7, mutation_aspect=None))
        #self.graph.arrow(x, y, vx, vy, head_width=head_width, head_length=head_length, fc=fc, ec=ec, length_includes_head=length_includes_head, **kwargs)

    def test_graph_3d(self):
        if not self.projection == '3d' :
            raise RuntimeError('\n' + '  You tried to draw a 3d object on a non-3d graph. Aborting...'\
                               + '\n'\
                               + '    Graph name: '+self.name\
                               + '\n'\
                               + '    Graph projection: '+self.projection
            )

            
class ltPlotFct:
    def __init__(self, x, y, label=None, color=color_default, dashes=dashes_default, marker=None, markersize=marker_size_default):
        self.label = label
        self.x = x
        self.y = y
        self.color = color
        self.dashes = dashes
        self.marker = marker
        self.markersize = marker_size_default if marker is not None else None
        self.TF_computed = False

    def plot(self, fig, graph):
        fig.graphs[graph].graph.plot(self.x, self.y, color=self.color, linewidth=1, label=self.label, marker=self.marker, markersize=self.markersize, dashes=self.dashes)

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
        
class ltPlotFct3d(ltPlotFct):
    def __init__(self, x, y, z, label=None, color=color_default, dashes=dashes_default, marker=None, markersize=marker_size_default):
        ltPlotFct.__init__(self, x, y, label=label, color=color, dashes=dashes, marker=marker, markersize=markersize)
        self.z = z

    def plot(self, fig, graph):
        fig.graphs[graph].test_graph_3d()
        fig.graphs[graph].graph.plot(self.x, self.y, self.z, color=self.color, linewidth=1, label=self.label, marker=self.marker, markersize=self.markersize, dashes=self.dashes)

        
class ltPlotPts(ltPlotFct):
    def __init__(self, x, y, xerr=None, yerr=None, label=None, color=color_default, marker=marker_pts_default, markersize=marker_size_default):
        ltPlotFct.__init__(self, x, y, label=label, color=color, marker=marker, markersize=markersize)
        self.xerr = xerr
        self.yerr = yerr

    def plot(self, fig, graph):
        fig.graphs[graph].graph.errorbar(self.x, self.y, xerr=self.xerr, yerr=self.yerr, marker=self.marker, markersize=self.markersize, fmt=' ', linewidth=0.4, elinewidth=1,capsize=3,capthick=0.4,color=self.color,label=self.label)
        

class ltPlotPts3d(ltPlotPts):
    def __init__(self, x, y, z, label=None, color=color_default, marker=marker_pts_default, markersize=marker_size_default):
        ltPlotPts.__init__(self, x, y, label=label, color=color, marker=marker, markersize=markersize)
        self.z = z

    def plot(self, fig, graph):
        fig.graphs[graph].test_graph_3d()
        fig.graphs[graph].graph.scatter(self.x, self.y, self.z, c=self.color, marker=self.marker, s=self.markersize, label=self.label)

        
class ltPlotRegLin(ltPlotPts):
    ''' This code has been taken from
    https://www.physique-experimentale.com/python/ajustement_de_courbe.py
    '''
    def __init__(self, x, y, xerr, yerr, label=None, label_reg=None, color=color_default, color_reg='C3', marker=marker_pts_default, markersize=marker_size_default,
                 p0_x=0, p0_y=0, dashes=dashes_default, give_info=True, info_placement='upper left'):
        ltPlotPts.__init__(self,x, y, xerr, yerr, label=label, color=color, marker=marker, markersize=markersize)
        self.label_reg = label_reg
        self.color_reg = color_reg
        self.dashes = dashes
        self.give_info = give_info
        self.info_placement = info_placement
        
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

        self.points = ltPlotPts(x, y, xerr, yerr, label=label, color=color, marker=marker, markersize=markersize)
        self.reglin = ltPlotFct(x_aj, y_aj, label=label_reg, color=color_reg, dashes=dashes)
        
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
            mpl.rc('text', usetex=True)

            reglintxt = "Linear regression:"
            if lang == 'FR':
                reglintxt = "R\\'egression lin\\'eaire :"
            ax.text(x_info, y_info,
                    reglintxt + " $f(x) = ax+b$" + "\n" + '$a = \\num{{ {0:.2e} }} \pm \\num{{  {1:.2e} }}$'.format(self.popt[0],self.uopt[0]) + "\n" + '$b = \\num{{ {0:.2e} }} \pm \\num{{ {1:.2e} }}$'.format(self.popt[1],self.uopt[1]),
                    transform = ax.transAxes, multialignment=multialignment, verticalalignment=verticalalignment, horizontalalignment=horizontalalignment)

    def plot_pts(self, fig, graph):
        self.points.plot(fig, graph)

        
class ltPlotContour2d:
    def __init__(self, x, y, z_fct, cmap=cmap_default, levels=None, label=None, clabel=False, norm_xy=True):
        self.label = label
        self.x = x
        self.y = y
        self.z_fct = z_fct
        self.X, self.Y = np.meshgrid(x, y)
        self.cmap = cmap
        self.levels = levels
        self.clabel = clabel
        self.norm_xy = norm_xy

    def plot(self, fig, graph):
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        if self.levels is not None :
            current_contour=fig.graphs[graph].graph.contour(self.X, self.Y, self.z_fct(self.X, self.Y), origin='lower', linewidths=1, cmap=self.cmap, levels=self.levels)
        else:
            current_contour=fig.graphs[graph].graph.contour(self.X, self.Y, self.z_fct(self.X, self.Y), origin='lower', linewidths=1, cmap=self.cmap)
        if self.clabel :
            fig.graphs[graph].graph.clabel(current_contour, inline=1, fmt='%1.1f', fontsize=8)
        current_contour=0

        
class ltPlotScalField:
    def __init__(self, x, y, z_fct, cmap=cmap_default, color=color_default, label=None, norm_xy=True, norm_xyz=False, alpha=1, alpha_3d=0.5, use_cmap=True):
        self.label = label
        self.x = x
        self.y = y
        self.z_fct = z_fct
        self.X, self.Y = np.meshgrid(x, y)
        self.cmap = cmap
        self.color = color
        self.alpha = alpha
        self.alpha_3d = alpha_3d
        self.norm_xy = norm_xy or norm_xyz
        self.norm_xyz = norm_xyz
        self.use_cmap = use_cmap

    def plot(self, fig, graph):
        if fig.graphs[graph].projection == '3d':
            self._plot3d(fig, graph)
        else :
            self._plot2d(fig, graph)

    def _plot2d(self, fig, graph):
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        fig.graphs[graph].graph.imshow(self.z_fct(self.X, self.Y), cmap=self.cmap, extent=(min(self.x), max(self.x), min(self.y), max(self.y)), origin='lower', alpha=self.alpha)

    def _plot3d(self, fig, graph):
        if self.alpha == 1 :
            self.alpha = self.alpha_3d
        _ScalField3d = ltPlotSurf(self.x, self.y, z_fct=self.z_fct, label=self.label, alpha=self.alpha, color=self.color, cmap=self.cmap, norm_xy=self.norm_xy, norm_xyz=self.norm_xyz, use_cmap=self.use_cmap)
        _ScalField3d.plot(fig, graph)


class ltPlotSurf:
    def __init__(self, theta, phi, x_fct=None, y_fct=None, z_fct=None, R_fct=None, label=None, alpha=0.5, color=color_default, cmap=cmap_default, norm_xy=True, norm_xyz=True, use_cmap=False):
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
        self.Theta, self.Phi = np.meshgrid(theta, phi)
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

    def plot(self, fig, graph):
        if fig.graphs[graph].projection == '3d':
            self._plot3d(fig, graph)
        else :
            self._plot2d(fig, graph)

    def _plot2d(self, fig, graph):
        _Surf2d = ltPlotScalField(self.theta, self.phi, z_fct=self.z_fct, cmap=self.cmap, color=self.color, label=self.label, norm_xy=self.norm_xy, norm_xyz=self.norm_xyz, alpha=self.alpha, use_cmap=self.use_cmap)
        _Surf2d.plot(fig, graph)

    def _plot3d(self, fig, graph):
        fig.graphs[graph].test_graph_3d()
        x = self.x_fct(self.Theta, self.Phi)
        y = self.y_fct(self.Theta, self.Phi)
        z = self.z_fct(self.Theta, self.Phi)
        ax = fig.graphs[graph].graph
        if self.norm_xy :
            ax.set_aspect('equal', adjustable='box')
        if self.norm_xyz :
            max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max()
            Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(x.max()+x.min())
            Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(y.max()+y.min())
            Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(z.max()+z.min())
            for xb, yb, zb in zip(Xb, Yb, Zb):
                ax.plot([xb], [yb], [zb], 'w')
        if self.use_cmap:
            fig.graphs[graph].graph.plot_surface(x, y, z, rstride=1, cstride=1, linewidth=0, alpha=self.alpha, cmap=self.cmap)
        else:
            fig.graphs[graph].graph.plot_surface(x, y, z, rstride=1, cstride=1, linewidth=0, alpha=self.alpha, color=self.color)
        
class ltPlotVectField2d:
    def __init__(self, x, y, vx_fct, vy_fct, label=None, color=color_default, norm_xy=True, label_fieldline=None, color_fieldline=color_default, dashes_fieldline=dashes_default):
        self.label = label
        self.x = x
        self.y = y
        self.vx_fct = vx_fct
        self.vy_fct = vy_fct
        self.X, self.Y = np.meshgrid(x, y)
        self.color = color
        self.norm_xy = norm_xy

        self.label_fieldline = label_fieldline
        self.color_fieldline = color_fieldline
        self.dashes_fieldline = dashes_fieldline

    def plot(self, fig, graph):
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        fig.graphs[graph].graph.quiver(self.X, self.Y, self.vx_fct(self.X, self.Y), self.vy_fct(self.X, self.Y), linewidth=.5, label=self.label, color=self.color)

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
        fig.graphs[graph].graph.plot(line_xy[0], line_xy[1], label=label, color=color, dashes=dashes, linewidth=.5)
        
        
class ltPlotVectField3d(ltPlotVectField2d):
    def __init__(self, x, y, z, vx_fct, vy_fct, vz_fct, label=None, norm_xyz=True, label_fieldline=None, color_fieldline=color_default, dashes_fieldline=dashes_default):
        ltPlotVectField2d.__init__(self, x, y, vx_fct, vy_fct, label=label, norm_xy=norm_xyz, label_fieldline=label_fieldline, color_fieldline=color_fieldline, dashes_fieldline=dashes_fieldline)
        self.z = z
        self.vz_fct = vz_fct
        self.X, self.Y, self.Z = np.meshgrid(x, y, z)

    def plot(self, fig, graph):
        fig.graphs[graph].test_graph_3d()
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        fig.graphs[graph].graph.quiver(self.X, self.Y, self.Z, self.vx_fct(self.X, self.Y, self.Z), self.vy_fct(self.X, self.Y, self.Z), self.vz_fct(self.X, self.Y, self.Z), length=0.1, normalize=True, linewidth=.5, label=self.label, color=self.color)

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
        fig.graphs[graph].graph.plot(line_xyz[0], line_xyz[1], line_xyz[2], label=label, color=color, dashes=dashes, linewidth=.5)

        
class ltPlotNMR:
    def __init__(self, delta_min=0, delta_max=11, Freq_MHz=100, color=color_default, show_integral=True, dashes=dashes_default):
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
            
            fig.graphs[graph].graph.plot(delta, spectrum_integral, color='black', linewidth=.25 ,label=None)
        fig.graphs[graph].graph.plot(delta, spectrum, color=color, linewidth=.25 , label=None, dashes=self.dashes)
            
        fig.graphs[graph].graph.tick_params(direction='in',which='major',bottom=1, top=0, left=0, right=0, width=0.7)
        fig.graphs[graph].graph.tick_params(direction='in',which='minor',bottom=1, top=0, left=0, right=0, width=0.35)

        if fig.graphs[graph].x_label is None :
            fig.graphs[graph].graph.set_xlabel("$\\delta$ (ppm)")

        fig.graphs[graph].graph.set_xlim([self.delta_min, self.delta_max])

        fig.graphs[graph].graph.invert_xaxis()

        
class ltPlotEpH:
    def __init__(self, element, C_tr, pH_min=0, pH_max=14, E_min=-.1, E_max=.1, color=color_default, text_color='black', show_species=True):
        self.element = element

        self.C_tr = C_tr
        self.pH_min = pH_min
        self.pH_max = pH_max
        self.E_min = E_min
        self.E_max = E_max
        self.color = color
        self.text_color = text_color
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
                    list_E = [E_min, E_max, Ep(pC, pH_min), Ep(pC, pH_max)]
                    for pH in [sep.pHa, sep.pHb]:
                        if type(pH) is not str:
                            list_E.append(Ep(pC, pH(pC)))
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
        data = EpHgeneric(pH_min=self.pH_min-.5, pH_max=self.pH_max+.5, E_min=self.E_min-.1, E_max=self.E_max+.1, conc=self.C_tr)

        for sep in self.data_file.seps:
            data.addsep(sep)
        for spe in self.data_file.spes:
            data.addspe(spe)

        seps = []
        for sep in data.seps:
            seps.append(ltPlotFct(sep[0], sep[1], label=None, color=self.color))
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
                ax.text(spe[0], spe[1], spe[2], color=self.color, verticalalignment='center', horizontalalignment='center')
