from ltLaTeXpyplot.module.EpHgeneric import *

Eaz = 0.54
Ezb = 1.19

def Esepaz(pC, pH):
    return Eaz + RT_on_F*pC

def pHsep(pC):
    return (Ezb - Eaz - RT_on_F*pC*(1+1/5))/RT_on_F*10/12

def Esepzb(pC, pH):
    return Ezb - RT_on_F/5*pC - RT_on_F*12/10*pH

def Esepab(pC, pH):
    return Esepzb(pC, pHsep(pC)) - RT_on_F*(pH - pHsep(pC))

sep1 = EpHsep('min', pHsep, Esepaz, Esepaz)
sep2 = EpHsep(pHsep, 'max', Esepab, Esepab)
sep3 = EpHsep('min', pHsep, Esepzb, Esepzb)

spe1 = EpHspe('I$_2$', 'min', pHsep, Esepzb, Esepaz, pH_r=.25, E_r=.6)
spe2 = EpHspe('IO$_3^-$', 'min', 'max', 'max', Esepzb, pH_r=.75, E_r=.25)
spe3 = EpHspe('I$^-$', 'min', 'max', Esepaz, Esepab)

seps = [sep1, sep2, sep3]
spes = [spe1, spe2, spe3]
