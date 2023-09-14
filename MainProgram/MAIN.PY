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
    i=1 #definisco contatore
    
    listaValori = []
    algorimoGenetico.generaValoriDefaultDriver(listaValori)
    print("Generating Value list for Default Driver -> " + str(listaValori))
    print("Build DefaultDriver and Apply to file json...")
    defaultDriver = driver2.Driver(listaValori) #costruisco il mio driver 
    buildDriverVariabile.buildDriver(listaValori)

    while (i<3):
        print('\nSIMULATION NUMBER ' + str(i))
        print('\n')
        #driver.Driver() #come parametri del costruttore posso dargli li stessi del file json, quindi posso tenere una lista con i valori dei geni e aggiornare sia il json sia l'oggetto
        coppiaValori = startVTDSimulation_SimoneDario.scriptVTD() #dovrei passargli come parametro la configurazione del driver
        timeSim, MediaLaneOffset = coppiaValori
        defaultDriver.setTimePath(timeSim)
        defaultDriver.setLaneOffset(MediaLaneOffset)
        print(defaultDriver.LaneOffset, defaultDriver.listaGeni, defaultDriver.timePath)
        algorimoGenetico.generaValoriDriver(listaValori) #qui ci sara il controllo per capire se i dati che ho prelevato posso andare bene 
        print("Generating Value list -> " + str(listaValori))
        print("Build Driver and Apply to file json...")
        buildDriverVariabile.buildDriver(listaValori)
        i = i + 1

print("\nMAIN TERMINATO")