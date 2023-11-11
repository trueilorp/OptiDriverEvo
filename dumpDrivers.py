from scipy.integrate import quad
from openpyxl import Workbook
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os, logging
from os.path import dirname
from dotenv import load_dotenv 
load_dotenv()

logging.getLogger('matplotlib').setLevel(logging.WARNING) 

def build_header_excel():
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

    return headers

def get_path_excel():
    directory_path = '/home/udineoffice/Desktop/OptiDriverEvo_OnePlusOne/outputs'

    folders = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]

    folders.sort(key=lambda x: os.path.getctime(os.path.join(directory_path, x)), reverse=True)

    if folders:
        most_recent_folder = folders[0]
        
        file_to_store = os.path.join(directory_path, most_recent_folder, 'Results_of_simulations.xlsx')
        dir_path = os.path.join(directory_path, most_recent_folder)
        print(file_to_store)

    return file_to_store, dir_path

def dump_drivers(drivers, best_drivers):
    path_file_to_store, dir_path = get_path_excel()
    drivers_to_append = []
    for driver, best_driver in zip(drivers, best_drivers):
        row_driver_to_append = [driver.id_driver, driver.time_sim, driver.lane_offset, driver.total_fitness_function, best_driver.id_driver]
        for param in driver.parameters:
            row_driver_to_append.append(float(param))
        drivers_to_append.append(row_driver_to_append)       
          
    with open(os.path.join(dir_path,'driver_temp.csv'), 'a', newline='\n') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerows(drivers_to_append)
        writer.writerow('\n')

def write_drivers_in_excel():
    path_file_to_store, dir_path = get_path_excel()
    with open(os.path.join(dir_path,'driver_temp.csv'), 'r') as file_csv:
        csv_reader = csv.reader(file_csv)
        data = []
        sheet_counter = 2
        with pd.ExcelWriter(path_file_to_store, engine='xlsxwriter') as writer:
            for row in csv_reader:
                if not any(row) or row == ['\n']:
                    if data:                        
                        df = pd.DataFrame(data)
                        df.to_excel(writer, sheet_name=f'Sim_{sheet_counter}', index=False, header=build_header_excel())
                        data = []
                        sheet_counter += 1
                else:
                    float_row = [float(column) for column in row]
                    data.append(float_row)
    os.remove(os.path.join(dir_path,'driver_temp.csv'))