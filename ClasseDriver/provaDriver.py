import startVTDSimulation_SimoneDario
import logging
from ClasseDriver import driver
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
from src.utils import DRIVER_PARAMS_LABEL_TO_NAME, read_configurations, configure_loggers, make_output_folders, copy_files
##from src.utils import FMU_DEFAULT_PATH, generate_fmu_mapping_car, fmu_mapping_car_path
from src.adams import shrink_results
from src.adams import TooManyResultsError, generate_post_processing_files


sim_configuration = read_configurations(['sim_config.json']) #quindi leggo lo scenario file e il driver config
driver_configuration = read_configurations(['driver_config.json']) #leggo le varie configurazione dei driver (default, hasty, brisk)
for sim_name,sim_params in sim_configuration.items():
    driver_config_name = sim_params['driverConfigName'] if 'driverConfigName' in sim_params.keys() else None #assegno alle 2 variabili i vari parametri di scenarioFile e driverConfigName che sono presenti in sim_config.json. Se la chiave esiste si assegna il valore, altrimenti no
    #assegno alla variabile il driver che e' scritto nel file json nell'etichetta driverConfigName