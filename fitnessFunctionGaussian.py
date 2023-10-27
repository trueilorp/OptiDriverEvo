from scipy.integrate import quad
from openpyxl import Workbook
from openpyxl import load_workbook
import numpy as np
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()

def gaussian(x, mean, std_dev):
    return 1 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-((x - mean) ** 2) / (2 * std_dev ** 2))

def get_normalize_values(ff_values):
    
    normalized_values = [] 

    #https://stackoverflow.com/questions/40137244/why-does-quad-return-both-zeros-when-integrating-a-simple-gaussian-pdf-at-a-very
    mean = np.mean(ff_values)
    std = np.std(ff_values)

    for ff_value in ff_values:
        integral, _ = quad(gaussian, -1, ff_value, args=(mean, std), points=[-1*np.sqrt(std), 1*np.sqrt(std)])
        norm_value = 1 - integral
        normalized_values.append(norm_value)

    return normalized_values
     
def get_ff_normalize(drivers):
 
    valori_parziali_ts = []
    valori_parziali_lo = []

    for driver in drivers:        
        valori_parziali_ts.append(driver.time_sim) 
        #if driver.lane_offset != -1:
        valori_parziali_lo.append(driver.lane_offset)
        
    '''last_driver = drivers[which_driver] 
    time_sim_last_driver = last_driver.time_sim
    lane_offset_last_driver = last_driver.lane_offset'''

    #if lane_offset_last_driver == -1:
        #return -1

    norm_time_sims = get_normalize_values(valori_parziali_ts)
    norm_lane_offs = get_normalize_values(valori_parziali_lo)
     
    fitness_functions = [ts + lo for ts, lo in zip(norm_time_sims, norm_lane_offs)]
    return fitness_functions #lista di tutte le fitness 

def can_calculate_ff(drivers_runs):
    if drivers_runs[-1].time_sim != drivers_runs[-2].time_sim and drivers_runs[-1].lane_offset != drivers_runs[-2].lane_offset:
        return True
    else:
        return False
    
def calculate_fitness_function(driver_runs):   
    fitness_functions = get_ff_normalize(driver_runs)
    for i,driver in enumerate(driver_runs):
        driver.total_fitness_function = fitness_functions[i]

def get_new_parent(drivers_runs):
    parent = drivers_runs[-2]
    offspr = drivers_runs[-1]
    if parent.time_sim != offspr.time_sim:
        if(offspr.time_sim < parent.time_sim):
            parent = offspr          
    else: #time_sim sono uguali
        if(offspr.lane_offset < parent.lane_offset):
            parent = offspr
    return parent





