Eza = 0.52
Eab = 0.16
pKsCuOHOH = 20
pKsCuCuO = 15

pHsepa = 14-(pKsCuCuO-pC)/1
pHsepb = 14-(pKsCuOHOH-pC)/2

Esepza = Eza-0.06*pC
Esepab = Eab
Esepzb = (Esepza+Esepab)/2

pH_max2 = max([pH_max,pHsepa+1,pHsepb+1])
pH_max = pH_max2
E_min2 = min([E_min,-0.47-0.06*(pH_max-pHsepb)])
E_max2 = max([E_max,1])
E_max = E_max2
E_min = E_min2

Ecible = Esepza - 0.06*pH_max + 0.06*pHsepa

pHcible = (Esepza-Esepab)/0.12+pHsepa
pH_min2 = min([pH_min,pHcible])
pH_min = pH_min2

sep1pH,sep1E = [pH_min, pHsepa,pH_max],[Esepza,Esepza,Ecible]
#lines_to_draw.append([None,sep1pH,sep1E,diag_color])

pHdeb = min([pHsepa,pHsepb])
pHfin = max([pHsepa,pHsepb])

if pHsepa < pHsepb :
    Eciblea = Esepab + (0.06*pHsepb - 0.06*pHsepa)
else :
    Eciblea = Esepab + (0.06*pHsepa - 0.06*pHsepb)

Ecibleb = Eciblea - 0.06*pH_max + 0.06*pHfin

#\draw[thin, dotted] (\pHmin,\Esepab)--(\pHdeb,\Esepab)--(\pHfin,\Eciblea);

sep2pH,sep2E = [pHsepb, pHsepb,pH_max],[E_max,Eciblea,Ecibleb]
functions_to_draw.append(['Cu, $C_{{ {ind} }} = \\SI{{ {C} }}{{ {units} }}$'.format(ind='\\mathrm{{tr}}',C=C,units='mol.L^{-1}'),sep2pH,sep2E,diag_color])



lines_to_draw.append([None,[pH_min, pHcible],[Esepzb, Esepzb],diag_color])
lines_to_draw.append([None,[pHsepb, pHcible, pH_max],[Eciblea, Esepzb, Ecible],diag_color])

if afficher_especes_chimiques is not False:
    ax.text(0.75*pH_min+0.25*pHsepb, Ecible+.1, 'Cu', color = text_diag_color)
    ax.text(0.5*pH_min+0.5*pHsepb, 0.5*Esepzb+0.5*E_max, 'Cu$^{2+}$', color = text_diag_color)
    ax.text(0.25*pH_max+0.75*pHsepb, 0.75*Esepzb+0.25*E_max, 'Cu(OH)$_{2}$', color = text_diag_color)
    ax.text(0.85*pHsepb+0.15*pH_max, 0.85*Esepzb+0.15*Ecible-.025, 'Cu$_{2}$O', color = text_diag_color)

