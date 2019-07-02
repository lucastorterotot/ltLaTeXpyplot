#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import ltLaTeXpyplot as lt
import ltLaTeXpyplot.data.orbitals.orbitals_data as data # uses the orbital data of this package

steps = 50
theta = np.arange(0,np.pi*(1+1./steps),np.pi/steps)
phi = np.arange(-np.pi*(1+1./steps),np.pi*(1+1./steps),np.pi/steps)

print('  Creating orbitals: Ylm representations...')

to_process = {'dz2' : data.Y_fcts_R['dz2'],
              '21p' : data.Y_fcts_C['21p']}

ntot = len(to_process)
ncur = 0
for dic in [to_process]:
    for key, Ylm in dic.items():
        cmap = 'coolwarm'
        if key in ['s', '00']:
            cmap += '_r'
        ncur += 1
        fig = lt.ltFigure(name='orbitale-'+key, height_width_ratio=1)
        def R_fct(theta, phi):
            return (np.absolute(Ylm(theta, phi)))**2
        def C_fct(theta, phi):
            return (2*np.sign(np.real(Ylm(theta, phi)))+np.sign(np.imag(Ylm(theta, phi))))+0*theta

        max_range = 3/8
        fig.addgraph('graph1', projection='3d', x_ticks=False, y_ticks=False, z_ticks=False,
                     x_min=-max_range, x_max=max_range, y_min=-max_range, y_max=max_range, z_min=-max_range, z_max=max_range)

        fig.addplot(lt.ltPlotSurf(theta, phi, R_fct=R_fct, linewidth=.1, C_fct=C_fct, use_cmap=True, cmap=cmap), 'graph1')

        print('    Orbital ', ncur, '/', ntot, ' : '+key)

        fig.save(format='png')

print('  Orbitals created.')
