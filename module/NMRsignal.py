#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ltNMRsignal:
    def __init__(
        self,
        delta,
        nbH = 1,
        mults = [],
        J_Hz = []
    ):
        self.delta = delta
        self.nbH = nbH
        self.mults = mults
        self.J_Hz = J_Hz

    def inverse(self):
        return ltNMRsignal(self.delta, -self.nbH, self.mults, self.J_Hz)
