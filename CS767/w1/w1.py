import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt

def MB_speed(v,m,T):
    """ Maxwell-Boltzmann speed distribution for speeds """
    kB = 1.38e-23
    return (m/(2*np.pi*kB*T))**1.5 * 4*np.pi * v**2 * np.exp(-m*v**2/(2*kB*T))

fig = plt.figure()
ax = fig.add_subplot(111)
v = np.arange(0,800,1)
amu = 1.66e-27
mass = 85*amu
for T in [100,200,300]:
    fv = MB_speed(v,mass,T)
    ax.plot(v,fv,label='T='+str(T)+' K',lw=2)
ax.legend(loc=0)
ax.set_xlabel('$v$ (m/s)')
ax.set_ylabel('PDF, $f_v(v)$')
plt.savefig('Boltzmann.png', dpi=300)
plt.plot()
plt.show()