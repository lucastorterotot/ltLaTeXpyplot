#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

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
        if sep.pHa == 'min':
            pHa = self.pH_min
        elif sep.pHa == 'max':
            pHa = self.pH_max
        else:
            pHa = sep.pHa(self.pC)
        if sep.pHb == 'min':
            pHb = self.pH_min
        elif sep.pHb == 'max':
            pHb = self.pH_max
        else:
            pHb = sep.pHb(self.pC)
        if sep.Ea == 'min':
            Ea = self.E_min
        elif sep.Ea == 'max':
            Ea = self.E_max
        else:
            Ea = sep.Ea(self.pC, pHa)
        if sep.Eb == 'min':
            Eb = self.E_min
        elif sep.Eb == 'max':
            Eb = self.E_max
        else:
            Eb = sep.Eb(self.pC, pHb)
        self.seps.append([[pHa, pHb],[Ea, Eb]])

    def addspe(self, spe):
        pH = spe.pH(self.pC)
        E = spe.E(self.pC)
        self.spes.append([pH, E, spe.chf])
    

class EpHsep:
    def __init__(self, pHa, pHb, Ea, Eb):
        self.pHa = pHa
        self.pHb = pHb
        self.Ea = Ea
        self.Eb = Eb

        
class EpHspecies:
    def __init__(self, chf, pH, E):
        self.chf = chf
        self.pH = pH
        self.E = E
        
