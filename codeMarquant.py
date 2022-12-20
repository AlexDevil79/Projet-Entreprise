import dataset
import numpy as np
import numpy.fft as fft
import scipy.signal as sgn
import scipy.stats as stat
import matplotlib.pyplot as plt
from itertools import chain
### Calcul des marquants ###
# Signal = {"file_adress" : cheminRelatifSignalWAV, info1 : ..., info2 : ..., ...} ouvert sous format I + j*Q
# Marquant = fonction : signal -> liste de scalaires

# scalars : 
alphaPhase = 0.1
binsPhase = 13
betaPhase = 0.078070918215571

alphaAmp = 0.9
binsAmp = 82
betaAmp = 0.05702412979475391

alphaFreq = 0.20714285714285713
binsFreq = 19
betaFreq = 0.21917998669297095

# méthodes pour le calcul des cumulants
def calcMoment2(sig,n):
    absol = np.abs(sig)
    if np.min(absol) == 0:
        sig = np.zeros(10)
    else:
        sig = sig/absol
    return stat.moment(sig,n)

def calcMoment(sig, n, q):
    """ 
        retourne 1/N [Σ(s^(n-q))*conj(s^q)]
    
        Args: 
            -sig : le liste à 2 colonnes (I,Q)
            -n : l'ordre du moment
            -q : le nombre de conjugaison
    """
    # Centering and normalization
    sig = sig-np.mean(sig)
    absol = np.abs(sig)
    if np.min(absol) == 0:
        sig = np.zeros(10)
    else:
        sig = sig/absol
    conjSq=np.conj(sig**q)
    return np.sum(conjSq*sig**(n-q))/len(sig)

#Les cumulant avec conjugaison
def C41(signal):
    sig = dataset.openSignal(signal["file_adress"])
    return calcMoment2(sig,4)-3*calcMoment2(sig,3)*calcMoment(sig, 2,1)
    
def C42(signal):
    sig = dataset.openSignal(signal["file_adress"])
    return calcMoment(sig, 4,2)-np.abs(calcMoment2(sig,2))**2-2*calcMoment(sig,2,1)**2

def C61(signal):
    sig = dataset.openSignal(signal["file_adress"])
    return calcMoment(sig, 6,1)-5*calcMoment(sig,2,1)*calcMoment2(sig,4)-10*calcMoment2(sig,2)*calcMoment(sig,4,1)+30*calcMoment2(sig,2)*calcMoment(sig,2,1)

def C62(signal):
    sig = dataset.openSignal(signal["file_adress"])
    return calcMoment(sig, 6,2)-6*calcMoment2(sig,2)*calcMoment(sig,4,2)-8*calcMoment(sig,2,1)*calcMoment(sig,4,1)-calcMoment(sig,2,2)*calcMoment2(sig,4)+6*calcMoment2(sig,2)**2*calcMoment(sig,2,2)+24*calcMoment(sig,2,1)**2*calcMoment2(sig,2)

def C63(signal):
    sig = dataset.openSignal(signal["file_adress"])
    return calcMoment(sig, 6,3)-9*calcMoment(sig,2,1)*calcMoment(sig,4,2)+12*calcMoment(sig,2,1)**3-3*calcMoment(sig,2,0)*calcMoment(sig,4,3)-3*calcMoment(sig,2,2)*calcMoment(sig,4,1)+18*calcMoment(sig,2,0)*calcMoment(sig,2,1)*calcMoment(sig,2,2)

def LCPLX_Cumul(signal,n=8):
    sig = dataset.openSignal(signal["file_adress"])
    C=np.zeros(n, dtype=complex)
    C[0]=calcMoment2(sig,1)
    for idx in range(1,n+1):
        somme=0
        for idx2 in range(1,idx):
            somme+=C[idx2-1]*calcMoment2(sig,idx-idx2)*np.math.factorial(idx-1)/((np.math.factorial(idx2-1))*(np.math.factorial(idx-idx2)))
        C[idx-1]=calcMoment2(sig,idx)-somme
    #return np.abs(C[-1])**(2/n)
    return C[-1]

def cumulants(signal, n=4, q=2):
    sig = dataset.openSignal(signal["file_adress"])

    def compter_elements_communs(liste1, liste2):
        compteur = 0
        for element in liste1:
            if element in liste2:
                compteur += 1
        return compteur
    def get_partitions(collection):
        if len(collection) == 1:
            yield [collection]
            return

        first = collection[0]
        for smaller in get_partitions(collection[1:]):
            # insert `first` in each of the subpartition's subsets
            for n, subset in enumerate(smaller):
                 yield smaller[:n] + [[first] + subset] + smaller[n+1:]
            # put `first` in its own subset
            yield [[first]] + smaller

    Pns = list(get_partitions(list(range(1,n+1))))
    C=[]    
    for l in range(len(Pns)):
        I=Pns[l]
        p=len(I)
        prdt=np.zeros(p, dtype=complex)
        
        for k in range(p):
            q_j = compter_elements_communs(list(range(1,q+1)),I[k])
            prdt = calcMoment(sig,len(I[k]), q_j)
            
        prdt=((-1)**(p-1))*np.math.factorial(p-1)*np.prod(prdt)
        C.append(prdt)
    return np.sum(C)

