from scipy.integrate import quad
from openpyxl import Workbook
from openpyxl import load_workbook
import numpy as np, json
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()

def get_max_min_absolute():
    with open('/home/udineoffice/Desktop/OptiDriverEvo_OnePlusOne/config.json', 'r') as file:
        config = json.load(file)
    return config["maxTravelTime"], config["minTravelTime"], config["maxLaneOffset"], config["minLaneOffset"]

def get_normalized_ts(driver_off):
    max_ts, min_ts, _,_ = get_max_min_absolute()
    ff_value_normalized = (driver_off.time_sim - min_ts)/(max_ts-min_ts)
    return ff_value_normalized

def get_normalized_lo(driver_off):
    _,_, max_lo, min_lo = get_max_min_absolute()
    ff_value_normalized = (driver_off.lane_offset - min_lo)/(max_lo-min_lo)
    return ff_value_normalized
    
def calculate_fitness_function(driver_offspring):   
    fitness_function = get_normalized_ts(driver_offspring) + get_normalized_lo(driver_offspring)
    print("\nFITNESS FUNCTION " + str(fitness_function))
    driver_offspring.total_fitness_function = fitness_function




