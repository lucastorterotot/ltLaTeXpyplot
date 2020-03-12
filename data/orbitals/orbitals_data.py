import numpy as np
from scipy.constants import Planck, epsilon_0, electron_mass, elementary_charge, proton_mass

a0 = Planck*Planck * epsilon_0 / (np.pi * electron_mass * elementary_charge*elementary_charge)

r_on_a0_max ={
    '1x' : 6,
    '2x' : 15,
    '3x' : 30,
    '4x' : 50}
r_on_a0_MAX = max([value for value in r_on_a0_max.values()])

from scipy.special import genlaguerre
from math import factorial

def Rnl(r,n,l,Z=1,a0=a0):
    u = Z/a0
    return ((2* u/n)**3 * (factorial(n-l-1))/(2*n*(factorial(n+l))**3))**.5 * np.exp(-u/n*r) * (2* u/n * r)**l * genlaguerre(n-l-1,2*l+1)(2* u/n * r)

from scipy.special import lpmv

def unnorm_Ylm(theta, phi, l, m):
    return np.exp(phi * m * 1j) * lpmv(m, l, np.cos(theta))

Ylm_normalizers = {}

def Ylm(theta, phi, l, m):
    if '{}_{}'.format(l,m) in Ylm_normalizers:
        return Ylm_normalizers['{}_{}'.format(l,m)] * unnorm_Ylm(theta, phi, l, m)
    else: # compute the normalizer
        print("\tComputing normalization factor for Y {} {}.".format(l,m))
        steps = 100
        thetas = np.arange(0,np.pi*(1+1./steps),np.pi/steps)
        phis = np.arange(-np.pi*(1+1./steps),np.pi*(1+1./steps),np.pi/steps)
        integral = 0
        Delta = (thetas[-1]-thetas[0])*(phis[-1]-phis[0])/(len(thetas)*len(phis))
        for t in thetas:
            for p in phis:
                integral += np.absolute(unnorm_Ylm(t, p, l, m))**2 * np.sin(t) * Delta
        Ylm_normalizers['{}_{}'.format(l,m)] = np.sqrt(1./integral)
        return Ylm(theta, phi, l, m)

def Ys(theta, phi):
    return np.real(Ylm(theta, phi, 0, 0))

def Ypz(theta, phi):
    return np.real(Ylm(theta, phi, 1, 0))
def Ypx(theta, phi):
    return np.real(.5**(.5) * (-Ylm(theta, phi, 1, 1)+Ylm(theta, phi, 1, -1)))
def Ypy(theta, phi):
    return np.real(.5**(.5) / 1j * (-Ylm(theta, phi, 1, 1)-Ylm(theta, phi, 1, -1)))

def Ydz2(theta, phi):
    return np.real(Ylm(theta, phi, 2, 0))
def Ydxz(theta, phi):
    return np.real(.5**(.5) * (-Ylm(theta, phi, 2, 1)+Ylm(theta, phi, 2, -1)))
def Ydyz(theta, phi):
    return np.real(.5**(.5) / 1j * (-Ylm(theta, phi, 2, 1)-Ylm(theta, phi, 2, -1)))
def Ydx2my2(theta, phi):
    return np.real(.5**(.5) * (Ylm(theta, phi, 2, 2)+Ylm(theta, phi, 2, 2)))
def Ydxy(theta, phi):
    return np.real(.5**(.5) /1j * (Ylm(theta, phi, 2, 2)-Ylm(theta, phi, 2, -2)))
# def Ydz2my2(theta, phi):
#     return .25*(15./np.pi)**.5*(np.cos(theta)**2-np.sin(theta)**2*np.sin(phi)**2)
# def Ydz2mx2(theta, phi):
#     return .25*(15./np.pi)**.5*(np.cos(theta)**2-np.sin(theta)**2*np.cos(phi)**2)

def Yfz3(theta, phi):
    return np.real(Ylm(theta, phi, 3, 0))
def Yfxz2(theta, phi):
    return np.real(.5**(.5) * (-Ylm(theta, phi, 3, 1)+Ylm(theta, phi, 3, -1)))
def Yfyz2(theta, phi):
    return np.real(.5**(.5) / 1j * (-Ylm(theta, phi, 3, 1)-Ylm(theta, phi, 3, -1)))
def Yfxyz(theta, phi):
    return np.real(.5**(.5) / 1j * (Ylm(theta, phi, 3, 2)-Ylm(theta, phi, 3, -2)))
def Yfzx2my2(theta, phi):
    return np.real(.5**(.5) * (Ylm(theta, phi, 3, 2)+Ylm(theta, phi, 3, -2)))
def Yfxx2m3y2(theta, phi):
    return np.real(.5**(.5) * (-Ylm(theta, phi, 3, 3)+Ylm(theta, phi, 3, -3)))
def Yfy3x2my2(theta, phi):
    return np.real(.5**(.5) / 1j * (-Ylm(theta, phi, 3, 3)-Ylm(theta, phi, 3, -3)))

Y_fcts_R = {
    's' : Ys,
    'pz' : Ypz,
    'px' : Ypx,
    'py' : Ypy,
    'dz2' : Ydz2,
    'dxz' : Ydxz,
    'dyz' : Ydyz,
    'dxy' : Ydxy,
    'dx2-y2' : Ydx2my2,
    'fz3' : Yfz3,
    'fxz2' : Yfxz2,
    'fyz2' : Yfyz2,
    'fxyz' : Yfxyz,
    'fz_x2-y2' : Yfzx2my2,
    'fx_x2-3y2' : Yfxx2m3y2,
    'fy3_x2-y2' : Yfy3x2my2,
}

orbitals = ['1s',
            '2s',
            '2px', '2py', '2pz',
            '3s',
            '3px', '3py', '3pz',
            '3dz2', '3dxz', '3dyz', '3dxy', '3dx2-y2',
            '4s',
            '4px', '4py', '4pz',
            '4dz2', '4dxz', '4dyz', '4dxy', '4dx2-y2',
            '4fz3', '4fxz2', '4fyz2', '4fxyz', '4fz_x2-y2', '4fx_x2-3y2', '4fy3_x2-y2']

orbital_to_L = {'s':0, 'p':1, 'd':2, 'f':3}
