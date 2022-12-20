from scipy.io import wavfile
import json
from parser_1 import getArgs
args = getArgs()

def jsonToDict(classSignal = '', rsb = False):
    ## importe les données stoquées dans data.json
    ## possibilité d'importer seulement une classe de signaux
    if rsb:
        chemin = 'data\\rsb_data.json'
    else:
        chemin = 'data\\data.json'
    with open(chemin) as dataBase:
        data = json.load(dataBase)
    if classSignal != '':
        return data[classSignal]
    return data

def openSignal(adressRelative):
    # rentrer chemin jusqu'au dossier
    adress = args.data
    adress += adressRelative
    # s = [[I0, Q0], [I1, Q1], ...]
    # signal = I + j*Q
    s = wavfile.read(adress)[1]
    return s[:,0] + 1j*s[:,1]

def getAdresses(classes, rsb = 0):
    if int(rsb) > 0:
        chemin = 'data\\rsb_data.json'
        str_rsb = 'rsb_'+str(rsb)
        with open(chemin) as dataBase:
            data = json.load(dataBase)[str_rsb]
    else:
        chemin = 'data\\data.json'
        with open(chemin) as dataBase:
            data = json.load(dataBase)
    return {k : data[k] for k in classes if k in data}
