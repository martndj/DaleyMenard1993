import numpy as np 
import matplotlib.pyplot as plt
from DM93 import Grid, Uncorrelated, Foar, Soar, Gaussian

#====================================================================
#===| setup and configuration |======================================

# -- units of space: m 
km = 1000.

# -- discretization
a = 2500.*km
L = 2.*np.pi * a
N = 100
grid = Grid(N, L)

Lc = a/4.


corrModels = {  'uncorrelated' : Uncorrelated(grid),
                'foar' : Foar(grid, Lc),
                'soar' : Soar(grid, Lc),
                'gaussian' : Gaussian(grid, Lc),
                }

# -- generating random realizations of correlated signal

realizations = dict()
realPowSpec = dict()
for label, cm in corrModels.iteritems():
    realizations[label] = cm.random()
    powSpec = grid.transform(realizations[label])[grid.N:]**2
    # normalization 
    realPowSpec[label] = powSpec/(powSpec[0] + 2.*sum(powSpec[1:]))
    del powSpec

#====================================================================
#===| plots |========================================================

# -- correlation models and spectra

fig1 = plt.figure(figsize=(8,8))
fig1.subplots_adjust(hspace=0.6)
for label, cm in corrModels.iteritems():
    axGrid = plt.subplot(311)
    axSpTh = plt.subplot(312)
    axSpNu = plt.subplot(313)
    axGrid.plot(grid.x, cm.corrFunc(), label=label)
    axSpTh.plot(grid.halfK, cm.powSpecTh(), label=label)

    axSpNu.plot(grid.halfK, cm.powSpecNum(), label=label)

axGrid.set_title('Correlation $L_c=%.0f$ km'%(Lc/km))

xticklabels, xticks = grid.ticks(5, units=km)[:2]
axGrid.set_xticks(xticks)
axGrid.set_xticklabels(xticklabels)
axGrid.set_xlabel('distance [km]')

axSpTh.set_title('Normalized theoretical power spectrum')
axSpTh.set_xlabel('wavenumber $k$')

axSpNu.set_title('Normalized numerical power spectrum')
axSpNu.set_xlabel('wavenumber $k$')

axSpNu.legend(loc='best')

# -- realizations
fig2 = plt.figure()
axGd = plt.subplot(211)
axSp = plt.subplot(212) 
for label in corrModels.iterkeys():
    axGd.plot(grid.x, realizations[label], label=label)
    axSp.plot(grid.halfK, realPowSpec[label], label=label) 
    
axGd.set_title('Correlated signal realization')
axGd.set_xlabel('$x$ [km]')
axGd.set_xticks(xticks)
axGd.set_xticklabels(xticklabels)

axSp.set_title('Normalized power spectrum')
axSp.set_xlabel('wavenumber $k$')
axSp.legend(loc='best')


plt.show()
