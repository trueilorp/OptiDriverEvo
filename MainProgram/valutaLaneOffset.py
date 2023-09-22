import pandas as pd
import openpyxl
import time
from ClasseDriver import driver2

# Imposta il percorso del tuo file Excel
file_path = 'Dati_rdbSniffer.csv'

# Imposta il nome della colonna che desideri leggere
nome_colonna ='laneOffset'

while True:
    try:
        # Carica il file Excel utilizzando openpyxl per consentire l'accesso in tempo reale
        excel_file = openpyxl.load_workbook(file_path, data_only=True)
        
        # Accedi al foglio di lavoro che contiene i dati
        foglio_lavoro = excel_file.active
        
        # Leggi la colonna specifica
        dati_colonna = [row[0].value for row in foglio_lavoro.iter_rows(min_col=foglio_lavoro[nome_colonna].column,
                                                                      max_col=foglio_lavoro[nome_colonna].column,
                                                                      min_row=2)]  # Parti dalla seconda riga
        
        # Crea un DataFrame pandas
        df = pd.DataFrame({nome_colonna: dati_colonna})
        
        # Esegui operazioni sui dati come desiderato
        for indice, riga in df.iterrows():
            valore = riga['laneOffset']
            check = driver2.Driver.computeLaneOffset(valore)
            if check == 0:
                print("Interrompi simulazione")

        # Chiudi il file Excel
        excel_file.close()
        
        # Attendi un certo intervallo prima di leggere di nuovo
        ##time.sleep(5)  # Attendi 5 secondi prima di leggere di nuovo
    except Exception as e:
        print(f"Errore durante la lettura del file Excel: {e}")

