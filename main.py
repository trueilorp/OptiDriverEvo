import startVTDSimulation_SimoneDario
import algoritmoGenetico
import dumpDrivers
import driver
import fitnessFunctionAbsolute, fitnessFunctionGaussian
import json, logging, datetime
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()

logging.getLogger('matplotlib').setLevel(logging.WARNING)

def build_json_of_driver(lista_parametri):
        # Carica il file di configurazione JSON
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
    build_json_of_driver(driver.parameters) #applico la configurazione del driver al json 
    time_sim, media_lane_offset = startVTDSimulation_SimoneDario.scriptVTD(num_runs) #starta vtd con il driver corrente 
    return (time_sim, media_lane_offset)

def one_plus_one_absolute():
    num_run = 1 #definisco contatore

    drivers_runs = [] #definisco una lista nella quale salvero' tutti i vari driver
    best_drivers = [] #lista che contiene tutti i best parziali

    driver_parent = driver.Driver(1,[])
    driver_parent.build_default_driver() #costruisco il mio driver di default
    
    print('\nSTANDARD SIMULATION 1\n')
    time_sim, max_lane_offset  = simulate(driver_parent, num_run) #inizio la simulazione di vtd con il mio driver  
    driver_parent.set_performance(time_sim, max_lane_offset) #setto i valori  del driver 
    drivers_runs.append(driver_parent) #aggiungo il driverParent alla mia lista di tutti i driver 
    
    fitnessFunctionAbsolute.calculate_fitness_function(driver_parent) 

    best_drivers.append(driver_parent)
    num_run += 1
    tot_runs = get_number_of_runs()
   
    while (num_run <= tot_runs):
        
        print('\nSIMULATION NUMBER ' + str(num_run) + '\n')

        offspring_parameters = algoritmoGenetico.mutate(driver_parent) #mutate driver paramters
        driver_offspring = driver.Driver(num_run, offspring_parameters) #instatiate new offspring driver 

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

    num_run = 1 #definisco contatore

    drivers_runs = [] #definisco una lista nella quale salvero' tutti i vari driver
    best_drivers = [] #lista che contiene tutti i best parziali

    driver_parent = driver.Driver(1,[])
    driver_parent.build_default_driver() #costruisco il mio driver di default
    
    print('\nSTANDARD SIMULATION 1\n')
    time_sim, max_lane_offset  = simulate(driver_parent, num_run) #inizio la simulazione di vtd con il mio driver  
    driver_parent.set_performance(time_sim, max_lane_offset) #setto i valori  del driver 
    drivers_runs.append(driver_parent) #aggiungo il driverParent alla mia lista di tutti i driver 
    #aspetto a calcolare la fitness function del parent perche' non ho valori con cui confrontarla 

    best_drivers.append(driver_parent)
    num_run += 1
    ff_already_calculated = False
    tot_runs = get_number_of_runs()
   
    while (num_run <= tot_runs):
        
        print('\nSIMULATION NUMBER ' + str(num_run) + '\n')

        offspring_parameters = algoritmoGenetico.mutate(driver_parent) #mutate driver paramters
        driver_offspring = driver.Driver(num_run, offspring_parameters) #instatiate new offspring driver 

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
                driver_parent = fitnessFunctionGaussian.get_new_parent(drivers_runs) #caso in cui uno dei valori e' diverso
        
        best_drivers.append(driver_parent)
        print("\nDumping drivers...")
        dumpDrivers.dump_drivers(drivers_runs, best_drivers)
        num_run += 1 

    return driver_parent

# ############ #
# MAIN PROGRAM #
# ############ #    

if __name__ == "__main__":

    time_beginning_of_program = datetime.datetime.now() #prendo il tempo di inizio programma 
    with open('/home/udineoffice/Desktop/OptiDriverEvo_OnePlusOne/sim_config.json', 'r') as file:
        method_simulation = json.load(file)
        sim_config = method_simulation.get('Simone_Dario_Audi_A4_2009_black', {})
    try:
        if sim_config["methodOfSimulation"] == "Gaussian":
            driver_parent = one_plus_one_gaussian()
        elif sim_config["methodOfSimulation"] == "Absolute":
            driver_parent = one_plus_one_absolute()
    except KeyError:
        print("La chiave 'methodOfSimulation' non è presente nel dizionario.")

    print("\nThis is the best driver:\nParameters: " + str(driver_parent.parameters) + str('\nTime of simulation:  ') 
      + str(driver_parent.time_sim) + str('\nMax lane offset: ')  + str(driver_parent.lane_offset) 
      + str('\nFitness function: ')  + str(driver_parent.total_fitness_function))
    
    duration = datetime.datetime.now() - time_beginning_of_program
    print('\n\nTOTAL TIME ELAPSED -> ' + "{:.2f}".format(duration.total_seconds()/60) + 'min')
    print("\nALL DONE!")
