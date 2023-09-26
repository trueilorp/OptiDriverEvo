import json
import algorimoGenetico
import startVTDSimulation_SimoneDario
import logging
import algorimoGenetico
import buildDriverVariabile
import subprocess, logging, os, time, datetime, shutil, random, string, sys, glob
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
import SelectFromCSV

from src.utils import DRIVER_PARAMS_LABEL_TO_NAME, read_configurations, configure_loggers, make_output_folders, copy_files
##from src.utils import FMU_DEFAULT_PATH, generate_fmu_mapping_car, fmu_mapping_car_path
from src.adams import shrink_results
from src.adams import TooManyResultsError, generate_post_processing_files


def buildDriverJSON(listaValori):
    default_directory = '/home/udineoffice/Desktop/SimulationLauncher'
    if os.getcwd() != default_directory:
        os.chdir(default_directory)
    # Carica il file di configurazione JSON
    with open('driver_config_variabile.json') as config_file:
        config_data = json.load(config_file)

        driver_genitore = config_data['DRIVER']
        
    # Assegna un valore a 'api_key'
        driver_genitore['DesiredVelocity'] = listaValori[0]
        driver_genitore['DesiredAcceleration'] = listaValori[1]
        driver_genitore['DesiredDeceleration'] = listaValori[2]
        driver_genitore['CurveBehavior'] = listaValori[3]
        driver_genitore['ObserveSpeedLimits'] = listaValori[4]
        driver_genitore['DistanceKeeping'] = listaValori[5]
        driver_genitore['LaneKeeping'] = listaValori[6]
        driver_genitore['SpeedKeeping'] = listaValori[7]
        driver_genitore['LaneChangingDynamic'] = listaValori[8]
        driver_genitore['UrgeToOvertake'] = listaValori[9]
        driver_genitore['RespondToTailgatingVehicles'] = listaValori[10]
        driver_genitore['ForesightDistance'] = listaValori[11]
        driver_genitore['SteeringDistance'] = listaValori[12]
        driver_genitore['ObserveKeepRightRule'] = listaValori[13]
        driver_genitore['ConsiderEnvConditions'] = listaValori[14]
        driver_genitore['UseOfIndicator'] = listaValori[15]
        driver_genitore['ReactionTime'] = listaValori[16]
        driver_genitore['ObeyTrafficSigns'] = listaValori[17]
        driver_genitore['ObeyTrafficLights'] = listaValori[18]
        driver_genitore['ObeyTrafficRules'] = listaValori[19]
        driver_genitore['Swarm'] = listaValori[20]
        driver_genitore['RouteAdherence'] = listaValori[21]

    with open('driver_config_variabile.json', "w") as config_file:
        json.dump(config_data, config_file, indent=4)

    # Accedi ai valori di configurazione
    #speedKeeping = config_data['SpeedKeeping']
    #steeringDistance = config_data['SteeringDistance']

