Eaz = 0.54
Ezb = 1.19


Esepaz = Eaz + 0.06/2* np.log10(2./concentration_travail)

pHsep = 10./(0.06*12)*(Ezb - Esepaz +0.06/10*np.log10(concentration_travail/2.))

pH_max2 = max([pH_max,pHsep+1])
pH_max = pH_max2

pH_min2 = min([pH_min,0,pHsep-1])
pH_min = pH_min2

Esepzb1 = Ezb + 0.06/10*np.log10(concentration_travail/2.) - 0.06*12./10.*pH_min
Esepzb2 = Esepaz

Esepab2 = Esepzb2 - 0.06*(pH_max - pHsep)

E_min2 = min([E_min, Esepaz, Esepzb1, Esepzb2, Esepab2])
E_max2 = max([E_max, Esepaz, Esepzb1, Esepzb2, Esepab2])
E_max = E_max2
E_min = E_min2

sep1pH,sep1E = [pH_min, pHsep, pH_max],[Esepaz, Esepaz, Esepab2]

sep2pH,sep2E = [pH_min, pHsep],[Esepzb1, Esepzb2]

functions_to_draw.append(['I, $C_{{ {ind} }} = \\SI{{ {C} }}{{ {units} }}$'.format(ind='\\mathrm{{tr}}',C=C,units='mol.L^{-1}'),sep1pH,sep1E,diag_color])

lines_to_draw.append([None,sep2pH,sep2E,diag_color])

if afficher_especes_chimiques is not False:
    ax.text(0.9*pH_min+0.1*pHsep, 0.25*sep2E[0]+0.75*sep2E[1], 'I$_{2}$', color = text_diag_color)
    ax.text(0.5*pH_min+0.5*pH_max, 0.5*Esepaz+0.5*E_max, 'IO$_3^-$', color = text_diag_color)
    ax.text(0.25*pH_min+0.75*pHsep, 0.8*Esepaz+0.2*E_min, 'I$^-$', color = text_diag_color)
