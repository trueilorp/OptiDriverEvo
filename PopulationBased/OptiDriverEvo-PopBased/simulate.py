import startVTDSimulation_SimoneDario
import json
from dotenv import load_dotenv  
load_dotenv()

def buildJSON_ofDriver(lista_parametri):
        with open('/home/udineoffice/Desktop/OptiDriverEvo_PopulationBased/driver_config.json') as config_file:
            config_data = json.load(config_file)

            driver_genitore = config_data['DRIVER']
            attributes = [  'DesiredVelocity', 'DesiredAcceleration', 'DesiredDeceleration', 'CurveBehavior',
                            'ObserveSpeedLimits', 'DistanceKeeping', 'LaneKeeping', 'SpeedKeeping',
                            'LaneChangingDynamic', 'UrgeToOvertake', 'RespondToTailgatingVehicles',
                            'ForesightDistance', 'SteeringDistance', 'ObserveKeepRightRule',
                            'ConsiderEnvConditions', 'UseOfIndicator', 'ReactionTime', 'ObeyTrafficSigns',
                            'ObeyTrafficLights', 'ObeyTrafficRules', 'Swarm', 'RouteAdherence']
                         
            for i, attribute in enumerate(attributes):
                driver_genitore[attribute] = str(lista_parametri[i])

        with open('/home/udineoffice/Desktop/OptiDriverEvo_PopulationBased/driver_config.json', "w") as config_file:
            json.dump(config_data, config_file, indent=4)

def simulate(driver, num_runs):
    genes_of_driver = driver.parameters
    print(genes_of_driver)
    buildJSON_ofDriver(genes_of_driver) 
    time_sim, media_lane_offset = startVTDSimulation_SimoneDario.scriptVTD(num_runs) 
    return (time_sim, media_lane_offset)
