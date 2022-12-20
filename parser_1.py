import argparse
from os import path

def allFamilies():
    return {'Phonie_AM' : ['AM'], 
            'Surmodulation_AM' : ['AM_FSK', 'AM_PSK'],
            'ASK' : ['ASK4'],
            'Phonie_FM' : ['FM'],
            'Surmodulation_FM' : ['FM_FSK', 'FM_PSK'], 
            'FSK' : ['FSK2', 'FSK4', 'GFSK2', 'GFSK4'], 
            'OFDM' : ['OFDM'], 
            'PSK' : ['PI2DPSK2', 'PI4DPSK4', 'PSK2', 'PSK4'],
            'QAM' : ['QAM16', 'QAM32', 'QAM64']}

def allFunctions():
    return ['C41', 
            'C42', 
            'C61', 
            'C62', 
            'C63', 
            'LCPLX_Cumul', 
            'max_DSP',
            'std_phase',
            'std_phase2',
            'frequenceInstantanee', 
            'phaseInstantanee', 
            'amplitudeInstantanee', 
            'largeurDeBande']

def allClasses():
    return ['AM', 
            'AM_FSK', 
            'AM_PSK', 
            'ASK4', 
            'FM', 
            'FM_FSK',
            'FM_PSK', 
            'FSK2', 
            'FSK4', 
            'GFSK2', 
            'GFSK4', 
            'OFDM', 
            'PI2DPSK2', 
            'PI4DPSK4', 
            'PSK2', 
            'PSK4', 
            'QAM16', 
            'QAM32', 
            'QAM64']

def getArgs():
    """
    This function builds the argument parser
    and returns parsed arguments
    Output : parsed arguments
    """
    
    ## common settings
    parser = argparse.ArgumentParser(description = "Argument parser, to use in a terminal with mainTest.py")

    # data folder
    parser.add_argument("--data","-d",type=str,default="S:\\DataBase\\data",help="Adresse relative du dossier contenant les données, depuis le dossier grand-parent de mainTest")
    # markers used
    parser.add_argument("--marquants","-m",nargs='+',type=str,default=["all"],help="Marquants utilisés")
    # classes used
    parser.add_argument("--classes","-c",nargs='+',type=str,default=["all"],help="Classes de modulation utilisées dans les données")
    # classes used
    parser.add_argument("--familles","-f",nargs='+',type=str,default=None,help="Familles de classes de modulation utilisées dans les données")
    # rsb used
    parser.add_argument("--rsb","-rsb",type=int,default=0,help="RSB minimal de la base de donnée")
    # save result
    parser.add_argument("--save","-s",default=False,action='store_true',help="Force la sauvegarde de la figure")

    args = parser.parse_args()

    if 'all' in args.marquants:
        args.marquants = allFunctions()

    for x in args.marquants:
        try:
            assert(x in allFunctions())
        except AssertionError:
            raise Exception(f"{x} n'est pas un marquant implémenté !\n(ou bien ce marquant n'a pas été ajouté correctement)\n\
les marquants répertoriés sont les suivants :\n\
{' '.join(allFunctions())}")

    if 'all' in args.classes:
        args.classes = allClasses()

    for x in args.classes:
        try:
            assert(x in allClasses())
        except AssertionError:
            raise Exception(f"{x} n'est pas une classe de modulation répertoriée !\n\
les classes répertoriées sont les suivantes :\n\
{' '.join(allClasses())}")
    
    try:
        if 'all' in args.familles:
            args.familles = allFamilies().keys()

        args.classes = []
        for famille in args.familles:
            try:
                assert(famille in allFamilies().keys())
            except AssertionError:
                raise Exception(f"{famille} n'est pas une famille de classes de modulation répertoriée !\n\
les familles répertoriées sont les suivantes :\n\
{' '.join(list(allFamilies().keys()))}")
            for classe in allFamilies()[famille]:
                args.classes.append(classe)
    except TypeError:
        pass

    args.data = path.join(path.curdir,'..',args.data)

    return args
