from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
import json

class Driver:
     
    def __init__(self, lista_parametri):
       self.parameters = lista_parametri
        
    def reset_driver(self):
        self.parameters = None



