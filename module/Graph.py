#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ltLaTeXpyplot.module.default_tex_settings import pgf_with_latex
from ltLaTeXpyplot.module.utils import num_formatter
import ltLaTeXpyplot.module.default_mpl_settings as defaults

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D

class ltGraph:
    def __init__(self, fig, name, title = None,
                 twin_of = None, twin_common_axis = 'x', 
                 inset_of = None, inset_pos = None, indicate_inset_zoom = True,
                 x_label = None, y_label = None, z_label = None,
                 x_scaling = 'linear', y_scaling = 'linear', z_scaling = 'linear', projection = 'rectilinear',
                 x_min = None, x_max = None, y_min = None, y_max = None, z_min = None, z_max = None,
                 x_ticks = True, x_ticks_min = None, x_ticks_max = None, x_ticks_step = None,
                 y_ticks = True, y_ticks_min = None, y_ticks_max = None, y_ticks_step = None,
                 z_ticks = True, z_ticks_min = None, z_ticks_max = None, z_ticks_step = None,
                 xticklabels = None, yticklabels = None,
                 xtickpos = None, ytickpos = None,
                 minorticks = True,
                 num_x_major = True, num_x_minor = False,
                 num_y_major = True, num_y_minor = False,
                 num_z_major = True, num_z_minor = False,
                 show_grid = False, show_x_axis = False, show_y_axis = False,
                 show_grid_minor_x = False, show_grid_minor_y = False,
                 show_legend = False, legend_location = 'best', legend_on_side = False,
                 show_cmap_legend = False, cmap_label = None,
                 position = [1,1,1],
                 share_x = None, share_y = None):
        self.fig = fig
        self.name = name
        self.twin_of = twin_of
        self.twin_common_axis = twin_common_axis
        self.inset_of = inset_of
        self.inset_pos = inset_pos
        self.indicate_inset_zoom = indicate_inset_zoom
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
        self.xticklabels = xticklabels
        self.yticklabels = yticklabels
        self.xtickpos = xtickpos
        self.ytickpos = ytickpos
        self.minorticks = minorticks
        self.num_x_major = num_x_major
        self.num_y_major = num_y_major
        self.num_z_major = num_z_major
        self.num_x_minor = num_x_minor
        self.num_y_minor = num_y_minor
        self.num_z_minor = num_z_minor
        self.show_grid = show_grid
        self.show_grid_minor_x = show_grid_minor_x
        self.show_grid_minor_y = show_grid_minor_y
        self.show_x_axis = show_x_axis
        self.show_y_axis = show_y_axis
        self.show_legend = show_legend
        self.legend_location = legend_location
        self.legend_on_side = legend_on_side
        self.position = position
        if isinstance(position, int) and len(str(position)) == 3:
            self.position = [int(value) for value in str(position)]
        self.show_cmap_legend = show_cmap_legend
        self.cmap_label = cmap_label
        if isinstance(share_x , str):
            self.share_x = fig.graphs[share_x].graph
        else:
            self.share_x = share_x
        if isinstance(share_y , str):
            self.share_y = fig.graphs[share_y].graph
        else:
            self.share_y = share_y

        if self.twin_of is None and self.inset_of is None:
            self.graph = fig.fig.add_subplot(self.position[0],
                                             self.position[1],
                                             self.position[2],
                                             projection = self.projection,
                                             sharex = self.share_x,
                                             sharey = self.share_y
                                            )
        elif self.twin_of in self.fig.graphs:
            if self.twin_common_axis == 'x':
                self.graph = fig.graphs[self.twin_of].graph.twinx()
            elif self.twin_common_axis == 'y':
                self.graph = fig.graphs[self.twin_of].graph.twiny()
        elif self.inset_of in self.fig.graphs:
            ax = fig.graphs[self.inset_of].graph
            if self.inset_pos == 'upper right':
                self.inset_pos = [0.5, 0.5, 0.47, 0.47]
                inset_loc = 1
            elif self.inset_pos == 'upper left':
                self.inset_pos = [0.03, 0.5, 0.47, 0.47]
                inset_loc = 2
            elif self.inset_pos == 'lower left':
                self.inset_pos = [0.03, 0.03, 0.47, 0.47]
                inset_loc = 3
            elif self.inset_pos == 'lower right':
                self.inset_pos = [0.5, 0.03, 0.47, 0.47]
                inset_loc = 4
            elif self.inset_pos == 'right':
                self.inset_pos = [0.5, 0.235, 0.47, 0.47]
                inset_loc = 5
            elif self.inset_pos == 'center left':
                self.inset_pos = [0.03, 0.235, 0.47, 0.47]
                inset_loc = 6
            elif self.inset_pos == 'center right':
                self.inset_pos = [0.5, 0.235, 0.47, 0.47]
                inset_loc = 7
            elif self.inset_pos == 'lower center':
                self.inset_pos = [0.235, 0.03, 0.47, 0.47]
                inset_loc = 8
            elif self.inset_pos == 'upper center':
                self.inset_pos = [0.235, 0.5, 0.47, 0.47]
                inset_loc = 9
            elif self.inset_pos == 'center':
                self.inset_pos = [0.235, 0.235, 0.47, 0.47]
                inset_loc = 10
            else :
                inset_center_x = self.inset_pos[0] + self.inset_pos[2]/2
                inset_center_y = self.inset_pos[1] + self.inset_pos[3]/2
                if inset_center_x < 1/3 and inset_center_y < 1/3:
                    inset_loc = 3
                elif inset_center_x < 1/3 and inset_center_y < 2/3:
                    inset_loc = 6
                elif inset_center_x < 1/3 and inset_center_y >= 2/3:
                    inset_loc = 2
                elif inset_center_x < 2/3 and inset_center_y < 1/3:
                    inset_loc = 8
                elif inset_center_x < 2/3 and inset_center_y < 2/3:
                    inset_loc = 10
                elif inset_center_x < 2/3 and inset_center_y >= 2/3:
                    inset_loc = 9
                elif inset_center_x >= 2/3 and inset_center_y < 1/3:
                    inset_loc = 4
                elif inset_center_x >= 2/3 and inset_center_y < 2/3:
                    inset_loc = 7
                else:
                    inset_loc = 1
            self._inset_loc = inset_loc
            if hasattr(ax, 'inset_axes'):
                self.graph = ax.inset_axes(self.inset_pos)
            else :
                from mpl_toolkits.axes_grid1.inset_locator import inset_axes
                width = self.inset_pos[2]*100
                height = self.inset_pos[3]*100
                self.graph = inset_axes(ax,
                   width = "{}%".format(width),
                   height = "{}%".format(height),  # height : 1 inch
                   loc = inset_loc)
        else:
            raise_type = 'new'
            if self.twin_of is not None :
                raise_type = 'twin'
                link = self.twin_of
            elif self.inset_of is not None :
                raise_type = 'inset'
                link = self.inset_of
            error_strings = [
                '',
                '  You tried to make a {} graph but it failed. Aborting...'.format(raise_type),
                '    Graph name: {}'.format(self.name)
            ]
            if not raise_type == 'new':
                error_strings += [
                    '    Supposed {} of: {}'.format(raise_type, link),
                    '    Can be {} of: '.format(raise_type)
                ]
                error_strings += ['\t{}'.format(key) for key in self.fig.graphs]
            error_string = '\n'.join(error_strings)
            raise RuntimeError(error_string)
        
        if show_grid:
            self.graph.grid(linewidth = defaults.linewidths['grid'])
            if show_grid_minor_x:
                self.graph.grid(axis = "x", which = "minor", linewidth = defaults.linewidths['grid']/2)
            if show_grid_minor_y:
                self.graph.grid(axis = "y", which = "minor", linewidth = defaults.linewidths['grid']/2)
        if show_x_axis and not (projection == '3d' or x_min is None or x_max is None):
            self.graph.plot([x_min,x_max],
                            [0,0],
                            color = 'black',
                            linewidth = defaults.linewidths['gridaxis']
                           )
        if show_y_axis and not (projection == '3d' or y_min is None or y_max is None):
            self.graph.plot([0,0],
                            [y_min,y_max],
                            color = 'black',
                            linewidth = defaults.linewidths['gridaxis']
                           )

        if not x_ticks:
            plt.setp(self.graph.get_xticklabels(), visible = False)
        if not y_ticks:
            plt.setp(self.graph.get_yticklabels(), visible = False)
        if not z_ticks:
            plt.setp(self.graph.get_zticklabels(), visible = False)

        for ticks_category in ['major', 'minor']:
            if self.projection == 'polar':
                self.graph.tick_params(direction = 'in',
                                       which = ticks_category,
                                       width = defaults.linewidths[ticks_category+'ticks']
                                      )
            else:
                self.graph.tick_params(
                    direction = 'in',
                    which = ticks_category,
                    bottom = (self.twin_of is None or self.twin_common_axis != 'y'),
                    top = 1,
                    left = (self.twin_of is None or self.twin_common_axis != 'x'),
                    right = 1,
                    width = defaults.linewidths[ticks_category+'ticks']
                )

    def set_xticklabels(self):
        if self.xticklabels is not None:
            self.graph.set_xticks(self.xtickpos)
            self.graph.xaxis.set_ticklabels(self.xticklabels)

    def set_yticklabels(self):
        if self.yticklabels is not None:
            self.graph.set_yticks(self.ytickpos)
            self.graph.yaxis.set_ticklabels(self.yticklabels)

    def update(self):
        if self.title is not None:
            self.graph.set_title(self.title, fontsize = pgf_with_latex["font.size"])
        self.graph.set_xscale(self.x_scaling)
        self.graph.set_yscale(self.y_scaling)
        if self.projection == '3d':
            self.graph.set_zscale(self.z_scaling)

        if self.x_label is not None :
            self.graph.set_xlabel(self.x_label)
        if self.y_label is not None and self.projection != 'polar':
            self.graph.set_ylabel(self.y_label)
        if self.z_label is not None and self.projection == '3d':
            self.graph.set_zlabel(self.z_label)

        if self.show_legend :
            plots, labels = self.graph.get_legend_handles_labels()
            for Nlabels in range(len(labels)):
                Nlabels = len(labels) - Nlabels -1
                if labels[Nlabels] == 'indicate_inset':
                    plots[Nlabels].set_label(None)
            if self.legend_on_side:
                self.graph.legend(bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0.)
            else :
                self.graph.legend(loc = self.legend_location)

        if self.x_min is not None and self.x_max is not None :
            self.graph.set_xlim([self.x_min,self.x_max])
        if self.y_min is not None and self.y_max is not None :
            self.graph.set_ylim([self.y_min,self.y_max])
        if self.z_min is not None and self.z_max is not None and self.projection == '3d':
            self.graph.set_zlim([self.z_min,self.z_max])

        if self.x_ticks_step is not None :
            if self.x_ticks_min is None:
                self.x_ticks_min = self.x_min
            if self.x_ticks_max is None:
                self.x_ticks_max = self.x_max
            if self.x_ticks_min is not None and self.x_ticks_max is not None :
                self.graph.xaxis.set_ticks(
                    np.arange(self.x_ticks_min,self.x_ticks_max+self.x_ticks_step/10.,self.x_ticks_step)
                )
        if self.y_ticks_step is not None :
            if self.y_ticks_min is None:
                self.y_ticks_min = self.y_min
            if self.y_ticks_max is None:
                self.y_ticks_max = self.y_max
            if self.y_ticks_min is not None and self.y_ticks_max is not None :
                self.graph.yaxis.set_ticks(
                    np.arange(self.y_ticks_min,self.y_ticks_max+self.y_ticks_step/10.,self.y_ticks_step)
                )
        if self.z_ticks_step is not None and self.projection == '3d' :
            if self.z_ticks_min is None:
                self.z_ticks_min = self.z_min
            if self.z_ticks_max is None:
                self.z_ticks_max = self.z_max
            if self.z_ticks_min is not None and self.z_ticks_max is not None :
                self.graph.zaxis.set_ticks(
                    np.arange(self.z_ticks_min,self.z_ticks_max+self.z_ticks_step/10.,self.z_ticks_step)
                )

        if self.minorticks and not self.projection == '3d':
            self.graph.minorticks_on()
        if self.num_y_major :
            self.graph.yaxis.set_major_formatter(num_formatter)
        if self.num_y_minor :
            self.graph.yaxis.set_minor_formatter(num_formatter)
        if self.num_x_major :
            self.graph.xaxis.set_major_formatter(num_formatter)
        if self.num_x_minor :
            self.graph.xaxis.set_minor_formatter(num_formatter)
        if hasattr(self.graph, 'zaxis'):
            if self.num_z_major :
                self.graph.zaxis.set_major_formatter(num_formatter)
            if self.num_z_minor :
                self.graph.zaxis.set_minor_formatter(num_formatter)

        if self.inset_of is not None and self.indicate_inset_zoom :
            ax = self.fig.graphs[self.inset_of].graph
            if hasattr(ax, 'indicate_inset_zoom'):
                ax.indicate_inset_zoom(self.graph)
            else:
                # inspired from https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/axes/_axes.py
                xlim = self.graph.get_xlim()
                ylim = self.graph.get_ylim()
                bounds = [xlim[0], ylim[0], xlim[1] - xlim[0], ylim[1] - ylim[0]]
                transform = None
                facecolor = 'none'
                edgecolor = '0.5'
                alpha = 0.5
                zorder = 4.99
                ax.apply_aspect()

                if transform is None:
                    transform = ax.transData

                xy = (bounds[0], bounds[1])
                import matplotlib.patches as mpatches
                rectpatch = mpatches.Rectangle(
                    xy, bounds[2], bounds[3],
                    facecolor = facecolor, edgecolor = edgecolor, alpha = alpha,
                    zorder = zorder,  label = None, transform = transform)
                ax.add_patch(rectpatch)

                if self.graph is not None:
                    # want to connect the indicator to the rect....
                    connects = []
                    xr = [bounds[0], bounds[0]+bounds[2]]
                    yr = [bounds[1], bounds[1]+bounds[3]]
                    for xc in range(2):
                        for yc in range(2):
                            xyA = (xc, yc)
                            xyB = (xr[xc], yr[yc])
                            connects += [
                                mpatches.ConnectionPatch(
                                    xyA, xyB,
                                    'axes fraction', 'data',
                                    axesA = self.graph, axesB = ax, arrowstyle = "-",
                                    zorder = zorder, edgecolor = edgecolor, alpha = alpha)]
                            ax.add_patch(connects[-1])
                    # decide which two of the lines to keep visible....
                    xlim = ax.get_xlim()
                    ylim = ax.get_ylim()
                    Dx = xlim[1] - xlim[0]
                    Dy = ylim[1] - ylim[0]
                    dx = self.inset_pos[2]
                    dy = self.inset_pos[3]
                    centers = {
                        '1' : (.97-dx/2, .97-dy/2),
                        '2' : (.03+dx/2, .97-dy/2),
                        '3' : (.03+dx/2, .03+dy/2),
                        '4' : (.97-dx/2, .03+dy/2),
                        '5' : (.97-dx/2, .5),
                        '6' : (.03+dx/2, .5),
                        '7' : (.97-dx/2, .5),
                        '8' : (.5, .03+dy/2),
                        '9' : (.5, .97-dy/2),
                        '10': (.5, .5),
                        }
                    x0 = (centers[str(self._inset_loc)][0] - dx/2) * Dx + xlim[0]
                    x1 = (centers[str(self._inset_loc)][0] + dx/2) * Dx + xlim[0]
                    y0 = (centers[str(self._inset_loc)][1] - dy/2) * Dy + ylim[0]
                    y1 = (centers[str(self._inset_loc)][1] + dy/2) * Dy + ylim[0]
                    import matplotlib.transforms as mtransforms
                    pos = mtransforms.Bbox(np.array([[x0, y0], [x1, y1]]))
                    bboxins = pos#.transformed(ax.figure.transFigure)
                    rectbbox = mtransforms.Bbox.from_bounds(
                        *bounds)#.transformed(transform)
                    x0 = rectbbox.x0 < bboxins.x0
                    x1 = rectbbox.x1 < bboxins.x1
                    y0 = rectbbox.y0 < bboxins.y0
                    y1 = rectbbox.y1 < bboxins.y1
                    connects[0].set_visible(x0 ^ y0)
                    connects[1].set_visible(x0 == y1)
                    connects[2].set_visible(x1 == y0)
                    connects[3].set_visible(x1 ^ y1)
        self.set_xticklabels()
        self.set_yticklabels()

    def fill_between(self, x, y1, y2, alpha = .5, **kwargs):
        self.graph.fill_between(x, y1, y2, alpha = alpha, **kwargs)

    def addarrow(self, x, y, vx, vy, arrowstyle = '->', lw = 1, mutation_scale = 7, mutation_aspect = None):
        self.graph.add_patch(FancyArrowPatch(posA = (x, y), posB = (x+vx, y+vy),
                                             arrowstyle = arrowstyle, lw = lw, 
                                             mutation_scale = mutation_scale, mutation_aspect = mutation_aspect))

    def test_graph_3d(self):
        if not self.projection == '3d' :
            raise RuntimeError('\n'.join([
                '',
                '  You tried to draw a 3d object on a non-3d graph. Aborting...',
                '    Graph name: {}'.format(self.name),
                '    Graph projection: {}'.format(self.projection),
            ])
            )
