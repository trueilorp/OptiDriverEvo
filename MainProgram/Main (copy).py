import startVTDSimulation_SimoneDario
import algoritmoGenetico
import dumpDrivers
import driver
from src.utils import DRIVER_PARAMS_LABEL_TO_NAME, read_configurations, configure_loggers, make_output_folders, copy_files
import json, logging, datetime, copy
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()

logging.getLogger('matplotlib').setLevel(logging.WARNING)

def buildJSON_ofDriver(lista_parametri):
        # Carica il file di configurazione JSON
        with open('/home/udineoffice/Desktop/SimulationLauncherNew/driver_config.json') as config_file:
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
                driver_genitore[attribute] = lista_parametri[i]

        with open('/home/udineoffice/Desktop/SimulationLauncherNew/driver_config.json', "w") as config_file:
            json.dump(config_data, config_file, indent=4)

def get_number_of_runs():
    with open('/home/udineoffice/Desktop/SimulationLauncherNew/config.json', 'r') as file:
        config = json.load(file)
    return config["numberOfIterations"]

def simulate(driver, num_runs):
    buildJSON_ofDriver(driver.Lista_parametri) #applico la configurazione del driver al json 
    time_sim, media_lane_offset = startVTDSimulation_SimoneDario.scriptVTD(num_runs) #starta vtd con il driver corrente 
    return (time_sim, media_lane_offset)

if __name__ == '__main__': #tipico codice all`inizio dello script, infatti ci permette di dire che il file verra eseguito solo se il modulo viene eseguito direttamente come script e non quando viene importato da un altro script. __name__ variabile predefinita che contiene il nome del modulo
        
    time_beginning_of_program = datetime.datetime.now() #prendo il tempo di inizio programma 
    num_run = 1 #definisco contatore

    drivers_runs = [] #definisco una lista nella quale salvero' tutti i vari driver
    drivers_runs_to_dump = [] #definisco la lista dove, dopo aver settato le perfomance del driver, viene inserito all'interno di essa
    who_is_best_driver = [] #lista che contiene tutti i best parziali

    driverParent = driver.Driver(num_run,[])
    driverParent.buildDefaultDriver() #costruisco il mio driver di default
    
    print('\nSTANDARD SIMULATION 1\n')
    timeSim, MaxLaneOffset  = simulate(driverParent, num_run) #inizio la simulazione di vtd con il mio driver  
    driverParent.setPerformance(timeSim, MaxLaneOffset) #setto i valori  del driver 
    drivers_runs.append(driverParent) #aggiungo il driverParent alla mia lista di tutti i driver 
    #aspetto a calcolare la fitness function del parent perche' non ho valori con cui confrontarla 

    num_run += 1
    ff_already_calculated = False
    tot_runs = get_number_of_runs()
   
    while (num_run <= tot_runs):
        
        print('\nSIMULATION NUMBER ' + str(num_run) + '\n')

        lista_parametri_offspring = algoritmoGenetico.mutaGene(driverParent) #muto la lista dei parametri
        driverOffspring = driver.Driver(num_run, lista_parametri_offspring) #creo il driver offspring 

        print("Starting VTD Script")
        timeSim, MaxLaneOffset = simulate(driverOffspring, num_run) 
        driverOffspring.setPerformance(timeSim, MaxLaneOffset)
        drivers_runs.append(copy.deepcopy(driverOffspring))
        can_calculate_ff, ff_already_calculated = driverOffspring.calculateFFParent(drivers_runs, ff_already_calculated, drivers_runs_to_dump)
        
        if can_calculate_ff == True:
            driverOffspring.calculateFitnessFunction(drivers_runs, drivers_runs_to_dump) #calcolo la fitness function del mio driver 
            algoritmoGenetico.setNewDriverParent(driverParent, driverOffspring)    
            best_driver = driverParent
        
        who_is_best_driver.append(copy.deepcopy(best_driver))
        num_run += 1 

print("\nThis is the best driver:\nParameters: " + str(best_driver.Lista_parametri) + str('\nTime of simulation:  ') 
      + str(best_driver.TimeSim) + str('\nMax lane offset: ')  + str(best_driver.LaneOffset) 
      + str('\nFitness function: ')  + str(best_driver.Fitness_function_totale))

print("\nDumping drivers...")
dumpDrivers.dump_drivers(drivers_runs_to_dump, who_is_best_driver)

duration = datetime.datetime.now() - time_beginning_of_program
print('\n\nTempo totale programma -> ' + "{:.2f}".format(duration.total_seconds()/60) + 'min')
print("\nALL DONE!")

