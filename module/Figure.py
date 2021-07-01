#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ltLaTeXpyplot.module.default_tex_settings import pgf_with_latex
from ltLaTeXpyplot.module.utils import inches_per_cm
from ltLaTeXpyplot.module.Graph import ltGraph

from scipy.constants import golden

import matplotlib as mpl
mpl.use('pgf')
mpl.rcParams.update(pgf_with_latex)

import matplotlib.pyplot as plt

from contextlib import suppress

class ltFigure:
    def __init__(self,
                 name = 'fig',
                 title = None,
                 page_width_cm = 17,
                 width_frac = .8,
                 height_width_ratio = 1./golden,
                 tight_layout = False,
                 lang = 'FR',
                 auto_color = True
                ):
        self.name = name
        self.title = title
        self.page_width_cm = page_width_cm
        self.width_frac = width_frac
        self.height_width_ratio = height_width_ratio

        self.fig_width_inches = page_width_cm * width_frac * inches_per_cm
        self.fig_height_inches = self.fig_width_inches * height_width_ratio

        self.figsize = [self.fig_width_inches, self.fig_height_inches]

        #plt.clf() # TODO check that there is no conflict with other figures
        self.fig = plt.figure(figsize = self.figsize)
        self.graphs = {}
        self.tight_layout = tight_layout

        self.lang = lang
        self.suppressNotImplementedError = False
        self.bbox_inches = 'tight'

        self.color_theme_candidate = True
        self.auto_color = auto_color

    def close(self):
        plt.close(self.fig)
        
    def update(self):
        pgf_preamble = pgf_with_latex['pgf.preamble']
        if self.lang == 'FR':
            pgf_with_latex['pgf.preamble'].append(
                r"\SIdecimalsign{,}\SIthousandsep{\,}"
            )
        mpl.rcParams.update(pgf_with_latex)
        
        if self.title is not None:
            self.fig.suptitle(self.title, fontsize = pgf_with_latex["font.size"]+.95)
        for graph in self.graphs.values():
            graph.update()
        if self.tight_layout :
            self.fig.tight_layout()

    def save(self, format = 'pgf'):
        self.update()
        for graph in self.graphs.values():
            if graph.projection == '3d':
                self.bbox_inches = None
        if self.suppressNotImplementedError:
            with suppress(NotImplementedError):
                self._savefig(format = format)
        else:
            self._savefig(format = format)
        if format == 'pgf' and self.color_theme_candidate and self.auto_color:
            self._make_color_theme()

    def _savefig(self, format = 'pgf'):
        self.fig.savefig(
            '{}-pyplot.{}'.format(
                self.name,
                format),
            bbox_inches = self.bbox_inches)

    def _make_color_theme(self):
        file_to_update = '{}-pyplot.pgf'.format(self.name)
        import os
        os.system("sed -i 's|{}|{}|g' {}".format(
            'definecolor{currentstroke}{rgb}{0.121569,0.466667,0.705882}',
            'colorlet{currentstroke}{ltcolor\\\ltcolortheme}',
            file_to_update
        ))
        os.system("echo 'fi' | cat - {file} > .tmp-{file}~ && mv .tmp-{file}~ {file}".format(
            file = file_to_update
        ))
        os.system("printf '{string}' | cat - {file} > .tmp-{file}~ && mv .tmp-{file}~ {file}".format(
            string = '\\ifx\\undefined\\ltcolortheme\\def\\ltcolortheme{blue}\\definecolor{ltcolorblue}{rgb}{0.121569,0.466667,0.705882}\\',
            file = file_to_update
        ))
        os.system("echo '{string}' | cat - {file} > .tmp-{file}~ && mv .tmp-{file}~ {file}".format(
            string = '%% First make sure the auto color theme will work without the ltstyle package:',
            file = file_to_update
        ))

    def addgraph(self, name, **kwargs):
        if not name in self.graphs:
            self.graphs[name] = ltGraph(self, name, **kwargs)
        else:
            raise NameError('Figure {} already has a graph named {}.'.format(self.name, name))

    def addtwingraph(self, name, twin_of, axis = 'x', **kwargs):
        self.addgraph(name, twin_of = twin_of, twin_common_axis = axis, **kwargs)

    def testgraph(self, name, position = 111):
        if not name in self.graphs:
            self.addgraph(name, position = position)
            print('Warning, auto-generated graph at position {}'.format(position))
            print('with name {}'.format(name))

    def addplot(self, plot, name):
        self.testgraph(name)
        plot.plot(self, name)

    def addinsetgraph(self,
                      name,
                      inset_of,
                      inset_pos = 'upper right',
                      indicate_inset_zoom = True,
                      x_ticks = False,
                      y_ticks = False,
                      **kwargs
                     ):
        self.addgraph(
            name,
            inset_of = inset_of,
            inset_pos = inset_pos,
            indicate_inset_zoom = indicate_inset_zoom,
            x_ticks = x_ticks,
            y_ticks = y_ticks,
            **kwargs
        )
