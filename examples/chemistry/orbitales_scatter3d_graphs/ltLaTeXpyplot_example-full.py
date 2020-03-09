#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import ltLaTeXpyplot as lt
import ltLaTeXpyplot.data.orbitals.orbitals_data as data # uses the orbital data of this package
import matplotlib.pyplot as plt

r_on_a0 = np.arange(0,data.r_on_a0_MAX,0.1)

radius = r_on_a0*data.a0

Rnl = data.Rnl

steps = 50
theta = np.arange(0,np.pi*(1+1./steps),np.pi/steps)
phi = np.arange(-np.pi*(1+1./steps),np.pi*(1+1./steps),np.pi/steps)


print('  Creating orbitals: scatter plots...')

ntot = len(data.orbitals)
ncur = 0

size = 2000

for key in data.orbitals:
    cmap = 'coolwarm'
    if key in ['1s', 's', '00'] :
        cmap += '_r'
    ncur += 1
    
    fig = lt.ltFigure(name='orbitale-'+key, height_width_ratio=1)
    max_range = data.r_on_a0_max["3x"] * data.a0
    fig.addgraph('graph1', projection='3d', x_ticks=False, y_ticks=False, z_ticks=False,
                 x_min=-max_range, x_max=max_range, y_min=-max_range, y_max=max_range, z_min=-max_range, z_max=max_range)

    n = int(key[0])
    l = data.orbital_to_L[key[1]]
    Ylm_fct = data.Y_fcts_R[key[1:]]
    
    t0, p0 = .5**.5, .5**.5
    
    def r_proba(r):
        return 4 * np.pi * r**2 * Rnl(r,n,l)**2+0*r
    def t_proba(t):
        return np.absolute(Ylm_fct(t, p0))**2+0*t
    def p_proba(p):
        return np.absolute(Ylm_fct(t0, p))**2+0*p

    r_proba_int = 0
    t_proba_int = 0
    p_proba_int = 0
    
    for value in radius:
        r_proba_int += r_proba(value)
    for value in theta:
        t_proba_int += t_proba(value)
    for value in phi:
        p_proba_int += p_proba(value)

    def pdf_r(r):
        return r_proba(r)/r_proba_int
    def pdf_t(t):
        return t_proba(t)/t_proba_int
    def pdf_p(p):
        return p_proba(p)/p_proba_int
        
    random_r = np.random.choice(radius, p=pdf_r(radius), size=size)
    random_t = np.random.choice(theta, p=pdf_t(theta), size=size)
    random_p = np.random.choice(phi, p=pdf_p(phi), size=size)
    
    x = random_r * np.cos(random_p) * np.sin(random_t)
    y = random_r * np.sin(random_p) * np.sin(random_t)
    z = random_r * np.cos(random_t)
    
    def C_fct(r, theta, phi):
        return (np.sign(Rnl(r,n,l) * np.real(Ylm_fct(theta, phi))))+0*theta

    fig.addplot(lt.ltPlotPts3d(x, y, z, marker='.', markersize=1, color=C_fct(random_r, random_t, random_p), cmap=cmap), 'graph1')

    print('    Orbital ', ncur, '/', ntot, ' : '+key)

    fig.save(format='png')
    plt.close()

print('  Orbitals created.')
