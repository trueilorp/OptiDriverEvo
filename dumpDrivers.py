from scipy.integrate import quad
from openpyxl import Workbook
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import os, logging
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()

logging.getLogger('matplotlib').setLevel(logging.WARNING) 

def doGrafico(run_values, y_values, tipo_grafico):
    
    cartella_radice = '/home/udineoffice/Desktop'
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

    # Ordina le cartelle per data di modifica, con la più recente in cima
    folders.sort(key=lambda x: os.path.getmtime(os.path.join(directory_path, x)), reverse=True)

    # Prendi la prima cartella (la più recente)
    if folders:
        most_recent_folder = folders[0]
        
        # Costruisci il percorso completo del file da memorizzare
        file_to_store = os.path.join(directory_path, most_recent_folder, 'Result_of_simulation.xlsx')
        print(file_to_store)

    workbook = Workbook()
    workbook.save(file_to_store)

    return file_to_store

def dump_drivers(drivers):

    valori_run = []
    valori_time_sim = []
    valori_lane_offset = []
    valori_fitness_function = []

    path_file_to_store = save_csv()
    nuovo_file = load_workbook(path_file_to_store)
    sheet = nuovo_file.active
    sheet.title = "Results of simulation"
    print("File Excel esistente aperto in modalità di sola lettura.")
    
    sheet['A1'] = 'Run'
    sheet['B1'] = 'TravelTime (s)'
    sheet['C1'] = 'LaneOffset'
    sheet['D1'] = 'ff1 + ff2'

    nuovo_file.save(path_file_to_store)

    num_of_run = 1

    for driver in drivers:
    
        valori_run.append(num_of_run)
        time_sim = driver.TimeSim
        valori_time_sim.append(time_sim)
        lane_offset = driver.LaneOffset
        valori_lane_offset.append(lane_offset)
        fitness_function = driver.Fitness_function_totale
        valori_fitness_function.append(fitness_function)

        #Scrivo i valori del mio driver
        sheet['A' + str(num_of_run + 1)] = num_of_run
        sheet['B' + str(num_of_run + 1)] = time_sim
        sheet['C' + str(num_of_run + 1)] = lane_offset
        sheet['D' + str(num_of_run + 1)] = fitness_function

        num_of_run += 1
        nuovo_file.save(path_file_to_store)
    
    nuovo_file.close()
   
    doGrafico(valori_run, valori_time_sim, "time simulation")
    doGrafico(valori_run, valori_lane_offset, "lane offset")
    doGrafico(valori_run, valori_fitness_function, "fitness function totale")
