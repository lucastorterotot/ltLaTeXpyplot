from ltLaTeXpyplot.module.EpHgeneric import *

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

def Esepabeff_plus(pC, pH):
    return Esepabeff(pC, pH) + .25
    
sep1 = EpHsep('min', pHeff1, Esepzaeff, Esepzaeff)
sep2 = EpHsep(pHeff1, pHeff2, Esepzaeff, Esepzaeff)
sep3 = EpHsep(pHeff2, 'max', Esepzaeff, Esepzaeff)
    
sep4 = EpHsep('min', pHeff1, Esepabeff, Esepabeff)
sep5 = EpHsep(pHeff1, pHeff2, Esepabeff, Esepabeff)
sep6 = EpHsep(pHeff2, pHeff3, Esepabeff, Esepabeff)
sep7 = EpHsep(pHeff3, 'max', Esepabeff, Esepabeff)

sep8a = EpHsep(pHsepb, pHsepb, Esepabeff, Esepabeff_plus)
sep8b = EpHsep(pHsepb, pHsepb, Esepabeff_plus, 'max')

sep9 = EpHsep(pHsepa, pHsepa, Esepzaeff, Esepabeff)

spe1 = EpHspe('Cu', 'min', 'max', Esepzaeff, Esepzaeff)
spe2 = EpHspe('Cu$_2$O', pHeff3, 'max', Esepabeff, Esepzaeff)
spe3 = EpHspe('Cu(OH)$_2$', pHsepb, 'max', Esepabeff, 'max', E_r=.25)
spe4 = EpHspe('Cu$^{2+}$', 'min', pHsepb, 'max', Esepabeff, E_r=.75)

def condition_I(pC):
    return Esepza1(pC, 0) < Esepab1(pC, 0)

spe5 = EpHspe('Cu$^+$', 'min', pHsepa, Esepzaeff, Esepabeff, condition=condition_I)

seps = [sep1, sep2, sep3, sep4, sep5, sep6, sep7, sep8a, sep8b, sep9]

spes = [spe1, spe2, spe3, spe4, spe5]
