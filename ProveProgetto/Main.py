import TimeSimNormalizzato, LaneOffsetNormalizzato
import random 
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
import datetime
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()


if __name__ == '__main__': #tipico codice all`inizio dello script, infatti ci permette di dire che il file verra eseguito solo se il modulo viene eseguito direttamente come script e non quando viene importato da un altro script. __name__ variabile predefinita che contiene il nome del modulo
    #"os" libreria che permette di interagire con il sistema operativo
    startProgram = datetime.datetime.now() #prendo il tempo di inizio simulazione 
    i=1 #definisco contatore
    print('\nSTANDARD SIMULATION\n')
    r1 = round(random.uniform(0,10),2)
    r2 = round(random.uniform(0,10),2)
    ff1N = TimeSimNormalizzato.normalizzaTS(r1,i)
    ff2N = LaneOffsetNormalizzato.normalizzaLO(r2,i)
    i = i + 1

    while (i<=5): #cosa metto in questo while
        print('\nSIMULATION NUMBER ' + str(i))
        print('\n')
        #muto 
        s1 = round(random.uniform(0,10),2)
        s2 = round(random.uniform(0,10),2)
        print('Nuovi valori: ' + str(s1) + '   ' + str(s2))
        ff1N = TimeSimNormalizzato.normalizzaTS(s1,i)
        ff2N = LaneOffsetNormalizzato.normalizzaLO(s2,i)        

        i = i + 1

print("Hai trovato il tuo driver finale")
#print(x.listaGeni)
#print(x.timePath, x.LaneOffset)

print("\nPlotting Graphs...")
TimeSimNormalizzato.doGrafico()
LaneOffsetNormalizzato.doGrafico()

duration = datetime.datetime.now() - startProgram
print('\n\nTempo totale programma -> ' + "{:.2f}".format(duration.total_seconds()/60) + 'min')
print("\nMAIN TERMINATO")

