
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()

class Driver:
     
    def __init__(self, num_run, lista_parametri):
       self.id_driver = num_run
       self.Lista_parametri = lista_parametri
       self.TimeSim = 0
       self.LaneOffset = None
       self.Fitness_function_totale = -1
       
    def default_driver_generate_value(self):
        lista_parametri = ['0.95'] * 17
        lista_parametri.extend(['1'] * 5)
        return lista_parametri
    
    def build_default_driver(self):
       lista_parametri = self.default_driver_generate_value()
       self.Lista_parametri = lista_parametri
        
    def set_performance(self, timesim, laneoffset):
        self.TimeSim = timesim
        self.LaneOffset = laneoffset
    



