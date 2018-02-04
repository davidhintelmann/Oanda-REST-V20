import numpy as np
import matplotlib.pyplot as plt
import NormCur as nc
import OHLC as oc
import GrabAll as ga

ieu, Ceu, iej, Cej, iea, Cea, iec, Cec, tickseu = ga.GrabAllCandles()

normEU = nc.NormCur(Ceu, Cej)
normEA = nc.NormCur(Ceu, Cea)

plt.figure(1)
plt.plot(Ceu)
plt.plot(normEU)
plt.plot(normEA)

plt.show()
