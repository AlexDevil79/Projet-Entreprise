import matplotlib.pyplot as plt
import numpy as np
import codeMarquant as marquant
import parser_1, dataset

def processFunctions():

    '''
    Calcule les marquants sur des échantillons aléatoires des classes demandées

    fonctions : liste de fonctions de type   dict -> list[float]   ou   dict -> float
        renvoyant les marquants calculés pour un échantillon en entrée
        le dictionnaire d'entrée doit être de la forme : {"signal" : str #adresse, "fe" : str #Hz}
    classes : liste[str] des noms des classes de modulation sur lesquelles on veut tester les marquants
    
    return :    result : [ family : [ sample : [scalaire : float] ] ]
    '''
    
    dataAdresses = dataset.getAdresses(args.classes, args.rsb)
    result = []

    # calcul du nombre d'échantillons minimal des familles concernées
    # (on évite de calculer sur plus d'échantillons que nécessaire)
    lengths = [len(dataAdresses[family]) for family in args.classes]
    n = min(lengths)


    for family in args.classes:

        resultsFamily = []
        indexes = np.linspace(0,len(dataAdresses[family])-1,n,dtype=int)
        for i in range(n):
            sample = dataAdresses[family][indexes[i]]
            print(f"{family}, échantillon {i} sur {n}",end='\r')

            # liste des résultats scalaires du calcul sur un échantillon
            resultsSample = []

            for f in args.marquants:
                f = getattr(marquant, f)
                resultsFunction = f(sample)
                try :
                    for res in resultsFunction:
                        resultsSample.append(res)
                except TypeError :
                    resultsSample.append(resultsFunction)
            
            resultsFamily.append(resultsSample)
        print(f"{family}, {n} échantillons calculés")
        
        result.append(resultsFamily)
    return result

def analyseResults(processedSamples):
    '''
    Fait une classification rapide en calculant le point moyen par classe
    puis en attribuant chaque point à la classe de point moyen le plus proche
    Retourne la matrice de confusion sur cette classification
    '''
    if args.familles == None or len(args.familles) == 1:
        nClasses = len(processedSamples)
        confusion = np.zeros((nClasses,nClasses))

        meanPoints = []
        for classResults in processedSamples:
            meanPoint = np.mean(np.array(classResults),axis=0)
            meanPoints.append(meanPoint)

        for classId,classResults in enumerate(processedSamples):
            for sampleResult in classResults:
                classAttribution = np.argmin(np.array([np.sum(np.abs(sampleResult-p)) for p in meanPoints]))
                confusion[classId,classAttribution] += 1
    else:
        nFamilles = len(args.familles)
        confusion = np.zeros((nFamilles,nFamilles))

        meanPoints = []
        for idFamille,famille in enumerate(args.familles):
            meanPoint = np.mean(np.array(processedSamples[0]),axis=0)*0
            for idClass,classResults in enumerate(processedSamples):
                if args.classes[idClass] in parser_1.allFamilies()[famille]:
                    meanPoint += np.mean(np.array(classResults),axis=0)
            meanPoint = meanPoint/len(parser_1.allFamilies()[famille])
            meanPoints.append(meanPoint)

        for classId,classResults in enumerate(processedSamples):
            familyId = 0
            for idFamille,famille in enumerate(args.familles):
                if args.classes[classId] in parser_1.allFamilies()[famille]:
                    familyId = idFamille
            for sampleResult in classResults:
                familyAttribution = np.argmin(np.array([np.sum(np.abs(sampleResult-p)) for p in meanPoints]))
                confusion[familyId,familyAttribution] += 1
    return confusion

def displayAnalysis(analysedResults):
    '''
    Affiche la matrice de confusion donnée en entrée
    '''
    plt.close()
    print(analysedResults)
    if args.familles == None or len(args.familles) == 1:
        labels = args.classes
    else:
        labels = args.familles
        # Normalisation en %
        for i in range(analysedResults.shape[0]):
            analysedResults[i,:] = (100/np.sum(analysedResults[i,:]))*analysedResults[i,:]

    fig,ax=plt.subplots()
    ax.matshow(analysedResults, cmap='gray', vmin=0, vmax=analysedResults.max())
    ax.yaxis.tick_right()
    ax.set_ylabel("Classe réelle")
    ax.set_yticks(range(len(labels)),labels)
    ax.set_xlabel("Classe attribuée")
    ax.set_xticks(range(len(labels)),labels,rotation='vertical')
    ax.set_title(", ".join(args.marquants))
    fig.tight_layout()
    if args.save:
        plt.savefig("matrices de confusion\\latestConfusionMatrix.jpg")
        plt.savefig(f"matrices de confusion\\#m {'&'.join(args.marquants)} #c_or_f {'&'.join(labels)} #rsbmin{args.rsb}")
        plt.close()
    else:
        plt.show()

args = parser_1.getArgs()

if args.rsb > 0:
    print("rsb :",args.rsb)

print("marquants :",*(args.marquants))
try:
    assert(args.familles!=None)
    print("familles de classes de modulation :",end='')
    for f in args.familles:
        print(f" {f} ({' '.join(parser_1.allFamilies()[f])}",end=') ')
    print()
except AssertionError:
    print("classes de modulation :",*(args.classes))


### Main
displayAnalysis(analyseResults(processFunctions()))