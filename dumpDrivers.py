from scipy.integrate import quad
from openpyxl import Workbook
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import os, logging
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()

logging.getLogger('matplotlib').setLevel(logging.WARNING) 

def build_header_file_csv(sheet):
    headers = [
        'Run/Drivers', 'TravelTime (s)', 'LaneOffset (cm)',
        'Total Fitness Function', 'Best driver',
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
         
def get_grafico(run_values, y_values, tipo_grafico, dir_path):
    
    cartella_radice = dir_path
    nome_sottocartella = 'Graphs'
    cartella = os.path.join(cartella_radice, nome_sottocartella)
    
    if not os.path.exists(cartella):
            os.makedirs(cartella)
    
    # Visualizza la funzione gaussiana
    plt.plot(run_values, y_values)
    plt.title('Funzione Gaussiana')
    plt.xlabel('Run')
    plt.ylabel('Fitness function')
    plt.grid(True)

    nome_grafico = f'grafico_{tipo_grafico}.png'
    percorso_grafico = os.path.join(cartella, nome_grafico)
    plt.savefig(percorso_grafico)

    plt.close()

def save_csv():
    # Specifica il percorso della directory principale
    directory_path = '/home/udineoffice/Desktop/SimulationLauncherNew/outputs'

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

def dump_drivers(drivers, best_drivers):

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

    for driver, best_driver in zip(drivers, best_drivers):
        
        valori_run.append(num_of_run)
        time_sim = driver.TimeSim
        valori_time_sim.append(time_sim)
        lane_offset = driver.LaneOffset
        valori_lane_offset.append(lane_offset)
        fitness_function = driver.Fitness_function_totale
        valori_fitness_function.append(fitness_function)

        #Scrivo i valori del mio driver
        sheet['A' + str(num_of_run + 1)] = driver.id_driver
        sheet['B' + str(num_of_run + 1)] = time_sim
        sheet['C' + str(num_of_run + 1)] = lane_offset
        sheet['D' + str(num_of_run + 1)] = fitness_function
        sheet['E' + str(num_of_run + 1)] = best_driver.id_driver

        colonna_parametri = 6
        #Scrivo i parametri del mio driver
        for params in driver.Lista_parametri:
            cella = sheet.cell(row=num_of_run+1, column=colonna_parametri)  
            cella.value = params
            colonna_parametri += 1  # Passa alla colonna successiva per il prossimo parametro

        num_of_run += 1
        nuovo_file.save(path_file_to_store)
    
    nuovo_file.close()
   
    get_grafico(valori_run, valori_time_sim, "time simulation", dir_path)
    get_grafico(valori_run, valori_lane_offset, "lane offset", dir_path)
    get_grafico(valori_run, valori_fitness_function, "fitness function totale", dir_path)
