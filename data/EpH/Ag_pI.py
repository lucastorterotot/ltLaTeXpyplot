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

# if afficher_especes_chimiques is not False:
#     ax.text(.5*pI_sep + .5*pI_max, .5*Esepza + .5*E_max, 'Ag$^+$', color = text_diag_color)
#     ax.text(.5*pI_sep + .5*pI_max, .5*Esepza + .5*Esep_pI_min, 'Ag', color = text_diag_color)
#     ax.text(.5*pI_sep + .5*pI_min, Esepza, 'AgI', color = text_diag_color)

seps = [sep1, sep2, sep3]
spes = []

