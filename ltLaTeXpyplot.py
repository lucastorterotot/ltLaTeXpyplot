#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Importing packages

from os.path import expanduser
homedir = expanduser("~")

import numpy as np
import scipy as sc

import scipy.optimize as spo
from scipy.integrate import odeint

import matplotlib as mpl
mpl.use('pgf')
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

from mpl_toolkits.mplot3d import Axes3D


### Defining global variables for this package

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
    return s[:ind] + ',' + s[ind+1:]   # change dot to comma

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
    "figure.figsize": figsize(0.9,((5.0)**0.5-1.0)/2.0),     # default fig size of 0.9 textwidth
    "pgf.preamble": [                       # plots will be generated using this preamble
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts because your computer can handle it :)
        r"\usepackage[T1]{fontenc}",   
        r"\usepackage{sistyle}",        
        ]
    }
mpl.rcParams.update(pgf_with_latex)

### Package core

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

        plt.clf() # TODO check that there is no conflict with other figures
        self.fig = plt.figure(figsize=self.figsize)
        if tight_layout :
            self.fig.tight_layout()
        self.graphs = {}

    def update(self):
        if self.title is not None:
            self.fig.suptitle(self.title, fontsize=10.95)
        for graph in self.graphs.keys():
            self.graphs[graph].update()

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
            print 'Warning, auto-generated graph at position {}'.format(position)
            print 'with name {}'.format(name)

    def addplot(self, plot, name):
        self.testgraph(name)
        plot.plot(self, name)

    def addarrow(self, x, y, vx, vy, head_width=0.05, head_length=0.1, fc='k', ec='k'):
        self.fig.arrow(x, y, vx, vy, head_width=head_width, head_length=head_length, fc=fc, ec=ec)

        