def max_DSP(signal):
    sig = dataset.openSignal(signal["file_adress"])
    sig = sig*np.sum(np.abs(sig))/len(sig)-1
    return np.max(np.abs(fft.fft(sig))**2)/len(sig)

def std_phase(signal):
    seuil = 0.5    
    sig = dataset.openSignal(signal["file_adress"])
    sig = sig*np.sum(np.abs(sig))/len(sig)-1    
    Phi = np.angle([z for z in sig if np.abs(z)>seuil])
    return np.std(Phi)

def std_phase2(signal):
    seuil = 0.5    
    sig = dataset.openSignal(signal["file_adress"])
    sig = sig*np.sum(np.abs(sig))/len(sig)-1    
    Phi = np.angle([z for z in sig if np.abs(z)>seuil])
    return np.sqrt(np.abs((np.sum(Phi**2)-(np.sum(Phi))**2)/len(Phi)))

# méthode pour les méthodes 'xxxInstantanee'
def count(x, mode, alpha = alphaPhase, bins = binsPhase, beta = betaPhase):
    # on calcule l'histogramme y de x
    h, values = np.histogram(x, bins=bins)
    # récupère les maximums locaux de y, sous condition qu'ils soient supérieurs à ymax*alpha
    hmax = h.max()
    if mode == 'clip':
        extremas = sgn.argrelextrema(np.concatenate((np.zeros(2),h,np.zeros(2))), np.greater, order = int(bins*beta), mode = mode)[0]-2
    else:
        extremas = sgn.argrelextrema(h, np.greater, order = int(bins*beta), mode = mode)
    hMaxLocaux = h[extremas]
    hMaxLocaux = hMaxLocaux[np.where(hMaxLocaux>=hmax*alpha)]
    #plt.clf();plt.plot(values[:-1], h);plt.show()
    return [len(hMaxLocaux)]

def frequenceInstantanee(signal, alpha = alphaFreq, bins = binsFreq, beta = betaFreq):
    # calcul la fréquence instantané   
    lenMax = 10**6 #longueur maximale du signal, pour éviter le crash de VS Code
    s = np.complex64(dataset.openSignal(signal["file_adress"])) # ouverture du signal par son adresse
    fe = int(len(s)/float(signal["duree_s"])) # fréquence d'échantillonnage du signal pour le spectrogramme
    if len(s) > lenMax:
        s = s[:int(lenMax)]
    try:
        Spec, fs, bin, im = plt.specgram(s, NFFT=1024, Fs=fe, noverlap=900, scale='linear', mode='psd')
        plt.clf()
    except:
        print("Erreur taille array : len(s) = {}.".format(len(s)))
        Spec = np.zeros((10,10))
        fs = np.arange(10)
    # On calcule la fréquence max pour chaque temps
    n = len(Spec[0])
    Sxx = np.zeros(n)
    for i in range(n):
        Sxx[i] = abs(float(fs[np.argmax(Spec[:,i])]))
    return count(Sxx,'wrap', alpha, bins, beta)

def phaseInstantanee(signal, alpha = alphaPhase, bins = binsPhase, beta = betaPhase):
    # calcul la phase instantané
    s = dataset.openSignal(signal["file_adress"]) # ouverture du signal par son adresse
    phase = np.arctan2(s.imag,s.real)# func de phase
    return count(phase, 'wrap', alpha, bins, beta)

def amplitudeInstantanee(signal, alpha = alphaAmp, bins = binsAmp, beta = betaAmp):
    # calcul l'amplitude instantané
    s = dataset.openSignal(signal["file_adress"]) # ouverture du signal par son adresse
    amp = np.abs(s)# func d'amplitude
    return count(amp, 'clip', alpha, bins, beta)

def largeurDeBande(signal):
    # calcul largeur de bande à 3 dB
    s = dataset.openSignal(signal["file_adress"])
    SdB = 10*np.log10(np.abs(fft.fft(s))[:len(s)//2])
    max3dB = np.max(SdB)-10*np.log10(2)
    bande = []
    df = 1/float(signal["duree_s"])
    f = 0
    for x in SdB:
        if x > max3dB:
            bande.append(f)
        f += df
    return [np.abs(bande[-1]-bande[0])]

def test():
    data = dataset.jsonToDict()['AM']
    for s in data:
        C41(s)
