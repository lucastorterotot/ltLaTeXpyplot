Eza = 0.8
pKs_AgI = 16.1

pI_sep = pKs_AgI - pC

Esepza = Eza - 0.06 * pC

pI_min = min([pH_min,pI_sep-1])
pI_max = max([pH_max,pI_sep+1])
pH_min, pH_max = pI_min, pI_max

Esep_pI_min = Esepza + 0.06 * (pI_min - pI_sep)

E_min2 = min([E_min, Esepza-.1, Esep_pI_min-.1])
E_max2 = max([E_max, Esepza+.1, Esep_pI_min+.1])
E_max = E_max2
E_min = E_min2

sep1pI, sep1E = [pI_min, pI_sep, pI_max], [Esep_pI_min, Esepza, Esepza]

functions_to_draw.append(['Ag, $C_{{ {ind} }} = \\SI{{ {C} }}{{ {units} }}$'.format(ind='\\mathrm{{tr}}',C=C,units='mol.L^{-1}'),sep1pI,sep1E,diag_color])

lines_to_draw.append([None,[pI_sep, pI_sep],[Esepza, E_max],diag_color])

if afficher_especes_chimiques is not False:
    ax.text(.5*pI_sep + .5*pI_max, .5*Esepza + .5*E_max, 'Ag$^+$', color = text_diag_color)
    ax.text(.5*pI_sep + .5*pI_max, .5*Esepza + .5*Esep_pI_min, 'Ag', color = text_diag_color)
    ax.text(.5*pI_sep + .5*pI_min, Esepza, 'AgI', color = text_diag_color)

