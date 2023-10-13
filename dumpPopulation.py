from scipy.integrate import quad
from openpyxl import Workbook
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import numpy as np
import os, logging
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()

logging.getLogger('matplotlib').setLevel(logging.WARNING) 

def build_header_file_csv(sheet):
    headers = [
        'Population', 'Run/Drivers', 'TravelTime (s)', 
        'LaneOffset (cm)','Best driver',
        'DesiredVelocity', 'DesiredAcceleration', 'DesiredDeceleration',
        'CurveBehavior', 'ObserveSpeedLimits', 'DistanceKeeping',
        'LaneKeeping', 'SpeedKeeping', 'LaneChangingDynamic',
        'UrgeToOvertake', 'RespondToTailgatingVehicles', 'ForesightDistance',
        'SteeringDistance', 'ObserveKeepRightRule', 'ConsiderEnvConditions',
        'UseOfIndicator', 'ReactionTime', 'ObeyTrafficSigns',
        'ObeyTrafficLights', 'ObeyTrafficRules', 'Swarm', 'RouteAdherence'] 

    for colonna, intestazione in enumerate(headers, start=1):
        cella = sheet.cell(row=1, column=colonna)
        cella.value = intestazione
         
def get_grafico(final_population, dir_path):
    
    cartella_radice = dir_path

    fitnesses_ini = np.array([list(final_population[i].fitness.values) for i in range(len(final_population))])
    fitnesses = np.array([list(final_population[i].fitness.values) for i in range(len(final_population))])
    plt.plot(fitnesses_ini[:,0], fitnesses_ini[:,1], "b.", label="Initial")
    plt.plot(fitnesses[:,0], fitnesses[:,1], "r.", label="Optimized")
    plt.legend(loc="upper right")
    plt.title("fitnesses")
    plt.xlabel("f1")
    plt.ylabel("f2")
    plt.grid(True)

    nome_grafico = f'fitnesses.png'
    percorso_grafico = os.path.join(cartella_radice, nome_grafico)
    plt.savefig(percorso_grafico)
    plt.close()

def save_csv():
    # Specifica il percorso della directory principale
    directory_path = '/home/udineoffice/Desktop/SimulationLauncher_PopulationBased/outputs'

    # Ottieni una lista di tutte le cartelle nella directory principale
    folders = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]

    # Ordina le cartelle per data di creazione, con la più recente in cima
    folders.sort(key=lambda x: os.path.getctime(os.path.join(directory_path, x)), reverse=True)

    # Prendi la prima cartella (la più recente)
    if folders:
        most_recent_folder = folders[0]
        
        # Costruisci il percorso completo del file da memorizzare
        file_to_store = os.path.join(directory_path, most_recent_folder, 'Result_of_simulation.xlsx')
        dir_path = os.path.join(directory_path, most_recent_folder)
        print(file_to_store)

    workbook = Workbook()
    workbook.save(file_to_store)

    return file_to_store, dir_path

def dump_population(pops):

    valori_run = []
    valori_time_sim = []
    valori_lane_offset = []
    valori_fitness_function = []

    path_file_to_store, dir_path = save_csv()
    nuovo_file = load_workbook(path_file_to_store)
    sheet = nuovo_file.active
    sheet.title = "Results of simulation"
    print("File Excel esistente aperto in modalità di sola lettura.")
    
    build_header_file_csv(sheet)
    nuovo_file.save(path_file_to_store)
    num_of_run = 1

    for pop in pops:
        for driver in pop:        
            valori_run.append(num_of_run)
            time_sim = driver.TimeSim
            valori_time_sim.append(time_sim)
            lane_offset = driver.LaneOffset
            valori_lane_offset.append(lane_offset)
            fitness_function = driver.Fitness_function_totale
            valori_fitness_function.append(fitness_function)

            #Scrivo i valori del mio driver
            sheet['A' + str(num_of_run + 1)] = pop
            sheet['B' + str(num_of_run + 1)] = driver.id_driver
            sheet['C' + str(num_of_run + 1)] = time_sim
            sheet['D' + str(num_of_run + 1)] = lane_offset
            sheet['E' + str(num_of_run + 1)] = fitness_function
            sheet['F' + str(num_of_run + 1)] = 'ciao'

            colonna_parametri = 6
            #Scrivo i parametri del mio driver
            for params in driver.Lista_parametri:
                cella = sheet.cell(row=num_of_run+1, column=colonna_parametri)  
                cella.value = params
                colonna_parametri += 1  # Passa alla colonna successiva per il prossimo parametro

            num_of_run += 1
            nuovo_file.save(path_file_to_store)
    
    nuovo_file.close()
    get_grafico(pops, dir_path)
