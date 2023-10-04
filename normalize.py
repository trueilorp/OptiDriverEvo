from scipy.integrate import quad
from openpyxl import Workbook
from openpyxl import load_workbook
import numpy as np
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()

def gaussian(x, mean, std_dev):
    return 1 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-((x - mean) ** 2) / (2 * std_dev ** 2))

def get_normalize_values(values_to_normalize, ff_value):
     
    #https://stackoverflow.com/questions/40137244/why-does-quad-return-both-zeros-when-integrating-a-simple-gaussian-pdf-at-a-very
    mean = np.mean(values_to_normalize)
    std_dev = np.std(values_to_normalize)
    integrale_gaussiana, _ = quad(gaussian, -1, ff_value, args=(mean, std_dev), points=[-1*np.sqrt(std_dev), 1*np.sqrt(std_dev)])
    valore_normalizzato = 1 - integrale_gaussiana   

    print("MEDIA " + str(mean))
    print("DEVIAZIONE STD " + str(std_dev))
    print("INTEGRALE GAUSSIANA " + str(integrale_gaussiana))
    print("VALORE NORMALIZZATO " + str(valore_normalizzato))

    return valore_normalizzato
     
def get_ff_normalize(drivers):
 
    valori_parziali_ts = []
    valori_parziali_lo = []

    for driver in drivers:
        valori_parziali_ts.append(driver.TimeSim) 
        valori_parziali_lo.append(driver.LaneOffset)
        
    last_driver = drivers[-1] #ultimo driver della mia lista da cui prelevo il tempo di simulazione
    time_sim_last_driver = last_driver.TimeSim
    lane_offset_last_driver = last_driver.LaneOffset

    print("\nTIMESIM")
    norm_time_sim = get_normalize_values(valori_parziali_ts, time_sim_last_driver)
    print("\nLANEOFFSET")
    norm_lane_offset = get_normalize_values(valori_parziali_lo, lane_offset_last_driver)
     
    fitness_function = norm_time_sim + norm_lane_offset
    print("\nFITNESS FUNCTION " + str(fitness_function))
    return fitness_function

def get_ff_normalize_beginning_driver(drivers):
 
    valori_parziali_ts = []
    valori_parziali_lo = []

    for driver in drivers:
        valori_parziali_ts.append(driver.TimeSim) 
        valori_parziali_lo.append(driver.LaneOffset)
        
    penultimate_driver = drivers[-2] #primo driver della mia lista da cui prelevo il tempo di simulazione
    time_sim_first_driver = penultimate_driver.TimeSim
    lane_offset_first_driver = penultimate_driver.LaneOffset

    print("\nTIMESIM")
    norm_time_sim = get_normalize_values(valori_parziali_ts, time_sim_first_driver)
    print("\nLANEOFFSET")
    norm_lane_offset = get_normalize_values(valori_parziali_lo, lane_offset_first_driver)
     
    fitness_function = norm_time_sim + norm_lane_offset
    print("\nFITNESS FUNCTION " + str(fitness_function))
    return fitness_function





