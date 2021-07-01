from ltLaTeXpyplot.module.EpHgeneric import *

E0 = 1.23

def E1 (pC, pH):
    return E0-RT_on_F*pH

def E1_up(pC, pH):
    return E1(pC, pH)+.1
def E1_down(pC, pH):
    return E1(pC, pH)-.1

sep1 = EpHsep('min', 'max', E1, E1)

spe1 = EpHspe('O$_2$', 'min', 'max', E1_up, E1_up, pH_r=.25, E_r=.25)
spe2 = EpHspe('H$_2$O', 'min', 'max', E1_down, E1_down, pH_r=.25, E_r=.25)

seps = [sep1]
spes = [spe1, spe2]
