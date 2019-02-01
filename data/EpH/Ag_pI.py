from ltLaTeXpyplot.data.EpH.EpHgeneric import *

Eza = 0.8
pKs_AgI = 16.1

def pI_sep(pC):
    return pKs_AgI - pC

def Esepza(pC, pH):
    return Eza - RT_on_F * pC

def Esep_pI_min(pC, pH):
    return Esepza(pC, pH) + RT_on_F * pH - pI_sep(pC)

sep1 = EpHsep('min', pI_sep, Esep_pI_min, Esepza)
sep2 = EpHsep(pI_sep, 'max', Esepza, Esepza)
sep3 = EpHsep(pI_sep, pI_sep, Esepza, 'max')

spe1 = EpHspe('Ag$^+$', pI_sep, 'max', Esepza, 'max')
spe2 = EpHspe('Ag', pI_sep, 'max', Esepza, Esep_pI_min)
spe3 = EpHspe('AgI', pI_sep, 'min', 'min', Esepza, E_r = .75)

seps = [sep1, sep2, sep3]
spes = [spe1, spe2, spe3]

