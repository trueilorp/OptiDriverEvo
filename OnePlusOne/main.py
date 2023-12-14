import dumpDrivers, algoritmoGenetico, driver, startVTDSimulation_SimoneDario, fitnessFunctionAbsolute, fitnessFunctionGaussian
import json, logging, datetime
from dotenv import load_dotenv 
load_dotenv()

logging.getLogger('matplotlib').setLevel(logging.WARNING)

def build_json_of_driver(lista_parametri):
        with open('/home/udineoffice/Desktop/OptiDriverEvo_OnePlusOne/driver_config.json') as config_file:
            config_data = json.load(config_file)

            driver_genitore = config_data['DRIVER']
            attributes = [  'DesiredVelocity', 'DesiredAcceleration', 'DesiredDeceleration', 'CurveBehavior',
                            'ObserveSpeedLimits', 'DistanceKeeping', 'LaneKeeping', 'SpeedKeeping',
                            'LaneChangingDynamic', 'UrgeToOvertake', 'RespondToTailgatingVehicles',
                            'ForesightDistance', 'SteeringDistance', 'ObserveKeepRightRule',
                            'ConsiderEnvConditions', 'UseOfIndicator', 'ReactionTime', 'ObeyTrafficSigns',
                            'ObeyTrafficLights', 'ObeyTrafficRules', 'Swarm', 'RouteAdherence']
                         
            for i, attribute in enumerate(attributes):
                driver_genitore[attribute] = lista_parametri[i]

        with open('/home/udineoffice/Desktop/OptiDriverEvo_OnePlusOne/driver_config.json', "w") as config_file:
            json.dump(config_data, config_file, indent=4)

def get_number_of_runs():
    with open('/home/udineoffice/Desktop/OptiDriverEvo_OnePlusOne/config.json', 'r') as file:
        config = json.load(file)
    return config["numberOfIterations"]

def simulate(driver, num_runs):
    build_json_of_driver(driver.parameters) 
    time_sim, media_lane_offset = startVTDSimulation_SimoneDario.scriptVTD(num_runs)
    return (time_sim, media_lane_offset)

def one_plus_one_absolute():
    num_run = 1 
    drivers_runs = []
    best_drivers = []

    driver_parent = driver.Driver(1,[])
    driver_parent.build_default_driver()
    
    print('\nSTANDARD SIMULATION 1\n')
    time_sim, max_lane_offset  = simulate(driver_parent, num_run) 
    driver_parent.set_performance(time_sim, max_lane_offset)
    drivers_runs.append(driver_parent) 
    
    fitnessFunctionAbsolute.calculate_fitness_function(driver_parent) 

    best_drivers.append(driver_parent)
    num_run += 1
    tot_runs = get_number_of_runs()
    
    while (num_run <= tot_runs):      
        print('\nSIMULATION NUMBER ' + str(num_run) + '\n')
        offspring_parameters = algoritmoGenetico.mutate(driver_parent)
        driver_offspring = driver.Driver(num_run, offspring_parameters) 

        print("Starting VTD Script")
        time_sim, max_lane_offset = simulate(driver_offspring, num_run) 
        driver_offspring.set_performance(time_sim, max_lane_offset)
        drivers_runs.append(driver_offspring)

        fitnessFunctionAbsolute.calculate_fitness_function(driver_offspring) 
        driver_parent = algoritmoGenetico.get_best_driver(driver_parent, driver_offspring)              
        
        best_drivers.append(driver_parent)
        print("\nDumping drivers...")
        dumpDrivers.dump_drivers(drivers_runs, best_drivers)
        num_run += 1 
    
    return driver_parent

def one_plus_one_gaussian():
    num_run = 1 
    drivers_runs = []
    best_drivers = [] 

    driver_parent = driver.Driver(1,[])
    driver_parent.build_default_driver() 
    
    print('\nSTANDARD SIMULATION 1\n')
    time_sim, max_lane_offset  = simulate(driver_parent, num_run) 
    driver_parent.set_performance(time_sim, max_lane_offset) 
    drivers_runs.append(driver_parent)

    best_drivers.append(driver_parent)
    num_run += 1
    ff_already_calculated = False
    tot_runs = get_number_of_runs()
   
    while (num_run <= tot_runs):
        
        print('\nSIMULATION NUMBER ' + str(num_run) + '\n')
        offspring_parameters = algoritmoGenetico.mutate(driver_parent) 
        driver_offspring = driver.Driver(num_run, offspring_parameters) 

        print("Starting VTD Script")
        time_sim, max_lane_offset = simulate(driver_offspring, num_run) 
        driver_offspring.set_performance(time_sim, max_lane_offset)
        drivers_runs.append(driver_offspring)
        
        if ff_already_calculated == True:
            fitnessFunctionGaussian.calculate_fitness_function(drivers_runs) 
            driver_parent = algoritmoGenetico.get_best_driver(driver_parent, driver_offspring)              
        else:
            if fitnessFunctionGaussian.can_calculate_ff(drivers_runs):     
                fitnessFunctionGaussian.calculate_fitness_function(drivers_runs) 
                ff_already_calculated = True
                driver_parent = algoritmoGenetico.get_best_driver(driver_parent, driver_offspring) 
            else:
                driver_parent = fitnessFunctionGaussian.get_new_parent(drivers_runs) 
        
        best_drivers.append(driver_parent)
        print("\nDumping drivers...")
        dumpDrivers.dump_drivers(drivers_runs, best_drivers)
        num_run += 1 

    return driver_parent

# ############ #
# MAIN PROGRAM #
# ############ #    

if __name__ == "__main__":

    time_beginning_of_program = datetime.datetime.now() 
    with open('/home/udineoffice/Desktop/OptiDriverEvo_OnePlusOne/sim_config.json', 'r') as file:
        method_simulation = json.load(file)
        sim_config = method_simulation.get('Simone_Dario_Audi_A4_2009_black', {})
    try:
        if sim_config["methodOfSimulation"] == "Gaussian":
            driver_parent = one_plus_one_gaussian()
        elif sim_config["methodOfSimulation"] == "Absolute":
            driver_parent = one_plus_one_absolute()
    except KeyError:
        print("Key 'methodOfSimulation' is not in file sim_conf.json")

    print("\nThis is the best driver:\nParameters: " + str(driver_parent.parameters) + str('\nTime of simulation:  ') 
      + str(driver_parent.time_sim) + str('\nMax lane offset: ')  + str(driver_parent.lane_offset) 
      + str('\nFitness function: ')  + str(driver_parent.total_fitness_function))
    
    dumpDrivers.write_drivers_in_excel()
    duration = datetime.datetime.now() - time_beginning_of_program
    print('\n\nTOTAL TIME ELAPSED -> ' + "{:.2f}".format(duration.total_seconds()/60) + 'min')
    print("\nALL DONE!")
