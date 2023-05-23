from ltLaTeXpyplot.module.EpHgeneric import *

Eaz = 1.39
Ezb = 1.63
pKa_HClO_ClO = 7.5

def Esepaz(pC, pH):
    return Eaz + RT_on_F*pC

def pHsepa(pC):
    return (Ezb - Eaz - RT_on_F*pC*2)/RT_on_F

def Esepzb(pC, pH):
    return Ezb - RT_on_F*pC - RT_on_F*pH

def pHsepb(pC):
    return pKa_HClO_ClO

def Esepab(pC, pH):
    if pH > pHsepb(pC):
        return Esepab(pC, pHsepb(pC)) - RT_on_F*(pH - pHsepb(pC))
    else:
        return Esepzb(pC, pHsepa(pC)) - RT_on_F/2*(pH - pHsepa(pC))

sep1 = EpHsep('min', pHsepa, Esepaz, Esepaz)
sep2 = EpHsep('min', pHsepa, Esepzb, Esepzb)
sep3 = EpHsep(pHsepa, pHsepb, Esepab, Esepab)
sep4 = EpHsep(pHsepb, 'max', Esepab, Esepab)
sep5 = EpHsep(pHsepb, pHsepb, Esepab, 'max')

spe1 = EpHspe('Cl$_2$', 'min', pHsepa, Esepzb, Esepaz, E_r=.7, pH_r=.25)
spe2 = EpHspe('HClO', 'min', pHsepb, 'max', Esepaz)
spe3 = EpHspe('Cl$^-$', 'min', 'max', Esepaz, Esepzb)
spe4 = EpHspe('ClO$^-$', 'max', pHsepb, 'max', Esepab)

seps = [sep1, sep2, sep3, sep4, sep5]
spes = [spe1, spe2, spe3, spe4]
