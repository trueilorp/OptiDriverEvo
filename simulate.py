
import startVTDSimulation_SimoneDario
import algoritmoGenetico
import dumpDrivers
import driver
import fitnessFunction
from src.utils import DRIVER_PARAMS_LABEL_TO_NAME, read_configurations, configure_loggers, make_output_folders, copy_files
import json, logging, datetime, copy
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()

logging.getLogger('matplotlib').setLevel(logging.WARNING)

def buildJSON_ofDriver(lista_parametri):
        # Carica il file di configurazione JSON
        with open('/home/udineoffice/Desktop/SimulationLauncher_PopulationBased/driver_config.json') as config_file:
            config_data = json.load(config_file)

            driver_genitore = config_data['DRIVER']
        # Assegna un valore a 'api_key'
            attributes = [  'DesiredVelocity', 'DesiredAcceleration', 'DesiredDeceleration', 'CurveBehavior',
                            'ObserveSpeedLimits', 'DistanceKeeping', 'LaneKeeping', 'SpeedKeeping',
                            'LaneChangingDynamic', 'UrgeToOvertake', 'RespondToTailgatingVehicles',
                            'ForesightDistance', 'SteeringDistance', 'ObserveKeepRightRule',
                            'ConsiderEnvConditions', 'UseOfIndicator', 'ReactionTime', 'ObeyTrafficSigns',
                            'ObeyTrafficLights', 'ObeyTrafficRules', 'Swarm', 'RouteAdherence']
                         
            for i, attribute in enumerate(attributes):
                driver_genitore[attribute] = str(lista_parametri[i])

        with open('/home/udineoffice/Desktop/SimulationLauncher_PopulationBased/driver_config.json', "w") as config_file:
            json.dump(config_data, config_file, indent=4)

def simulate(driver, num_runs):
    genes_of_driver = driver.parameters
    print(genes_of_driver)
    buildJSON_ofDriver(genes_of_driver) #applico la configurazione del driver al json 
    time_sim, media_lane_offset = startVTDSimulation_SimoneDario.scriptVTD(num_runs) #starta vtd con il driver corrente 
    return (time_sim, media_lane_offset)








