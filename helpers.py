''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import numpy as np
import scipy.constants as const
import math

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models import Span
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

# Mass of the sun in kg
SUN_MASS = 1.989 * 10**30

def calcChirpMass(m1, m2):
    m1 *= SUN_MASS
    m2 *= SUN_MASS
    return pow(m1*m2, 3/5) / pow(m1+m2, 1/5)

def calcTcoal(m1, m2, f):
    Mc = calcChirpMass(m1, m2)
    return 5 * (f*np.pi)**(-8/3) * (Mc*const.G/const.c**3)**(-5/3) / 256

def calcPhi(Mc, tau, Phi0):
    return -2 * tau**(5/8) * (5*const.G*Mc/const.c**3)**(-5/8) + Phi0

def hPlus(t, m1, m2, r, i, f, Phi0):
    Mc = calcChirpMass(m1, m2)
    tCoal = calcTcoal(m1, m2, f)
    tau = tCoal - t
    Phi = calcPhi(Mc, tau, Phi0)

    return (Mc*const.G/const.c**2)**(5/4) * (5/(const.c * tau))**(1/4) * \
        np.cos(Phi) * (1 + (np.cos(i))**2) / (2*r*const.parsec*10**6)

def hCross(t, m1, m2, r, i, f, Phi0):
    Mc = calcChirpMass(m1, m2)
    tCoal = calcTcoal(m1, m2, f)
    tau = tCoal - t
    Phi = calcPhi(Mc, tau, Phi0)

    return (Mc*const.G/const.c**2)**(5/4) * (5/(const.c * tau))**(1/4) * \
        np.sin(Phi) * np.cos(i) / (r*const.parsec*10**6)

def hMax(m1, m2, r, i, f, Phi0):
    Mc = calcChirpMass(m1, m2)
    tCoal = calcTcoal(m1, m2, f)
    tau = 0.0001
    Phi = calcPhi(Mc, tau, Phi0)

    return 2 * (Mc*const.G/const.c**2)**(5/4) * (5/(const.c * tau))**(1/4) * \
        np.cos(Phi) * (1 + (np.cos(i))**2) / (2*r*const.parsec*10**6)

def tDomain(m1, m2, f):
    Mc = calcChirpMass(m1, m2)
    tCoal = calcTcoal(m1, m2, f)
    t = np.linspace(-tCoal, tCoal, 10000*tCoal)
    return t
