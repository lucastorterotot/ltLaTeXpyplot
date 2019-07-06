#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ltLaTeXpyplot.module.core import num_format
import numpy as np

class Test_num_format(unittest.TestCase):
    exponents = np.linspace(-20,20,41)
    signifs = np.linspace(0.1,1,30)
    values = {}
    for exponent in exponents:
        for signif in signifs:
            value = float(
                'e'.join(
                    [str(signif), str(int(exponent))]
                )
            )
            values[value] = num_format(value, None)

    def test_format(self):
        '''test the output has the form \\num{ XXX }'''
        for outp in self.values.values():
            self.assertTrue('\\num{' == outp[:outp.rindex('{')+1])
            self.assertTrue('}' == outp[outp.index('}'):])

    def test_values(self):
        '''test the output value is less than 2% away from original value'''
        for inp, outp in self.values.items():
            outp = float(
                outp[outp.rindex('{')+1:outp.index('}')])

            self.assertTrue(abs(inp-outp)/inp < 2/100)
