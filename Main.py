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
    num_runs = 1 #definisco contatore

    drivers_runs = [] #definisco una lista nella quale salvero' tutti i vari driver
    drivers_runs_def = []
    
    driverParent = driver.Driver([])
    driverParent.buildDefaultDriver() #costruisco il mio driver di default
    
    print('\nSTANDARD SIMULATION 1\n')
    timeSim, MediaLaneOffset  = simulate(driverParent, num_runs) #inizio la simulazione di vtd con il mio driver  
    driverParent.setPerformance(timeSim, MediaLaneOffset) #setto i valori  del driver 
    drivers_runs.append(copy.deepcopy(driverParent)) #aggiungo il driverParent alla mia lista di tutti i driver 
    #aspetto a calcolare la fitness function del parent perche' non ho valori con cui confrontarla 

    #print("Default Driver: " + str(driverParent.TimeSim) + str(' ') + str(driverParent.LaneOffset) + str(' ') + str(driverParent.Fitness_function_totale))

    num_runs += 1
    flag = 0
    tot_runs = get_number_of_runs()
    
    while (num_runs <= tot_runs):
        
        print('\nSIMULATION NUMBER ' + str(num_runs) + '\n')

        lista_parametri_offspring = algoritmoGenetico.mutaGene(driverParent) #muto la lista dei parametri
        driverOffspring = driver.Driver(lista_parametri_offspring) #creo il driver offspring 

        print("Starting VTD Script")
        timeSim, MediaLaneOffset = simulate(driverOffspring, num_runs) 
        driverOffspring.setPerformance(timeSim, MediaLaneOffset)
        drivers_runs.append(copy.deepcopy(driverOffspring))
        can_calculate_ff, flag = driverOffspring.checkFFParent(drivers_runs, flag, drivers_runs_def)
        
        if can_calculate_ff == True:
            driverOffspring.calculateFitnessFunction(drivers_runs) #calcolo la fitness function del mio driver 
            algoritmoGenetico.setNewDriverParent(driverParent, driverOffspring)  
            drivers_runs_def.append(driverOffspring)  
            best_driver = driverParent   
        
        num_runs += 1 

print("\nHai trovato il tuo driver finale: " + str(best_driver.Lista_parametri) + str('\nTime of simulation:  ') 
      + str(best_driver.TimeSim) + str('\nMedia lane offset: ')  + str(best_driver.LaneOffset) 
      + str('\nFitness function:')  + str(best_driver.Fitness_function_totale))

print("\nDumping drivers...")
dumpDrivers.dump_drivers(drivers_runs_def)

duration = datetime.datetime.now() - time_beginning_of_program
print('\n\nTempo totale programma -> ' + "{:.2f}".format(duration.total_seconds()/60) + 'min')
print("\nALL DONE!")

