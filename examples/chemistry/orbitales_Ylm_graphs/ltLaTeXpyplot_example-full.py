#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import ltLaTeXpyplot as lt
import ltLaTeXpyplot.data.orbitals.orbitals_data as data # uses the orbital data of this package
import matplotlib.pyplot as plt

steps = 50
theta = np.arange(0,np.pi*(1+1./steps),np.pi/steps)
phi = np.arange(-np.pi*(1+1./steps),np.pi*(1+1./steps),np.pi/steps)

print('  Creating orbitals: Ylm real representations...')

ntot = len(data.Y_fcts_R)
ncur = 0
for key, Ylm in data.Y_fcts_R.items():
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
    plt.close()

print('  Creating orbitals: Ylm complex representations...')

l_max = 3
ntot = 0
for l in range(l_max+1):
    ntot += 1+2*l
ncur = 0

for l in range(l_max+1):
    for m in range(-l,l+1):
        cmap = 'coolwarm'
        if l == 0 and m == 0:
            cmap += '_r'
        ncur += 1

        sm = ''
        if m<0:
            sm = 'm'
        if m>0:
            sm = 'p'
        fig = lt.ltFigure(name='orbitale-{}{}{}'.format(l,abs(m),sm), height_width_ratio=1)
        def R_fct(theta, phi):
            return (np.absolute(data.Ylm(theta, phi, l, m)))**2
        def C_fct(theta, phi):
            return (2*np.sign(np.real(data.Ylm(theta, phi, l, m)))+np.sign(np.imag(data.Ylm(theta, phi, l, m))))+0*theta

        max_range = 3/8
        fig.addgraph('graph1', projection='3d', x_ticks=False, y_ticks=False, z_ticks=False,
                     x_min=-max_range, x_max=max_range, y_min=-max_range, y_max=max_range, z_min=-max_range, z_max=max_range)

        fig.addplot(lt.ltPlotSurf(theta, phi, R_fct=R_fct, linewidth=.1, C_fct=C_fct, use_cmap=True, cmap=cmap, norm_xyz=True), 'graph1')

        print('    Orbital {}/{} : {}{}'.format(ncur, ntot, l, m))
        fig.save(format='png')
        plt.close()

print('  Orbitals created.')
