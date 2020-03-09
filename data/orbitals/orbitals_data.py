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

# Shperical harmonics, see
# https://en.wikipedia.org/wiki/Table_of_spherical_harmonics#Spherical_harmonics

def Y00(theta, phi):
    return 1./(2*np.pi**.5)

def Y10(theta, phi):
    return .5*(3./np.pi)**.5*np.cos(theta)
def Y11p(theta, phi):
    return -.5*(3./(2*np.pi))**.5*np.sin(theta)*np.exp(phi*1j)
def Y11m(theta, phi):
    return .5*(3./(2*np.pi))**.5*np.sin(theta)*np.exp(-phi*1j)

def Y20(theta, phi):
    return .25*(5./np.pi)**.5*(3*np.cos(theta)**2-1)
def Y21p(theta, phi):
    return -.5*(15./(2*np.pi))**.5*np.sin(theta)*np.cos(theta)*np.exp(phi*1j)
def Y21m(theta, phi):
    return .5*(15./(2*np.pi))**.5*np.sin(theta)*np.cos(theta)*np.exp(-phi*1j)
def Y22p(theta, phi):
    return .25*(15./(2*np.pi))**.5*np.sin(theta)**2*np.exp(phi*2j)
def Y22m(theta, phi):
    return .25*(15./(2*np.pi))**.5*np.sin(theta)**2*np.exp(-phi*2j)

def Y30(theta, phi):
    return .25 * (7/np.pi)**.5 * (5*np.cos(theta)**3 - 3*np.cos(theta))
def Y31p(theta, phi):
    return -1./8 * (21/np.pi)**.5 * np.sin(theta) * (5*np.cos(theta)**2-1) * np.exp(phi*1j)
def Y31m(theta, phi):
    return 1./8 * (21/np.pi)**.5 * np.sin(theta) * (5*np.cos(theta)**2-1) * np.exp(-phi*1j)
def Y32p(theta, phi):
    return 1./4 * (105/(2*np.pi))**.5 * np.sin(theta)**2 * np.cos(theta) * np.exp(phi*2j)
def Y32m(theta, phi):
    return 1./4 * (105/(2*np.pi))**.5 * np.sin(theta)**2 * np.cos(theta) * np.exp(-phi*2j)
def Y33p(theta, phi):
    return -1./8 * (35/np.pi)**.5 * np.sin(theta)**3 * np.exp(phi*3j)
def Y33m(theta, phi):
    return 1./8 * (35/np.pi)**.5 * np.sin(theta)**3 * np.exp(-phi*3j)

def Y40(theta, phi):
    return 3./16 * (1/np.pi)**.5 * (35 * np.cos(theta)**4 - 30 * np.cos(theta)**2 + 3)
def Y41p(theta, phi):
    return -3./8 * (5/np.pi)**.5 *np.sin(theta) * (7*np.cos(theta)**3-3*np.cos(theta)) * np.exp(phi*1j)
def Y41m(theta, phi):
    return 3./8 * (5/np.pi)**.5 *np.sin(theta) * (7*np.cos(theta)**3-3*np.cos(theta)) * np.exp(-phi*1j)
def Y42p(theta, phi):
    return 3./8 * (5/(2*np.pi))**.5 * np.sin(theta)**2 * (7*np.cos(theta)**2-1) * np.exp(phi*2j)
def Y42m(theta, phi):
    return 3./8 * (5/(2*np.pi))**.5 * np.sin(theta)**2 * (7*np.cos(theta)**2-1) * np.exp(-phi*2j)
def Y43p(theta, phi):
    return -3./8 * (35/np.pi)**.5 * np.sin(theta)**3 * np.cos(theta) * np.exp(phi*3j)
def Y43m(theta, phi):
    return 3./8 * (35/np.pi)**.5 * np.sin(theta)**3 * np.cos(theta) * np.exp(-phi*3j)
def Y44p(theta, phi):
    return 3./16 * (35/(2*np.pi))**.5 * np.sin(theta)**4 * np.exp(phi*4j)
def Y44m(theta, phi):
    return 3./16 * (35/(2*np.pi))**.5 * np.sin(theta)**4 * np.exp(-phi*4j)

def Ys(theta, phi):
    return np.real(Y00(theta, phi))

def Ypz(theta, phi):
    return np.real(Y10(theta, phi))
def Ypx(theta, phi):
    return np.real(.5**(.5) * (-Y11p(theta, phi)+Y11m(theta, phi)))
def Ypy(theta, phi):
    return np.real(.5**(.5) / 1j * (-Y11p(theta, phi)-Y11m(theta, phi)))

def Ydz2(theta, phi):
    return np.real(Y20(theta, phi))
def Ydxz(theta, phi):
    return np.real(.5**(.5) * (-Y21p(theta, phi)+Y21m(theta, phi)))
def Ydyz(theta, phi):
    return np.real(.5**(.5) / 1j * (-Y21p(theta, phi)-Y21m(theta, phi)))
def Ydx2my2(theta, phi):
    return np.real(.5**(.5) * (Y22p(theta, phi)+Y22m(theta, phi)))
def Ydxy(theta, phi):
    return np.real(.5**(.5) /1j * (Y22p(theta, phi)-Y22m(theta, phi)))
# def Ydz2my2(theta, phi):
#     return .25*(15./np.pi)**.5*(np.cos(theta)**2-np.sin(theta)**2*np.sin(phi)**2)
# def Ydz2mx2(theta, phi):
#     return .25*(15./np.pi)**.5*(np.cos(theta)**2-np.sin(theta)**2*np.cos(phi)**2)

def Yfz3(theta, phi):
    return np.real(Y30(theta, phi))
def Yfxz2(theta, phi):
    return np.real(.5**(.5) * (-Y31p(theta, phi)+Y31m(theta, phi)))
def Yfyz2(theta, phi):
    return np.real(.5**(.5) / 1j * (-Y31p(theta, phi)-Y31m(theta, phi)))
def Yfxyz(theta, phi):
    return np.real(.5**(.5) / 1j * (Y32p(theta, phi)-Y32m(theta, phi)))
def Yfzx2my2(theta, phi):
    return np.real(.5**(.5) * (Y32p(theta, phi)+Y32m(theta, phi)))
def Yfxx2m3y2(theta, phi):
    return np.real(.5**(.5) * (-Y33p(theta, phi)+Y33m(theta, phi)))
def Yfy3x2my2(theta, phi):
    return np.real(.5**(.5) / 1j * (-Y33p(theta, phi)-Y33m(theta, phi)))


Y_fcts_C = {
    '00' : Y00,
    '10' : Y10,
    '11p' : Y11p,
    '11m' : Y11m,
    '20' : Y20,
    '21p' : Y21p,
    '21m' : Y21m,
    '22p' : Y22p,
    '22m' : Y22m,
    '30' : Y30,
    '31p' : Y31p,
    '31m' : Y31m,
    '32p' : Y32p,
    '32m' : Y32m,
    '33p' : Y33p,
    '33m' : Y33m,
    # '40' : Y40,
    # '41p' : Y41p,
    # '41m' : Y41m,
    # '42p' : Y42p,
    # '42m' : Y42m,
    # '43p' : Y43p,
    # '43m' : Y43m,
    # '44p' : Y44p,
    # '44m' : Y44m,
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
