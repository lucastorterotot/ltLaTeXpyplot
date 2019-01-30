from EpHgeneric import *


Eza = 0.52
Eab = 0.16
pKsCuOHOH = 20
pKsCuCuO = 15

def pHsepa(pC):
    return 14-(pKsCuCuO-pC)/1.

def pHsepb(pC):
    return 14-(pKsCuOHOH-pC)/2.

def Esepza(pC, pH):
    return Eza-0.06*pC
def Esepab(pC, pH):
    return Eab
def Esepzb(pC, pH):
    return (Esepza(pC, pH)+Esepab(pC, pH))/2.

def Ecible(pC, pH):
    return Esepza(pC, pH) - 0.06*pH + 0.06*pHsepa(pC)

def pHcible(pC):
    return (Esepza(pC,0)-Esepab(pC, 0))/0.12+pHsepa(pC)

# Not really
sep1 = EpHsep('min', pHsepa, Esepza, Esepza)
sep2 = EpHsep(pHsepa, 'max', Esepza, Ecible)

def pHdeb(pC):
    return min([pHsepa(pC),pHsepb(pC)])
def pHfin(pC):
    return max([pHsepa(pC),pHsepb(pC)])

def Eciblea(pC, pH):
    return Esepab(pC, pH) + 0.06*abs(pHsepb(pC) - pHsepa(pC))

def Ecibleb(pC, pH):
    return Eciblea(pC, pH) - 0.06*pH + 0.06*pHfin(pC)

sep3 = EpHsep(pHsepb, pHsepb, 'max', Eciblea)
sep4 = EpHsep(pHsepb, 'max', Eciblea, Ecibleb)
sep5 = EpHsep('min', pHcible, Esepzb, Esepzb)
sep6 = EpHsep(pHsepb, pHcible, Eciblea, Esepzb)
sep7 = EpHsep(pHcible, 'max', Esepzb, Ecible)

# if afficher_especes_chimiques is not False:
#     ax.text(0.75*pH_min+0.25*pHsepb, Ecible+.1, 'Cu', color = text_diag_color)
#     ax.text(0.5*pH_min+0.5*pHsepb, 0.5*Esepzb+0.5*E_max, 'Cu$^{2+}$', color = text_diag_color)
#     ax.text(0.25*pH_max+0.75*pHsepb, 0.75*Esepzb+0.25*E_max, 'Cu(OH)$_{2}$', color = text_diag_color)
#     ax.text(0.85*pHsepb+0.15*pH_max, 0.85*Esepzb+0.15*Ecible-.025, 'Cu$_{2}$O', color = text_diag_color)

seps = [sep3, sep4, sep5, sep6, sep7]
spes = []
