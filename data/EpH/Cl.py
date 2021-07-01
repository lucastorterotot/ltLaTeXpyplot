from ltLaTeXpyplot.module.EpHgeneric import *

import numpy as np

Eza = 1.4
Eab = 1.59
pKa_HClO_ClO = 7.5

def Esepza(pC, pH):
    return Eza

def pHsepa(pC):
    c_tr = 10**(-pC)
    return (Eab + RT_on_F/2 * np.log10((c_tr*2./3)**2/    (c_tr*1./3)) - Eza)/RT_on_F

def pHsepb(pC):
    return pKa_HClO_ClO

def E1(pC, pH):
    return (Eza+Eab)*.5 - RT_on_F/2*pHsepb(pC)

def E2(pC, pH):
    return (Eza+Eab)*.5 - RT_on_F/2 * pKa_HClO_ClO - RT_on_F*(pH-pHsepb(pC))

def E3(pC, pH):
    c_tr = 10**(-pC)
    return Eab + RT_on_F/2 * np.log10((c_tr*2./3)**2/(c_tr*1./3)) - RT_on_F*pH

sep1 = EpHsep('min', pHsepa, Esepza, Esepza)
sep2 = EpHsep(pHsepa, pHsepb, Esepza, E1)
sep3 = EpHsep(pHsepb, 'max', E1, E2)
sep4 = EpHsep('min', pHsepa, E3, Esepza)
sep5 = EpHsep(pHsepb, pHsepb, E1, 'max')

spe1 = EpHspe('Cl$_2$', 'min', pHsepa, E3, Esepza, E_r=.7, pH_r=.25)
spe2 = EpHspe('HClO', 'min', pHsepb, 'max', Esepza)
spe3 = EpHspe('Cl$^-$', 'min', 'max', Esepza, E2)
spe4 = EpHspe('ClO$^-$', 'max', pHsepb, 'max', E2)

seps = [sep1, sep2, sep3, sep4, sep5]
spes = [spe1, spe2, spe3, spe4]
