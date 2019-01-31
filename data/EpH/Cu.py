from ltLaTeXpyplot.data.EpH.EpHgeneric import *

Eza = 0.52
Eab = 0.16
pKs_Cu_2OH = 18
pKs_Cu_Cu2O = 14

def pHsepa(pC):
    return 14-(pKs_Cu_Cu2O-pC)/1.

def pHsepb(pC):
    return 14-(pKs_Cu_2OH-pC)/2.

def pHcrois(pC):
    return pHsepa(pC) + .5*(Esepza1(pC, pHsepa(pC))-Esepab1(pC, pHsepa(pC)))/RT_on_F

def pHeff_list(pC):
    list = [pHsepa(pC), pHsepb(pC), pHcrois(pC)]
    list.sort()
    return list

def pHeff1(pC):
    return pHeff_list(pC)[0]
def pHeff2(pC):
    return pHeff_list(pC)[1]
def pHeff3(pC):
    return pHeff_list(pC)[2]

def Esepza1(pC, pH):
    return Eza-RT_on_F*pC
def Esepza2(pC, pH):
    return Esepza1(pC, pHsepa(pC)) - RT_on_F*(pH-pHsepa(pC))

def Esepab1(pC, pH):
    return Eab
def Esepab2(pC, pH):
    return Esepab1(pC, pHsepa(pC)) + RT_on_F*(pH-pHsepa(pC))
def Esepab3(pC, pH):
    return Esepab2(pC, pHsepb(pC)) - RT_on_F*(pH-pHsepb(pC))

def Esepzb1(pC, pH):
    return (Esepza1(pC, pH)+Esepab1(pC, pH))/2.
def Esepzb2(pC, pH):
    return (Esepza2(pC, pH)+Esepab2(pC, pH))/2.

def Esepzaeff(pC, pH):
    if pH < pHsepa(pC):
        return min([Esepza1(pC, pH), Esepzb1(pC, pH)])
    else:
        return min([Esepza2(pC, pH), Esepzb2(pC, pH)])

def Esepabeff(pC, pH):
    if pH <  pHsepa(pC):
        return max([Esepab1(pC, pH), Esepzb1(pC, pH)])
    elif pH < pHsepb(pC):
        return max([Esepab2(pC, pH), Esepzb2(pC, pH)])
    else:
        return Esepab3(pC, pH)
    
sep1 = EpHsep('min', pHeff1, Esepzaeff, Esepzaeff)
sep2 = EpHsep(pHeff1, pHeff2, Esepzaeff, Esepzaeff)
sep3 = EpHsep(pHeff2, 'max', Esepzaeff, Esepzaeff)
    
sep4 = EpHsep('min', pHeff1, Esepabeff, Esepabeff)
sep5 = EpHsep(pHeff1, pHeff2, Esepabeff, Esepabeff)
sep6 = EpHsep(pHeff2, pHeff3, Esepabeff, Esepabeff)
sep7 = EpHsep(pHeff3, 'max', Esepabeff, Esepabeff)

sep8 = EpHsep(pHsepb, pHsepb, Esepabeff, 'max')

sep9 = EpHsep(pHsepa, pHsepa, Esepzaeff, Esepabeff)

# if afficher_especes_chimiques is not False:
#     ax.text(0.75*pH_min+0.25*pHsepb, Ecible+.1, 'Cu', color = text_diag_color)
#     ax.text(0.5*pH_min+0.5*pHsepb, 0.5*Esepzb+0.5*E_max, 'Cu$^{2+}$', color = text_diag_color)
#     ax.text(0.25*pH_max+0.75*pHsepb, 0.75*Esepzb+0.25*E_max, 'Cu(OH)$_{2}$', color = text_diag_color)
#     ax.text(0.85*pHsepb+0.15*pH_max, 0.85*Esepzb+0.15*Ecible-.025, 'Cu$_{2}$O', color = text_diag_color)

seps = [sep1, sep2, sep3, sep4, sep5, sep6, sep7, sep8, sep9]
spes = []