class ltGraph:
    def __init__(self, fig, name, title=None,
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
        if self.comma_z_major :
            self.graph.zaxis.set_major_formatter(axes_format_comma)
        if self.comma_z_minor :
            self.graph.zaxis.set_minor_formatter(axes_format_comma)

    def fill_between(self, x, y1, y2, alpha=.5, **kwargs):
        self.graph.fill_between(x, y1, y2, alpha=alpha, **kwargs)

            
class ltPlotFct:
    def __init__(self, x, y, label=None, color=color_default, dashes=dashes_default, marker=None, markersize=marker_size_default):
        self.label = label
        self.x = x
        self.y = y
        self.color = color
        self.dashes = dashes
        self.marker = marker
        self.markersize = marker_size_default if marker is not None else None

    def plot(self, fig, graph):
        fig.graphs[graph].graph.plot(self.x, self.y, color=self.color, linewidth=1, label=self.label, marker=self.marker, markersize=self.markersize, dashes=self.dashes)

        
class ltPlotFct3d(ltPlotFct):
    def __init__(self, x, y, z, label=None, color=color_default, dashes=dashes_default, marker=None, markersize=marker_size_default):
        ltPlotFct.__init__(self, x, y, label=label, color=color, dashes=dashes, marker=marker, markersize=markersize)
        self.z = z

    def plot(self, fig, graph):
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
        fig.graphs[graph].graph.scatter(self.x, self.y, self.z, c=self.color, marker=self.marker, s=self.markersize, label=self.label)

        
class ltPlotRegLin(ltPlotPts):
    def __init__(self, x, y, xerr, yerr, label=None, label_reg=None, color=color_default, color_reg='C3', marker=marker_pts_default, markersize=marker_size_default,
                 p0_x=0, p0_y=0, dashes=dashes_default, give_info=True, info_placement='upper left'):
        ltPlotPts.__init__(self,x, y, xerr, yerr, label=label, color=color, marker=marker, markersize=markersize)
        self.label_reg = label_reg
        self.color_reg = color_reg
        self.dashes = dashes
        self.give_info = give_info
        self.info_placement = info_placement
        
        # fonction f décrivant la courbe à ajuster aux données
        def f(x,p):
            a,b = p 
            return a*x+b
        
        # dérivée de la fonction f par rapport à la variable de contrôle x
        def Dx_f(x,p):
            a,b = p
            return a

        # fonction d'écart pondérée par les erreurs
        def residual(p, y, x):
            return (y-f(x,p))/np.sqrt(yerr**2 + (Dx_f(x,p)*xerr)**2)

        # estimation initiale des paramètres
        # elle ne joue généralement aucun rôle
        # néanmoins, le résultat de l'ajustement est parfois aberrant
        # il faut alors choisir une meilleure estimation initiale
        p0 = np.array([p0_x,p0_y])

        # on utilise l'algorithme des moindres carrés non-linéaires 
        # disponible dans la biliothèque scipy (et indirectement la
        # bibliothèque Fortran MINPACK qui implémente l'algorithme
        # de Levenberg-Marquardt) pour déterminer le minimum voulu
        result = spo.leastsq(residual, p0, args=(y, x), full_output=True)

        # on obtient :
        # les paramètres d'ajustement optimaux
        popt = result[0];
        # la matrice de variance-covariance estimée des paramètres
        pcov = result[1];
        # les incertitudes-types sur ces paramètres
        uopt = np.sqrt(np.abs(np.diagonal(pcov)))

        # calcul de la valeur du "chi2 réduit" pour les paramètres ajustés
        chi2r = np.sum(np.square(residual(popt,y,x)))/(x.size-popt.size)

        print '  Regression lineaire :'
        print '    f(x) = a * x + b avec'
        print '    a = {} ;'.format(popt[0])
        print '    b = {}.'.format(popt[1])
        print ' '

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
            x_info = 0.24
            y_info = 0.5
            if 'left' in self.info_placement :
                x_info = 0.025
            if 'right' in self.info_placement :
                x_info = 0.455
            if 'upper' in self.info_placement :
                y_info = 0.85
            if 'lower' in self.info_placement :
                y_info = 0.125
            else :
                pass
            ax = fig.graphs[graph].graph
            ax.text(x_info, y_info + 0.075,"R\\'egression lin\\'eaire : $f(x) = ax+b$",transform = ax.transAxes)
            ax.text(x_info, y_info,'$a = \\num{{ {0:.2e} }} \pm \\num{{  {1:.2e} }}$'.format(self.popt[0],self.uopt[0]),transform = ax.transAxes)
            ax.text(x_info, y_info - 0.075,'$b = \\num{{ {0:.2e} }} \pm \\num{{ {1:.2e} }}$'.format(self.popt[1],self.uopt[1]),transform = ax.transAxes)

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

        
class ltPlotScalField2d:
    def __init__(self, x, y, z_fct, cmap=cmap_default, label=None, norm_xy=True):
        self.label = label
        self.x = x
        self.y = y
        self.z_fct = z_fct
        self.X, self.Y = np.meshgrid(x, y)
        self.cmap = cmap
        self.norm_xy = norm_xy

    def plot(self, fig, graph):
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        fig.graphs[graph].graph.imshow(self.z_fct(self.X, self.Y), cmap=self.cmap, extent=(min(self.x), max(self.x), min(self.y), max(self.y)), origin='lower')


class ltPlotSurf3d:
    def __init__(self, theta, phi, x_fct=None, y_fct=None, z_fct=None, R_fct=None, alpha=0.5, color=color_default, norm_xyz=True):
        if R_fct is not None:
            def x_fct(t, p):
                return R_fct(t, p) * np.sin(t) * np.cos(p)
            def y_fct(t, p):
                return R_fct(t, p) * np.sin(t) * np.sin(p)
            def z_fct(t, p):
                return R_fct(t, p) * np.cos(t)
        self.theta = theta
        self.phi = phi
        self.Theta, self.Phi = np.meshgrid(theta, phi)
        self.x_fct = x_fct
        self.y_fct = y_fct
        self.z_fct = z_fct
        self.R_fct = R_fct
        self.alpha = alpha
        self.color = color
        self.norm_xyz=True

    def plot(self, fig, graph):
        x = self.x_fct(self.Theta, self.Phi)
        y = self.y_fct(self.Theta, self.Phi)
        z = self.z_fct(self.Theta, self.Phi)
        if self.norm_xyz :
            ax = fig.graphs[graph].graph
            ax.set_aspect('equal', adjustable='box')
            max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max()
            Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(x.max()+x.min())
            Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(y.max()+y.min())
            Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(z.max()+z.min())
            for xb, yb, zb in zip(Xb, Yb, Zb):
                ax.plot([xb], [yb], [zb], 'w')
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
        if self.norm_xy :
            fig.graphs[graph].graph.set_aspect('equal', adjustable='box')
        fig.graphs[graph].graph.quiver(self.X, self.Y, self.Z, self.vx_fct(self.X, self.Y, self.Z), self.vy_fct(self.X, self.Y, self.Z), self.vz_fct(self.X, self.Y, self.Z), length=0.1, normalize=True, linewidth=.5, label=self.label, color=self.color)

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
        self.EpH_data_dir = homedir+'/Dropbox/Enseignement/py_files/Diagrammes_E-pH/'
        self.element = element
        self.element_data_file = self.EpH_data_dir + 'data-' + element + '.py'

        self.C_tr = C_tr
        self.pH_min = pH_min
        self.pH_max = pH_max
        self.E_min = E_min
        self.E_max = E_max
        self.color = color
        self.text_color = text_color
        self.show_species = show_species

    def plot(self, fig, graph):
        #################################
        ## tmp lines for compatibility ##
        functions_to_draw = []
        lines_to_draw = []
        afficher_especes_chimiques = self.show_species
        text_diag_color = self.text_color
        #################################
        pH_min = self.pH_min
        pH_max = self.pH_max
        E_min = self.E_min
        E_max = self.E_max
        C = self.C_tr
        pC = -np.log10(C)
        diag_color = self.color
        ax = fig.graphs[graph].graph
        execfile(self.element_data_file)
        #################################
        ## tmp lines for compatibility ##
        seps_from_data = lines_to_draw
        seps_from_data += functions_to_draw
        #################################

        seps = []
        for sep in seps_from_data:
            seps.append(ltPlotFct(sep[1], sep[2], label=None, color=self.color))
        seps[0].label = '{element}, $C_{{ {ind} }} = \\SI{{ {C} }}{{ {units} }}$'.format(element=self.element, ind='\\mathrm{{tr}}', C=C, units='mol.L^{-1}')
        for sep in seps:
            sep.plot(fig, graph)
