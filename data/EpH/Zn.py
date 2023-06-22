from ltLaTeXpyplot.module.EpHgeneric import *

import numpy as np

Eza = -0.76
pKs_Zn_2OH = 16.7
pKb_Zn_4OH = 15.3

def Esepza(pC, pH):
    return (Eza - RT_on_F/2 * pC)

def pHsepa(pC):
    return pC/2 + 14 - pKs_Zn_2OH/2

def pHsepb(pC):
    return 14+(pKs_Zn_2OH-pKb_Zn_4OH-pC)/2

def E1(pC, pH):
    return Eza + RT_on_F*(14-pKs_Zn_2OH/2-pH)

def E2(pC, pH):
    return Eza + RT_on_F/2*(-pKb_Zn_4OH+4*14-4*pH-pC)

sep1 = EpHsep('min', pHsepa, Esepza, Esepza)
sep2 = EpHsep(pHsepa, pHsepb, Esepza, E1)
sep3 = EpHsep(pHsepb, 'max', E1, E2)
sep4 = EpHsep(pHsepa, pHsepa, E1, 'max')
sep5 = EpHsep(pHsepb, pHsepb, E1, 'max')

spe1 = EpHspe('Zn$^{2+}$', 'min', pHsepa, 'max', Esepza)
spe2 = EpHspe('Zn(OH)$_2$', pHsepa, pHsepb, 'max', Esepza)
spe3 = EpHspe('Zn', 'min', 'max', Esepza, E2, pH_r = .4)
spe4 = EpHspe('Zn(OH)$_4$$^{2-}$', 'max', pHsepb, 'max', E2)

seps = [sep1, sep2, sep3, sep4, sep5]
spes = [spe1, spe2, spe3, spe4]
