import startVTDSimulation_SimoneDario
import copy 
import algoritmoGenetico
import buildDriverVariabile
from NormalizzaDati import TimeSimNormalizzato, LaneOffsetNormalizzato
from ClasseDriver import driver
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
from src.utils import DRIVER_PARAMS_LABEL_TO_NAME, read_configurations, configure_loggers, make_output_folders, copy_files
from ClasseDriver import driver2
import datetime
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
import SelectFromCSV

if __name__ == '__main__': #tipico codice all`inizio dello script, infatti ci permette di dire che il file verra eseguito solo se il modulo viene eseguito direttamente come script e non quando viene importato da un altro script. __name__ variabile predefinita che contiene il nome del modulo
    #"os" libreria che permette di interagire con il sistema operativo
    startProgram = datetime.datetime.now() #prendo il tempo di inizio simulazione 
    i=0 #definisco contatore
    print('\nSTANDARD SIMULATION\n')
    listaValori = []
    algoritmoGenetico.generaValoriDefaultDriver(listaValori)
    print("Generating Value list for Default Driver -> " + str(listaValori))
    print("Build DefaultDriver and Apply to file json...")
    driverParent = driver2.Driver(listaValori) #costruisco il mio driver 
    buildDriverVariabile.buildDriverJSON(listaValori) #applico la configurazione al json 
    timeSim, MediaLaneOffset  = startVTDSimulation_SimoneDario.scriptVTD(i) #dovrei passargli come parametro la configurazione del driver
    driverParent.setTimePath(timeSim)
    driverParent.setLaneOffset(MediaLaneOffset)
    print(timeSim, MediaLaneOffset)
    #print("Lista geni driver " + str(i) + ":", defaultDriver.listaGeni, "\n", "Lane Offset driver " + str(i) + ":", defaultDriver.LaneOffset,"\n", "TimeSim driver " + str(i) + ":", defaultDriver.timePath)
    i = i + 1

    while (i<5): #cosa metto in questo while
        print('\nSIMULATION NUMBER ' + str(i))
        print('\n')
        ffParent = algoritmoGenetico.FitnessFunction(driverParent.timePath, driverParent.LaneOffset, i+1)
        #print(driverParent.listaGeni) #da qui in poi c'e' l'errore
        listaValoriOffspring = copy.deepcopy(listaValori)
        algoritmoGenetico.mutaGene(listaValoriOffspring) #qui ci sara il controllo per capire se i dati che ho prelevato posso andare bene 
        print("Generating Value list -> " + str(listaValoriOffspring))
        print("Build Driver and Apply to file json...")
        #driverOffspring = copy.deepcopy(driverParent)
        driverOffspring = driver2.Driver(listaValoriOffspring) # costruisco il driver perche poi vado a settargli timePath e LaneOffset
        buildDriverVariabile.buildDriverJSON(listaValoriOffspring) # applico al file json 

        #print(driverParent.listaGeni)

        print("Starting VTD Script")
        timeSim, MediaLaneOffset = startVTDSimulation_SimoneDario.scriptVTD(i) #dovrei passargli come parametro la configurazione del driver

        print("Tempo Simulazione: " + str(timeSim),"Media Lane Offset: " + str(MediaLaneOffset))

        driverOffspring.setTimePath(timeSim) #setto le variabili d'istanza del driver
        driverOffspring.setLaneOffset(MediaLaneOffset) #setto le variabili d'istanza del driver
        ffOffspring = algoritmoGenetico.FitnessFunction(timeSim, MediaLaneOffset, i)
        print("FF Parent: " + str(ffParent), "FF Offspring: " + str(ffOffspring))
        if algoritmoGenetico.sopravvivenzaDriver(ffParent, ffOffspring) == 1:
                
                print("SOPRAVVIVE PARENT")
                print("Lista geni Parent" + str(driverParent.listaGeni))
                listaValori = listaValoriOffspring
        else:
                print("SOPRAVVIVE OFFSPRING")
                print("Lista geni Offspring" + str(driverOffspring.listaGeni))
                driverParent.listaGeni = driverOffspring.listaGeni
                driverParent.timePath = driverOffspring.timePath
                driverParent.LaneOffset = driverOffspring.LaneOffset
                listaValori = listaValoriOffspring

        ##print("Lista geni driver " + str(i) + ":", x.listaGeni, "\n", "Lane Offset driver " + str(i) + ":", x.LaneOffset,"\n", "TimeSim driver " + str(i) + ":", x.timePath)
        i = i + 1

print("Hai trovato il tuo driver finale: ")
#print(x.listaGeni)
#print(x.timePath, x.LaneOffset)

print("\nPlotting Graphs...")
TimeSimNormalizzato.doGrafico(i)
LaneOffsetNormalizzato.doGrafico(i)

duration = datetime.datetime.now() - startProgram
print('\n\nTempo totale programma -> ' + "{:.2f}".format(duration.total_seconds()/60) + 'min')
print("\nMAIN TERMINATO")

