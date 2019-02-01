from ltLaTeXpyplot.data.EpH.EpHgeneric import *

Eaz = 0.54
Ezb = 1.19

def Esepaz(pC, pH):
    c_tr = 10**(-pC)
    return Eaz + RT_on_F/2* np.log10(2./c_tr)

def pHsep(pC):
    c_tr = 10**(-pC)
    return 10./(RT_on_F*12)*(Ezb - Esepaz(pC,0) +RT_on_F/10*np.log10(c_tr/2.))

def Esepzb1(pC, pH):
    c_tr = 10**(-pC)
    return Ezb + RT_on_F/10*np.log10(c_tr/2.) - RT_on_F*12./10.*pH

def Esepzb2(pC, pH):
    return Esepaz(pC, pH)

def Esepab2(pC, pH):
    return Esepzb2(pC, pH) - RT_on_F*(pH - pHsep(pC))

sep1 = EpHsep('min', pHsep, Esepaz, Esepaz)
sep2 = EpHsep(pHsep, 'max', Esepaz, Esepab2)
sep3 = EpHsep('min', pHsep, Esepzb1, Esepzb2)

spe1 = EpHspe('I$_2$', 'min', pHsep, Esepzb1, Esepaz, pH_r=.25, E_r=.6)
spe2 = EpHspe('IO$_3^-$', 'min', 'max', 'max', Esepzb1)
spe3 = EpHspe('I$^-$', 'min', 'max', Esepaz, Esepab2)

seps = [sep1, sep2, sep3]
spes = [spe1, spe2, spe3]
