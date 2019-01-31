from EpHgeneric import *

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

# if afficher_especes_chimiques is not False:
#     ax.text(0.9*pH_min+0.1*pHsep, 0.25*sep2E[0]+0.75*sep2E[1], 'I$_{2}$', color = text_diag_color)
#     ax.text(0.5*pH_min+0.5*pH_max, 0.5*Esepaz+0.5*E_max, 'IO$_3^-$', color = text_diag_color)
#     ax.text(0.25*pH_min+0.75*pHsep, 0.8*Esepaz+0.2*E_min, 'I$^-$', color = text_diag_color)

seps = [sep1, sep2, sep3]
spes = []
