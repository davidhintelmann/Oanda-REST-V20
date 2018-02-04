import numpy as np

def NormCur(BCn, BCs):
    aveBCn = np.mean(BCn)
    aveBCs = np.mean(BCs)
    if aveBCn < aveBCs:
        scaled = aveBCs/aveBCn
        normalizedCurrency = np.round(BCs/scaled,5)
        return normalizedCurrency
    elif aveBCn > aveBCs:
        scaled = aveBCn/aveBCs
        normalizedCurrency = np.round(BCs/scaled,5)
        return normalizedCurrency
    else:
        print('Error: did not compute NormCur func. Normalizing issue?')
