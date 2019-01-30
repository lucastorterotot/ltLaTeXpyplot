Eza = 1.4
Eab = 1.59
pKa_HClO_ClO = 7.5

Esepza = Eza
#Esepab = Eab + 0.03 * np.log10((concentration_travail*2./3)**2/(concentration_travail*1./3)) - 0.06*pH
#Esepzb1 = (Eza+Eab)*.5 - 0.03*pH
#Esepzb2 = (Eza+Eab)*.5 - 0.03 * pKa_HClO_ClO - 0.06*pH

pHsepa = (Eab + 0.03 * np.log10((concentration_travail*2./3)**2/    (concentration_travail*1./3)) - Eza)/0.06
pHsepb = pKa_HClO_ClO

pH_max2 = max([pH_max,pHsepa+1,pHsepb+1])
pH_max = pH_max2

E_min2 = min([E_min,(Eza+Eab)*.5 - 0.03 * pKa_HClO_ClO - 0.06*pH_max])
E_max2 = max([E_max, Eza, Eab + 0.03 * np.log10((concentration_travail*2./3)**2/(concentration_travail*1./3))])
E_max = E_max2
E_min = E_min2

pH_min2 = min([pH_min,0])
pH_min = pH_min2

sep1pH,sep1E = [pH_min, pHsepa, pHsepb, pH_max],[Esepza, Esepza, (Eza+Eab)*.5 - 0.03*pHsepb, (Eza+Eab)*.5 - 0.03 * pKa_HClO_ClO - 0.06*(pH_max-pHsepb)]

sep2pH,sep2E = [pH_min, pHsepa],[Eab + 0.03 * np.log10((concentration_travail*2./3)**2/(concentration_travail*1./3)) - 0.06*pH_min, Esepza]

functions_to_draw.append(['Cl, $C_{{ {ind} }} = \\SI{{ {C} }}{{ {units} }}$'.format(ind='\\mathrm{{tr}}',C=C,units='mol.L^{-1}'),sep1pH,sep1E,diag_color])

lines_to_draw.append([None,sep2pH,sep2E,diag_color])

lines_to_draw.append([None,[pHsepb, pHsepb],[(Eza+Eab)*.5 - 0.03*pHsepb, E_max],diag_color])

if afficher_especes_chimiques is not False:
    ax.text(pH_min, 0.1*sep2E[0]+0.9*sep2E[1], 'Cl$_{2}$', color = text_diag_color)
    ax.text(0.5*pH_min+0.5*pHsepb, 0.5*Esepza+0.5*E_max, 'HClO', color = text_diag_color)
    ax.text(0.25*pH_min+0.75*pHsepb, 0.8*Esepza+0.2*E_min, 'Cl$^-$', color = text_diag_color)
    ax.text(0.5*pH_max+0.5*pHsepb, 0.75*Esepza+0.25*E_max, 'ClO$^-$', color = text_diag_color)
