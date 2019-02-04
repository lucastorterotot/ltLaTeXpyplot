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

def Esepbc_plus(pC, pH):
    return Ebc + .2

def Ecible(pC, pH):
    return Esepbc(pC, pH)-RT_on_F*3*pHsepb(pC)+RT_on_F*3*pHsepa(pC)

def Efa(pC, pH):
    return Ecible(pC, pH)-RT_on_F*pH+RT_on_F*pHsepb(pC)
def Efb(pC, pH):
    return Esepzb(pC, pH)-RT_on_F*pH+RT_on_F*pHsepb(pC)

sep1 = EpHsep('min', pHsepa, Esepbc, Esepbc)
sep2 = EpHsep('min', pHsepb, Esepzb, Esepzb)
sep3a1 = EpHsep(pHsepa, pHsepa, Esepbc, Esepbc_plus)
sep3a2 = EpHsep(pHsepa, pHsepa, 'max', Esepbc_plus)
sep3b = EpHsep(pHsepa, pHsepb, Esepbc, Ecible)
sep3c = EpHsep(pHsepb, pHsepb, Ecible, Esepzb)
sep4 = EpHsep(pHsepb, 'max', Ecible, Efa)
sep5 = EpHsep(pHsepb, 'max', Esepzb, Efb)

spe1 = EpHspe('Fe$^{3+}$', 'min', pHsepa, 'max', Esepbc)
spe2 = EpHspe('Fe$^{2+}$', 'min', pHsepb, Esepbc, Esepzb)
spe3 = EpHspe('Fe', 'min', 'max', Esepzb, 'min')
spe4 = EpHspe('Fe(OH)$_{3}$', pHsepa, 'max', Esepbc, Ecible, pH_r=.6)
spe5 = EpHspe('Fe(OH)$_{2}$', pHsepb, 'max', Efb, Efa)

seps = [sep1, sep2, sep3a1, sep3a2, sep3b, sep3c, sep4, sep5]
spes = [spe1, spe2, spe3, spe4, spe5]
