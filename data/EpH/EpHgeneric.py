#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from scipy.constants import elementary_charge, Boltzmann
T_value_C = 25
T_value = T_value_C + 273.15
RT_on_F = (Boltzmann*T_value/elementary_charge * np.log(10))

class EpHgeneric:
    def __init__(self, pH_min=0, pH_max=14, E_min=-1, E_max=1, conc=1e-3, pC=None):
        self.pH_min = pH_min
        self.pH_max = pH_max
        self.E_min = E_min
        self.E_max = E_max
        if conc is not None and pC is None:
            self.conc = conc
            self.pC = -np.log10(conc)
        elif conc is None and pC is not None:
            self.pC = pC
            self.conc = 10**(-1.*pC)
        else:
            raise ValueError('Please set a correct concentration input.')
        self.seps = []
        self.spes = []

    def addsep(self, sep):
        pHa, pHb, Ea, Eb = self.get_position(sep, sep.pHa, sep.pHb, sep.Ea, sep.Eb)
        self.seps.append([[pHa, pHb],[Ea, Eb]])

    def addspe(self, spe):
        pHa, pHb, Ea, Eb = self.get_position(spe, spe.pHa, spe.pHb, spe.Ea, spe.Eb)
        pH = pHa * (1-spe.pH_r) + pHb * spe.pH_r
        E = Ea * (1-spe.E_r) + Eb * spe.E_r
        self.spes.append([pH, E, spe.chf])

    def get_position(self, obj, pHa, pHb, Ea, Eb):
        if obj.pHa == 'min':
            pHa = self.pH_min
        elif obj.pHa == 'max':
            pHa = self.pH_max
        else:
            pHa = obj.pHa(self.pC)
        if obj.pHb == 'min':
            pHb = self.pH_min
        elif obj.pHb == 'max':
            pHb = self.pH_max
        else:
            pHb = obj.pHb(self.pC)
        if obj.Ea == 'min':
            Ea = self.E_min
        elif obj.Ea == 'max':
            Ea = self.E_max
        else:
            Ea = obj.Ea(self.pC, pHa)
        if obj.Eb == 'min':
            Eb = self.E_min
        elif obj.Eb == 'max':
            Eb = self.E_max
        else:
            Eb = obj.Eb(self.pC, pHb)
        return pHa, pHb, Ea, Eb

class EpHsep:
    def __init__(self, pHa, pHb, Ea, Eb):
        self.pHa = pHa
        self.pHb = pHb
        self.Ea = Ea
        self.Eb = Eb

        
class EpHspecies:
    def __init__(self, chf, pHa, pHb, Ea, Eb, pH_r=.5, E_r=.5):
        self.chf = chf
        self.pHa = pHa
        self.pHb = pHb
        self.Ea = Ea
        self.Eb = Eb
        self.pH_r = pH_r
        self.E_r = E_r
        
