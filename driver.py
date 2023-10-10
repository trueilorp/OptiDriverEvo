
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
import normalize

class Driver:

    WIDTHLANE = 3.500 #ho verificato dallo scenario editor 
      
    def __init__(self, lista_parametri):
       self.Lista_parametri = lista_parametri
       self.TimeSim = 0
       self.LaneOffset = None
       self.Fitness_function_totale = -1

    def defaultDriverGenerateValue(self):
        lista_parametri = ['0.50'] * 17
        lista_parametri.extend(['1'] * 5)
        return lista_parametri
    
    def buildDefaultDriver(self):
       lista_parametri = self.defaultDriverGenerateValue()
       self.Lista_parametri = lista_parametri
        
# Metodo per settare le variabili d'istanza 
    def setParameters(self, parameters):
        self.Lista_parametri = parameters

    def setPerformance(self, timesim, laneoffset):
        self.TimeSim = timesim
        self.LaneOffset = laneoffset
    
    def checkFFParent(self, drivers, flag, drivers_def):    
        driver_to_check = drivers[-1]
        driver_parent_to_compare = drivers[-2]
        if flag == 1:
            return True, flag 
        if flag == 0 and driver_to_check.TimeSim != driver_parent_to_compare.TimeSim and driver_to_check.LaneOffset != driver_parent_to_compare.LaneOffset: #caso in cui devo passare alla simulazione successiva
           driver_parent_to_compare.calculateFitnessFunctionAtTheBeginning(drivers) #calcolo la fitness function del mio driver 
           drivers_def.append(driver_parent_to_compare)
           flag = 1
           return True, flag
        else:
           return False, flag
    
    def calculateFitnessFunction(self, drivers): # drivers contiene anche l'ultimo driver runnato
        ff = normalize.get_ff_normalize(drivers)
        self.Fitness_function_totale = ff #setto i valori  del driver

    def calculateFitnessFunctionAtTheBeginning(self, drivers):
        ff = normalize.get_ff_normalize_beginning_driver(drivers)
        self.Fitness_function_totale = ff #setto i valori  del driver




