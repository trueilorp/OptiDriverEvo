import csv
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

    # Converti i dati in float, perche altrimenti mi da il risultato sbagliato
    timeSim_column = [float(value) for value in timeSim_column]
    # Prendo il massimo valore
    timeSimulation = max(timeSim_column)
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

    # Calcolo la media dei valori del laneOffset
    laneOffset_column_float = [float(stringa) for stringa in laneOffset_column] #prima converto la lista in float
    valoreMedio_LaneOffset = sum(laneOffset_column_float) / len(laneOffset_column_float)
    return valoreMedio_LaneOffset

