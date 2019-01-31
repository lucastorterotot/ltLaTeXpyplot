from EpHgeneric import *

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

# if afficher_especes_chimiques is not False:
#     ax.text(pH_min, 0.1*sep2E[0]+0.9*sep2E[1], 'Cl$_{2}$', color = text_diag_color)
#     ax.text(0.5*pH_min+0.5*pHsepb, 0.5*Esepza+0.5*E_max, 'HClO', color = text_diag_color)
#     ax.text(0.25*pH_min+0.75*pHsepb, 0.8*Esepza+0.2*E_min, 'Cl$^-$', color = text_diag_color)
#     ax.text(0.5*pH_max+0.5*pHsepb, 0.75*Esepza+0.25*E_max, 'ClO$^-$', color = text_diag_color)

seps = [sep1, sep2, sep3, sep4, sep5]
spes = []
