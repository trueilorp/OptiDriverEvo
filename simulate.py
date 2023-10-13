
import startVTDSimulation_SimoneDario
import algoritmoGenetico
import dumpPopulation
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

def get_number_of_runs():
    with open('/home/udineoffice/Desktop/SimulationLauncher_PopulationBased/config.json', 'r') as file:
        config = json.load(file)
    return config["numberOfIterations"]

def simulate(driver, num_runs):
    genes_of_driver = driver.parameters
    print(genes_of_driver)
    buildJSON_ofDriver(genes_of_driver) #applico la configurazione del driver al json 
    time_sim, media_lane_offset = startVTDSimulation_SimoneDario.scriptVTD(num_runs) #starta vtd con il driver corrente 
    return (time_sim, media_lane_offset)

def start_of_program():

    time_beginning_of_program = datetime.datetime.now() #prendo il tempo di inizio programma 
    num_run = 1 #definisco contatore

    drivers_runs = [] #definisco una lista nella quale salvero' tutti i vari driver
    best_drivers = [] #lista che contiene tutti i best parziali

    driver_parent = driver.Driver(1,[])
    driver_parent.build_default_driver() #costruisco il mio driver di default
    
    print('\nSTANDARD SIMULATION 1\n')
    time_sim, max_lane_offset  = simulate(driver_parent, num_run) #inizio la simulazione di vtd con il mio driver  
    drivers_runs.append(driver_parent) #aggiungo il driverParent alla mia lista di tutti i driver 
    #aspetto a calcolare la fitness function del parent perche' non ho valori con cui confrontarla 

    best_drivers.append(driver_parent)
    num_run += 1
    ff_already_calculated = False
    tot_runs = get_number_of_runs()
   
    while (num_run <= tot_runs):
        
        print('\nSIMULATION NUMBER ' + str(num_run) + '\n')

        lista_parametri_offspring = algoritmoGenetico.muta_gene(driver_parent) #muto la lista dei parametri
        driver_offspring = driver.Driver(num_run, lista_parametri_offspring) #creo il driver offspring 

        print("Starting VTD Script")
        time_sim, max_lane_offset = simulate(driver_offspring, num_run) 
        driver_offspring.set_performance(time_sim, max_lane_offset)
        drivers_runs.append(driver_offspring)
        
        if ff_already_calculated == True:
            fitnessFunction.calculate_fitness_function(drivers_runs, -1) #offspring  
            driver_parent = algoritmoGenetico.get_best_driver(driver_parent, driver_offspring)              
        else:
            if fitnessFunction.can_calculate_ff(drivers_runs):     
                fitnessFunction.calculate_fitness_function(drivers_runs, -2) #parent
                fitnessFunction.calculate_fitness_function(drivers_runs, -1) #offspring
                ff_already_calculated = True
                driver_parent = algoritmoGenetico.get_best_driver(drivers_runs[-2], drivers_runs[-1]) 
            else:
                driver_parent = fitnessFunction.get_new_parent(drivers_runs) #caso in cui uno dei valori e' diverso, deepcopy
        
        best_drivers.append(driver_parent)
        num_run += 1 

    end_of_program(driver_parent, drivers_runs, best_drivers, time_beginning_of_program)

def end_of_program(driver_parent, drivers_runs, best_drivers, time_beginning_of_program):
    print("\nThis is the best driver:\nParameters: " + str(driver_parent.Lista_parametri) + str('\nTime of simulation:  ') 
      + str(driver_parent.TimeSim) + str('\nMax lane offset: ')  + str(driver_parent.LaneOffset) 
      + str('\nFitness function: ')  + str(driver_parent.Fitness_function_totale))

    print("\nDumping drivers...")
    dumpPopulation.dump_population(drivers_runs, best_drivers)

    duration = datetime.datetime.now() - time_beginning_of_program
    print('\n\nTempo totale programma -> ' + "{:.2f}".format(duration.total_seconds()/60) + 'min')
    print("\nALL DONE!")

    






