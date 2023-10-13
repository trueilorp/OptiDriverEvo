from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
import json

class Driver:
     
    def __init__(self, lista_parametri):
       self.parameters = lista_parametri

    def default_driver_generate_value(self):
        with open('sim_config.json', 'r') as file:
            dati_json = json.load(file)
        sim_config = dati_json.get('Simone_Dario_SD_A4_2009_black', {})
        initial_driver = sim_config.get('initialDriver', None)

        with open('driver_config.json', 'r') as driver_file:
            driver_data = json.load(driver_file)
        driver_params = driver_data.get(initial_driver, {})
        lista_parametri = list(driver_params.values())
        return lista_parametri

    def build_default_driver(self):
       lista_parametri = self.default_driver_generate_value()
       self.parameters = lista_parametri
        
    def reset_driver(self):
        self.parameters = None



