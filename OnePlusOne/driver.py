from dotenv import load_dotenv  
load_dotenv()
import json

class Driver:
     
    def __init__(self, num_run, lista_parametri):
       self.id_driver = num_run
       self.parameters = lista_parametri
       self.time_sim = 0
       self.lane_offset = None
       self.total_fitness_function = -1

    def default_driver_generate_value(self):
        with open('sim_config.json', 'r') as file:
            dati_json = json.load(file)
        sim_config = dati_json.get('Simone_Dario_Audi_A4_2009_black', {})
        initial_driver = sim_config.get('initialDriver', None)

        with open('driver_config.json', 'r') as driver_file:
            driver_data = json.load(driver_file)
        driver_params = driver_data.get(initial_driver, {})
        lista_parametri = list(driver_params.values())
        return lista_parametri

    def build_default_driver(self):
       lista_parametri = self.default_driver_generate_value()
       self.parameters = lista_parametri
        
    def set_performance(self, timesim, laneoffset):
        self.time_sim = timesim
        self.lane_offset = laneoffset
    



