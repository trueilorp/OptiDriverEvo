import csv
import numpy as np
# Specifica il percorso completo del file CSV

def TimeSimFromCSV(csv_file):
    timeSim_column = []
    with open(csv_file, newline='') as file:
        # Crea un oggetto CSV reader
        csv_reader = csv.reader(file)
        
        # Salta la riga dell'intestazione se presente
        next(csv_reader, None)

        for row in csv_reader:
            timesim = row[0]  # Indice corrisponde alla colonna che mi interessa
            timeSim_column.append(timesim)

        timeSim_column_float = []
        for stringa in timeSim_column:
            try:
                valore_float = float(stringa)
                timeSim_column_float.append(valore_float)
            except ValueError:
                # Se la conversione in float non è possibile, puoi gestire il caso qui
                valore_float = 0
                timeSim_column_float.append(valore_float)
    # Prendo il massimo valore
    timeSimulation = max(timeSim_column_float)
    return timeSimulation

def MediaLaneOffsetFromCSV(csv_file):
    # Crea le liste per memorizzare i dati
    laneOffset_column = []
    with open(csv_file, newline='') as file1:
        csv_reader1 = csv.reader(file1) # Apri il file CSV in modalità di lettura
        next(csv_reader1, None)
        for row in csv_reader1:
            numero_colonne = len(row)
            if numero_colonne > 9:
                laneoffset = row[9] 
                laneOffset_column.append(laneoffset)

    # Converto in float i valori del laneOffset
        laneOffset_column_float = []
        for stringa in laneOffset_column:
            try:
                valore_float = float(stringa)
                laneOffset_column_float.append(valore_float)
            except ValueError:
                # Se la conversione in float non è possibile, puoi gestire il caso qui
                valore_float = 0

# Ora hai la lista laneOffset_column_float contenente i valori validi convertiti in float

    laneOffset_column_float_absolute = [abs(valore) for valore in laneOffset_column_float]
    valoreMedio_LaneOffset = np.mean(laneOffset_column_float_absolute)
    return valoreMedio_LaneOffset

