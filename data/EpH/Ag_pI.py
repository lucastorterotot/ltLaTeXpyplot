from ltLaTeXpyplot.module.EpHgeneric import *

Eza = 0.8
pKs_AgI = 16.1

def pI_sep(pC):
    return pKs_AgI - pC
def pI_sep_plus(pC):
    return pI_sep(pC)+2

def Esepza(pC, pH):
    return Eza - RT_on_F * pC
def Esepza_plus(pC, pH):
    return Esepza(pC, pH) + .25

def Esep_pI_min(pC, pH):
    return Esepza(pC, pH) + RT_on_F * (pH - pI_sep(pC))

sep1 = EpHsep('min', pI_sep, Esep_pI_min, Esepza)
sep2a = EpHsep(pI_sep, pI_sep_plus, Esepza, Esepza)
sep2b = EpHsep(pI_sep_plus, 'max', Esepza, Esepza)
sep3a = EpHsep(pI_sep, pI_sep, Esepza, Esepza_plus)
sep3b = EpHsep(pI_sep, pI_sep, Esepza_plus, 'max')

spe1 = EpHspe('Ag$^+$', pI_sep, 'max', Esepza, 'max')
spe2 = EpHspe('Ag', 'min', 'max', Esep_pI_min, Esepza, pH_r = .75)
spe3 = EpHspe('AgI', pI_sep, 'min', 'min', Esepza, E_r = .75)

seps = [sep1, sep2a, sep2b, sep3a, sep3b]
spes = [spe1, spe2, spe3]

