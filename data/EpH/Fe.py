from ltLaTeXpyplot.data.EpH.EpHgeneric import *

Ezb = -0.44
Ebc = 0.77
pKsFe2OH2 = 15.1
pKsFe2OH3 = 38

def pHsepa(pC):
    return 14-(pKsFe2OH3-pC)/3
def pHsepb(pC):
    return 14-(pKsFe2OH2-pC)/2

def Esepzb(pC, pH):
    return Ezb-RT_on_F/2*pC

def Esepbc(pC, pH):
    return Ebc

def Ecible(pC, pH):
    return Esepbc(pC, pH)-RT_on_F*3*pHsepb(pC)+RT_on_F*3*pHsepa(pC)

def Efa(pC, pH):
    return Ecible(pC, pH)-RT_on_F*pH+RT_on_F*pHsepb(pC)
def Efb(pC, pH):
    return Esepzb(pC, pH)-RT_on_F*pH+RT_on_F*pHsepb(pC)

sep1 = EpHsep('min', pHsepa, Esepbc, Esepbc)
sep2 = EpHsep('min', pHsepb, Esepzb, Esepzb)
sep3a = EpHsep(pHsepa, pHsepa, 'max', Esepbc)
sep3b = EpHsep(pHsepa, pHsepb, Esepbc, Ecible)
sep3c = EpHsep(pHsepb, pHsepb, Ecible, Esepzb)
sep4 = EpHsep(pHsepb, 'max', Ecible, Efa)
sep5 = EpHsep(pHsepb, 'max', Esepzb, Efb)

# if afficher_especes_chimiques is not False:
#     ax.text(0.75*pH_min+0.25*pHsepa, Ebc+.1, 'Fe$^{3+}$', color = text_diag_color)
#     ax.text(0.7*pH_min+0.3*pHsepb, 0.5*Ebc+0.5*Ezb, 'Fe$^{2+}$', color = text_diag_color)
#     ax.text(0.5*pH_min+0.5*pH_max, 0.5*Esepzb+0.5*E_min, 'Fe', color = text_diag_color)
#     ax.text(0.5*pHsepa+0.5*pH_max,.5*Ebc+.5*Ecible, 'Fe(OH)$_{3}$', color = text_diag_color)
#     ax.text(0.6*pHsepb+0.4*pH_max,0.5*Ecible+0.5*Efb, 'Fe(OH)$_{2}$', color = text_diag_color)



seps = [sep1, sep2, sep3a, sep3b, sep3c, sep4, sep5]
spes = []
