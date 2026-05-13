from ltLaTeXpyplot.module.EpHgeneric import *

Eza = 0.52
Eab = 0.16
pKs_Cu_2OH = 18
pKs_Cu_Cu2O = 14

def pHsepa(pC, convention):
    return 14-(pKs_Cu_Cu2O-pC)/1.

def pHsepb(pC, convention):
    return 14-(pKs_Cu_2OH-pC)/2.

def pHcrois(pC, convention):
    return pHsepa(pC, convention) + .5*(Esepza1(pC, convention, pHsepa(pC, convention))-Esepab1(pC, convention, pHsepa(pC, convention)))/RT_on_F

def pHeff_list(pC, convention):
    list = [pHsepa(pC, convention), pHsepb(pC, convention), pHcrois(pC, convention)]
    list.sort()
    return list

def pHeff1(pC, convention):
    return pHeff_list(pC, convention)[0]
def pHeff2(pC, convention):
    return pHeff_list(pC, convention)[1]
def pHeff3(pC, convention):
    return pHeff_list(pC, convention)[2]

def Esepza1(pC, convention, pH):
    return Eza-RT_on_F*pC
def Esepza2(pC, convention, pH):
    return Esepza1(pC, convention, pHsepa(pC, convention)) - RT_on_F*(pH-pHsepa(pC, convention))

def Esepab1(pC, convention, pH):
    return Eab
def Esepab2(pC, convention, pH):
    return Esepab1(pC, convention, pHsepa(pC, convention)) + RT_on_F*(pH-pHsepa(pC, convention))
def Esepab3(pC, convention, pH):
    return Esepab2(pC, convention, pHsepb(pC, convention)) - RT_on_F*(pH-pHsepb(pC, convention))

def Esepzb1(pC, convention, pH):
    return (Esepza1(pC, convention, pH)+Esepab1(pC, convention, pH))/2.
def Esepzb2(pC, convention, pH):
    return (Esepza2(pC, convention, pH)+Esepab2(pC, convention, pH))/2.

def Esepzaeff(pC, convention, pH):
    if pH < pHsepa(pC, convention):
        return min([Esepza1(pC, convention, pH), Esepzb1(pC, convention, pH)])
    else:
        return min([Esepza2(pC, convention, pH), Esepzb2(pC, convention, pH)])

def Esepabeff(pC, convention, pH):
    if pH <  pHsepa(pC, convention):
        return max([Esepab1(pC, convention, pH), Esepzb1(pC, convention, pH)])
    elif pH < pHsepb(pC, convention):
        return max([Esepab2(pC, convention, pH), Esepzb2(pC, convention, pH)])
    else:
        return Esepab3(pC, convention, pH)

def Esepabeff_plus(pC, convention, pH):
    return Esepabeff(pC, convention, pH) + .25
    
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

def condition_I(pC, convention):
    return Esepza1(pC, convention, 0) < Esepab1(pC, convention, 0)

spe5 = EpHspe('Cu$^+$', 'min', pHsepa, Esepzaeff, Esepabeff, condition=condition_I)

seps = [sep1, sep2, sep3, sep4, sep5, sep6, sep7, sep8a, sep8b, sep9]

spes = [spe1, spe2, spe3, spe4, spe5]
