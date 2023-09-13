import startVTDSimulation_SimoneDario
import logging
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()

if __name__ == '__main__': #tipico codice all`inizio dello script, infatti ci permette di dire che il file verra eseguito solo se il modulo viene eseguito direttamente come script e non quando viene importato da un altro script. __name__ variabile predefinita che contiene il nome del modulo
    #"os" libreria che permette di interagire con il sistema operativo
    #while (i<3):
    #print('Simulation number ' + str(i))
    startVTDSimulation_SimoneDario.scriptVTD()

print("\nMAIN TERMINATO")