import startVTDSimulation_SimoneDario
import logging
import algorimoGenetico
import buildDriverVariabile
from ClasseDriver import driver
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
from src.utils import DRIVER_PARAMS_LABEL_TO_NAME, read_configurations, configure_loggers, make_output_folders, copy_files
from ClasseDriver import driver2
import subprocess, logging, os, time, datetime, shutil, random, string, sys, glob
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
import SelectFromCSV

if __name__ == '__main__': #tipico codice all`inizio dello script, infatti ci permette di dire che il file verra eseguito solo se il modulo viene eseguito direttamente come script e non quando viene importato da un altro script. __name__ variabile predefinita che contiene il nome del modulo
    #"os" libreria che permette di interagire con il sistema operativo
    i=0 #definisco contatore
    print('STANDARD SIMULATION\n')
    listaValori = []
    algorimoGenetico.generaValoriDefaultDriver(listaValori)
    print("Generating Value list for Default Driver -> " + str(listaValori))
    print("Build DefaultDriver and Apply to file json...")
    defaultDriver = driver2.Driver(listaValori) #costruisco il mio driver 
    buildDriverVariabile.buildDriver(listaValori) #applico la configurazione al json 
    coppiaValori = startVTDSimulation_SimoneDario.scriptVTD(i) #dovrei passargli come parametro la configurazione del driver
    timeSim, MediaLaneOffset = coppiaValori
    defaultDriver.setTimePath(timeSim)
    defaultDriver.setLaneOffset(MediaLaneOffset)
    x = defaultDriver
    #print("Lista geni driver " + str(i) + ":", defaultDriver.listaGeni, "\n", "Lane Offset driver " + str(i) + ":", defaultDriver.LaneOffset,"\n", "TimeSim driver " + str(i) + ":", defaultDriver.timePath)
    i = i + 1

    while (i<3):
        print('\nSIMULATION NUMBER ' + str(i))
        print('\n')
        driverParent = x
        ffParent = algorimoGenetico.FitnessFunction(driverParent.timePath, driverParent.LaneOffset)
        algorimoGenetico.mutaGene(listaValori) #qui ci sara il controllo per capire se i dati che ho prelevato posso andare bene 
        print("Generating Value list -> " + str(listaValori))
        print("Build Driver and Apply to file json...")
        driverOffspring = driver2.Driver(listaValori) # costruisco il driver perche poi vado a settargli timePath e LaneOffset
        buildDriverVariabile.buildDriver(listaValori) # applico al file json 

        print("Starting VTD Script")
        coppiaValori = startVTDSimulation_SimoneDario.scriptVTD(i) #dovrei passargli come parametro la configurazione del driver
        timeSim, MediaLaneOffset = coppiaValori
        
        driverOffspring.setTimePath(timeSim) #setto le variabili d'istanza del driver
        driverOffspring.setLaneOffset(MediaLaneOffset) #setto le variabili d'istanza del driver
        ffOffspring = algorimoGenetico.FitnessFunction(timeSim, MediaLaneOffset)
        print(ffParent, ffOffspring)
        if algorimoGenetico.sopravvivenzaDriver(ffParent, ffOffspring) == 1:
                x = driverParent #tengo il parent
        else:
                x = driverOffspring #tengo l'offspring 

        print("Lista geni driver " + str(i) + ":", x.listaGeni, "\n", "Lane Offset driver " + str(i) + ":", x.LaneOffset,"\n", "TimeSim driver " + str(i) + ":", x.timePath)
        i = i + 1

print("Hai trovato il tuo driver finale!")
print("\nMAIN TERMINATO")