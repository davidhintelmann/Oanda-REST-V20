import numpy as np
import matplotlib.pyplot as plt
import NormCur as nc
import OHLC as oc
import GrabAll as ga

ieu, Ceu, iej, Cej, iea, Cea, iec, Cec, tickseu = ga.GrabAllCandles()

ticks = np.arange(tickseu)
normEJ = nc.NormCur(Ceu, Cej)
normEA = nc.NormCur(Ceu, Cea)
normEC = nc.NormCur(Ceu, Cec)

plt.subplot(2,1,1)
plt.plot(Ceu,'b')

plt.plot(normEJ,'k')
plt.plot(normEA,'g')
plt.plot(normEC,'r')

#plt.ylim(1.198,1.22)

plt.subplot(2,1,2)
plt.plot(normEJ-normEC)
plt.plot(normEJ-normEA,'g')
plt.plot(normEJ-Ceu,'b')

plt.show()
