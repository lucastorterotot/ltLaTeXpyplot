from EpHgeneric import *

E0 = 1.23

def E1 (pC, pH):
    return E0-RT_on_F*pH

sep1 = EpHsep('min', 'max', E1, E1)

# if afficher_especes_chimiques is not False:
#     ax.text(0.75*pH_min+0.25*pH_max, E0-RT_on_F*(0.75*pH_min+0.25*pH_max)+.05, 'H$_{2}$O', color = text_diag_color)
#     ax.text(0.75*pH_min+0.25*pH_max, E0-RT_on_F*(0.75*pH_min+0.25*pH_max)-.1, 'O$_{2}$', color = text_diag_color)

seps = [sep1]
spes = []
