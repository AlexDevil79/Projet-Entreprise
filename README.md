# Projet Entreprise

Ce code a pour but d'implémenter et de tester des fonctions appelées marquants 
sur des données étiquetées par type de modulation.

## Protocoles d'utilisation

### Ajout de marquants

- Ajouter le code de calcul du(des) marquant(s) dans *codeMarquant.py*
- Ajouter le nom du(des) marquant(s)
ajouté(s) à la liste de la fonction `allFunctions()` de *parser_1.py*

### Utilisation des tests

Python 3 est requis pour lancer les tests.

Modules Python requis :
- numpy
- scipy
- matplotlib

Pour installer l'un de ces modules, se référer à leur documentation respective.

Mode d'emploi :
- Ouvrir un terminal
- Se placer dans le dossier principal
- Exécuter *mainTest.py* avec python
- ajouter *-h* pour voir les paramètres possibles (données à utiliser, marquants à tester, types de modulation à comparer)

Exemple : 
```
...\Projet commande entreprise\projet_entreprise> python mainTest.py -d base_sans_residu -m moments1_10 -c AM FM
```
lance des tests pour le marquant *moments1_10* sur les classes de modulation *AM* et *FM*, en supposant que le dossier *base_sans_residu* contenant les données se trouve dans *Projet commande entreprise*.

Pour l'analyse des résultats : si pour chaque colonne la case la plus claire correspond à la diagonale, le test est positif. Les marquants utilisés peuvent permettre de distinguer les familles employées. Sinon, soit la manière de tester est insuffisante, soit les marquants ne permettent pas de distinguer les familles en question.

## Informations concernant le dataset

- Dataset stocké en local, à configurer soit dans le default de l'argument *--data*/*-d* du fichier *parser.py*, soit à entrer lors de chaque test
- Stockage de tous les informations sur les signaux dans le fichier *data.JSON*

## Détails sur le stockage des données

### Structure du fichier *data.JSON*

- data = {classe1 : [signal1, signal2, ...],
          classe2 : [signal1, signal2, ...],
          ...}

  - familles : {Phonie_AM : [AM], 
                Surmodulation_AM : [AM_FSK, AM_PSK],
                ASK : [ASK4],
                Phonie_FM : [FM],
                Surmodulation_FM : [FM_FSK, FM_PSK], 
                FSK : [FSK2, FSK4, GFSK2, GFSK4], 
                OFDM : [OFDM], 
                PSK : [PI2DPSK2, PI4DPSK4, PSK2, PSK4],
                QAM : [QAM16, QAM32, QAM64]}

  - signal = {"file_adress" : cheminRelatifSignalWAV, info1 : ..., info2 : ..., ...} ouvert sous format I + j*Q
    - info modulation analogique : type_cible, type_mod, duree_s, rsb_dB, bw_Hz, indice, fc_Hz, fe_Hz, p_brt_dB_Hz
    - info modulation numérique : type_cible, type_mod , ordre_mod, duree_s, duree_symb, rsb_dB, debit_bd, bw_Hz, fc_Hz, sps, roll_off, p_brt_dB_Hz

  avec :
  - debit_bd = bande_wd/(1+roll_off) : débit en baud
  - duree_s = duree_symb/debit_bd

En réalité, seule fe est connue et sera à utiliser (ou la durée du signal)

### Structure du fichier *rsb_data.JSON*

- rsb_data = {rsb_n1 : data1,
              rsb_n2 : data2,
              ...}

## Détails sur *codeMarquant.py*
Contient toutes les fonctions implémentant les marquants

## Détails sur *dataset.py*
Contient toutes les fonctions utiles pour la gestion des données

## Détails sur *parser_1.py*
Gère les arguments entrés dans le terminal lors de l'exécution de *mainTest.py*

## Détails sur *testMarquant.py*
Fichier utilisé pour tester la bonne implémentation du calcul des marquants

## Détails sur *optimizeMarquant.py*
Fichier utilisé pour optimiser les marquants phase, amplitude et fréquence Instantanée.

## Détails sur *generationDictionnaire.py*
Fichier utilisé pour générer les JSON