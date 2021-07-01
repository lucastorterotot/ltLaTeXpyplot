#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.constants import golden

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
    "figure.figsize": figsize(0.9,1./golden),     # default fig size of 0.9 textwidth
    "pgf.preamble": [                       # plots will be generated using this preamble
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts because your computer can handle it :)
        r"\usepackage[T1]{fontenc}",   
        r"\usepackage{sistyle}",
        r"\SIproductsign{\!\times\!}\SIunitsep{\,}\SIunitdot{{\fontfamily{cmr}\cdot}}",
        ]
    }
