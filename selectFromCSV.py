import csv
import numpy as np
# Specifica il percorso completo del file CSV

WIDTH_ROAD = 3.500 #ho verificato dallo scenario editor 
WIDTH_LANE = WIDTH_ROAD/2

def check_out_of_lane(max_lane_offset):
    check = (WIDTH_ROAD/4) + (max_lane_offset)
    if check > WIDTH_LANE:
        return False # l'auto e' uscita dalla corsia 
    else:
        return True # l'auto e' rimasta in corsia 

'''def check_out_of_lane(csv_file):
    lane_id_column = []
    with open(csv_file, newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)
        for row in csv_reader:
            numero_colonne = len(row)
            if numero_colonne > 4:        
                try:
                    lane_id = row[4]  # Indice corrisponde alla colonna che mi interessa: laneId
                    lane_id_column.append(lane_id)
                except ValueError:
                    lane_id_column.append(-1)
            
        for valore in lane_id_column:
            if valore != -1:
                return False
            else:
                return True'''

def get_time_sim_from_csv(csv_file):
    time_sim_column = []
    with open(csv_file, newline='') as file:
        # Crea un oggetto CSV reader
        csv_reader = csv.reader(file)
        
        # Salta la riga dell'intestazione se presente
        next(csv_reader, None)

        for row in csv_reader:
            time_sim = row[0]  # Indice corrisponde alla colonna che mi interessa
            time_sim_column.append(time_sim)

        time_sim_column_float = []
        for stringa in time_sim_column:
            try:
                valore_float = float(stringa)
                time_sim_column_float.append(valore_float)
            except ValueError:
                # Se la conversione in float non è possibile, puoi gestire il caso qui
                valore_float = 0
                time_sim_column_float.append(valore_float)
    # Prendo il massimo valore
    time_simulation = max(time_sim_column_float)
    return time_simulation

def get_max_lane_offset_from_csv(csv_file):

    # Crea le liste per memorizzare i dati
    lane_offset_column = []
    with open(csv_file, newline='') as file1:
        csv_reader1 = csv.reader(file1) # Apri il file CSV in modalità di lettura
        next(csv_reader1, None)
        for row in csv_reader1:
            numero_colonne = len(row)
            if numero_colonne > 8:
                laneoffset = row[8] 
                lane_offset_column.append(laneoffset)

    # Converto in float i valori del laneOffset
        lane_offset_column_float = []
        for stringa in lane_offset_column:
            try:
                valore_float = float(stringa)
                lane_offset_column_float.append(valore_float)
            except ValueError:
                # Se la conversione in float non è possibile, puoi gestire il caso qui
                valore_float = 0

# Ora hai la lista laneOffset_column_float contenente i valori validi convertiti in float

    laneOffset_column_float_absolute = [abs(valore) for valore in lane_offset_column_float]
    valore_max_lane_offset = max(laneOffset_column_float_absolute)
    if check_out_of_lane(valore_max_lane_offset): #e' in corsia 
        return valore_max_lane_offset * 100 #trasfomo in cm 
    else:
        return -1
    

