import numpy as np
from collections import defaultdict

from codeMarquant import *

# test si les marquants ont bien été implémentés
data = dataset.jsonToDict()

allClass2 = {'amplitude' : ['AM', 'AM_FSK', 'AM_PSK', 'QAM16', 'QAM32', 'QAM64', 'ASK4'],
            'fréquence' : ['FM', 'AM_FSK', 'FM_FSK', 'FM_PSK', 'FSK2', 'FSK4', 'GFSK2', 'GFSK4'],
            'phase' : ['PI2DPSK2', 'PI4DPSK4', 'FM_PSK', 'AM_PSK', 'PSK2', 'PSK4', 'QAM16', 'QAM32', 'QAM64']}

allClass = {'amplitude' : ['QAM16', 'QAM32', 'QAM64'],
            'fréquence' : ['AM_FSK', 'FM_FSK', 'FM_PSK', 'FSK2', 'FSK4', 'GFSK2', 'GFSK4'],
            'phase' : ['PSK2', 'PI2DPSK2', 'PI4DPSK4', 'PSK4', 'QAM16', 'QAM32', 'QAM64']}

ampCounter = {1 : ['AM', 'AM_FSK', 'AM_PSK'],
              2 : ['QAM16', 'QAM32', 'QAM64'],
              3 : ['ASK4']}

phaseCounter = {2 : ['PSK2', 'PI2DPSK2', 'PI4DPSK4'], 
                3 : ['PSK4', 'QAM16', 'QAM32', 'QAM64']}

frecCounter = {1 : ['FM', 'AM_FSK', 'FM_FSK', 'FM_PSK'],
               2 : ['GFSK2', 'FSK2','GFSK4', 'FSK4']}

def precisionComptage(classe, thing, alpha = 0.5, bins = 10, beta = 0.1):
    things = {'amplitude' : (amplitudeInstantanee, ampCounter),
            'fréquence' : (frequenceInstantanee, frecCounter),
            'phase' : (phaseInstantanee, phaseCounter)}
    fonction, counter = things[thing]
    l = []
    N = np.linspace(0,len(data[classe])-1, 100)
    for i in N:
        s = data[classe][int(i)]
        l.append(fonction(s, alpha, bins, beta)[0])
    d = defaultdict(int)
    for x in l:
        d[x] += 1
    n = -1
    for x in counter.keys():
        if classe in counter[x]:
            n = x
            pass
    return d[n]/sum(d.values())

def optimize(thing, pts):
    print("Optimisation de :", thing)
    A = np.linspace(0.01,0.5, pts)
    B = 10**(np.linspace(np.log10(0.05),np.log10(0.45), pts))
    Bi = np.linspace(8,50,pts)
    alphaOPt = A[0]
    betaOpt = B[0]
    binsOpt = Bi[0]
    m = 0
    classes = allClass[thing]
    print(classes)
    n = len(classes)
    i = 0
    for a in A:
        for b in B:
            for bi in Bi:
                i += 1
                print("Calcul",i,"sur",pts**3,end='\r')
                if b*int(bi) >= 1:
                    o = 0
                    for classe in classes:
                        o += precisionComptage(classe, thing, alpha = a, bins = int(bi), beta = b)**2
                    if o > m:
                        m = o
                        alphaOPt = a
                        betaOpt = b
                        binsOpt = int(bi)
                    
    return alphaOPt, binsOpt, betaOpt, np.sqrt(m/n)

print(optimize('fréquence', 8))
# result : 
# - phase : (0.1, 13, 0.078070918215571, 0.7983107164506812)
#       fsk : (0.1, 18, 0.22407636572582118, 0.7575453781787596)
#       qam (4) : (0.1, 13, 0.08549879733383485, 0.9201449161228175)
# - amplitude : (0.9, 82, 0.05702412979475391, 0.5434545584893526)
#       ask : (0.1, 80, 0.11505991785708991, 0.57)
#       qam16 (2) : (0.1, 83, 0.06947477471865686, 0.5)
#       qam32 (2) : (0.7857142857142857, 81, 0.06947477471865686, 0.51)
#       qam64 (2) : (0.7857142857142857, 81, 0.049999999999999996, 0.51)
# - fréquence : (0.20714285714285713, 19, 0.21917998669297095, 0.41743262929483604)
