import numpy as np
from scipy.constants import Planck, epsilon_0, electron_mass, elementary_charge

a0 = Planck*Planck * epsilon_0 / (np.pi * electron_mass * elementary_charge*elementary_charge)

Z = 1 # for hydrogene
alpha = Z/a0

r_on_a0_max ={
    '1x' : 6,
    '2x' : 15,
    '3x' : 30}
r_on_a0_MAX = max([value for value in r_on_a0_max.values()])

def R10(r):
    u = Z*r/a0
    return 2*alpha**(3./2)*np.exp(-u)
def R20(r):
    u = Z*r/a0
    return alpha**(3./2)*2**-.5*(1-u/2)*np.exp(-u/2)
def R21(r):
    u = Z*r/a0
    return alpha**(5./2)/(2*6**.5)*r*np.exp(-u/2)
def R30(r):
    u = Z*r/a0
    return 2*alpha**(3./2)/(9*3**.5)*(3-2*u+2./9*u**2)*np.exp(-u/3)
def R31(r):
    u = Z*r/a0
    return 4*alpha**(5./2)/(27*6**.5)*r*(2-u/3)*np.exp(-u/3)
def R32(r):
    u = Z*r/a0
    return 4*alpha**(7./2)/(81*30**.5)*r**2*np.exp(-u/3)
    
R_fcts = {
    '10' : R10,
    '20' : R20,
    '21' : R21,
    '30' : R30,
    '31' : R31,
    '32' : R32
}

def Y00(theta, phi):
    return 1./(2*np.pi**.5)
def Y10(theta, phi):
    return .5*(3./np.pi)**.5*np.cos(theta)
def Y11p(theta, phi):
    return .5*(3./(2*np.pi))**.5*np.sin(theta)*np.exp(phi*1j)
def Y11m(theta, phi):
    return .5*(3./(2*np.pi))**.5*np.sin(theta)*np.exp(-phi*1j)
def Y20(theta, phi):
    return .25*(5./np.pi)**.5*(3*np.cos(theta)**2-1)
def Y21p(theta, phi):
    return .5*(15./(2*np.pi))**.5*np.sin(theta)*np.cos(theta)*np.exp(phi*1j)
def Y21m(theta, phi):
    return .5*(15./(2*np.pi))**.5*np.sin(theta)*np.cos(theta)*np.exp(-phi*1j)
def Y22p(theta, phi):
    return .25*(15./(2*np.pi))**.5*np.sin(theta)**2*np.exp(phi*2j)
def Y22m(theta, phi):
    return .25*(15./(2*np.pi))**.5*np.sin(theta)**2*np.exp(-phi*2j)

def Ys(theta, phi):
    return np.real(Y00(theta, phi))
def Ypz(theta, phi):
    return np.real(Y10(theta, phi))
def Ypx(theta, phi):
    return np.real(.5**(.5) * (Y11p(theta, phi)+Y11m(theta, phi)))
def Ypy(theta, phi):
    return np.real(.5**(.5) / 1j * (Y11p(theta, phi)-Y11m(theta, phi)))
def Ydz2(theta, phi):
    return np.real(Y20(theta, phi))
def Ydxz(theta, phi):
    return np.real(.5**(.5) * (Y21p(theta, phi)+Y21m(theta, phi)))
def Ydyz(theta, phi):
    return np.real(.5**(.5) / 1j * (Y21p(theta, phi)-Y21m(theta, phi)))
def Ydx2my2(theta, phi):
    return np.real(.5**(.5) * (Y22p(theta, phi)+Y22m(theta, phi)))
def Ydxy(theta, phi):
    return np.real(.5**(.5) /1j * (Y22p(theta, phi)-Y22m(theta, phi)))
# def Ydz2my2(theta, phi):
#     return .25*(15./np.pi)**.5*(np.cos(theta)**2-np.sin(theta)**2*np.sin(phi)**2)
# def Ydz2mx2(theta, phi):
#     return .25*(15./np.pi)**.5*(np.cos(theta)**2-np.sin(theta)**2*np.cos(phi)**2)

Y_fcts_C = {
    '00' : Y00,
    '10' : Y10,
    '11p' : Y11p,
    '11m' : Y11m,
    '20' : Y20,
    '21p' : Y21p,
    '21m' : Y21m,
    '22p' : Y22p,
    '22m' : Y22m
}

Y_fcts_R = {
    's' : Ys,
    'pz' : Ypz,
    'px' : Ypx,
    'py' : Ypy,
    'dz2' : Ydz2,
    'dxz' : Ydxz,
    'dyz' : Ydyz,
    'dxy' : Ydxy,
    'dx2-y2' : Ydx2my2
}

orbitals = ['1s', '2s', '2px', '2py', '2pz', '3s', '3px', '3py', '3pz', '3dz2', '3dxz', '3dyz', '3dxy', '3dx2-y2']

orbital_to_L = {'s':0, 'p':1, 'd':2, 'f':3}
