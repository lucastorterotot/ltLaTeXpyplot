#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import ltLaTeXpyplot as lt
import numpy as np

class Test_EpH_calcs(unittest.TestCase):
    tests_elements_sizes = {
        'Ag_pI' : (5, 16, -0.1, 0.93168),
        'Cl' : (2, 8, -.1, 1.4),
        'Cu' : (2, 6, -.1, 0.64664),
        'Fe' : (2, 7, -0.49916, 0.97),
        'H' : (5, 6, -0.35496, 0.1),
        'I' : (5, 8, -.1, 0.82143),
        'O' : (5, 6, -.1, 0.9342),
    }
    
    def create(self, element, C_tr):
        fig = lt.ltFigure(name='test')
        fig.addgraph(
            'graph1',
            x_label='pH',
            y_label='$E$ ($\\SI{}{V}$)'
        )
        EpHplt = lt.ltPlotEpH(element, C_tr, pH_min = 5, pH_max = 6)
        fig.addplot(EpHplt, 'graph1')
        return EpHplt, fig.graphs['graph1']


    def test_elements_size(self):
        ''' Mostly desinged to spot changes in graphs'''
        for element, values in self.tests_elements_sizes.items():
            pH_min, pH_max, E_min, E_max = values
            EpHplt, graph = self.create(element, 1e-2)
            self.assertEqual(np.round(EpHplt.pH_min), pH_min)
            self.assertEqual(np.round(EpHplt.pH_max), pH_max)
            self.assertEqual(np.round(EpHplt.E_min, 5), E_min)
            self.assertEqual(np.round(EpHplt.E_max, 5), E_max)

    def test_compute_with(self):
        element1 = 'Fe'
        element2 = 'Cu'
        EpH1 = lt.ltPlotEpH(element1, 1e-2, pH_min = 5, pH_max = 6)
        EpH2 = lt.ltPlotEpH(element2, 1e-2, pH_min = 5, pH_max = 6)
        EpH1.compute_with([EpH2])
        pH_min1, pH_max1, E_min1, E_max1 = self.tests_elements_sizes[element1]
        pH_min2, pH_max2, E_min2, E_max2 = self.tests_elements_sizes[element2]
        pH_min = min([pH_min1, pH_min2])
        pH_max = max([pH_max1, pH_max2])
        E_min = min([E_min1, E_min2])
        E_max = max([E_max1, E_max2])
        for EpHplt in [EpH1, EpH2]:
            self.assertEqual(np.round(EpHplt.pH_min), pH_min)
            self.assertEqual(np.round(EpHplt.pH_max), pH_max)
            self.assertEqual(np.round(EpHplt.E_min, 5), E_min)
            self.assertEqual(np.round(EpHplt.E_max, 5), E_max)
