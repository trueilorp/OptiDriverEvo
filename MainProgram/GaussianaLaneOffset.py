import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os
import subprocess, logging, os, time, datetime, shutil, random, string, sys, glob
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
import SelectFromCSV


def gaussiana(x, mu, sigma):
    return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

colonne_fisse = ['laneOffset (cm)'] 
# Carica il file Excel in un DataFrame
df = pd.read_excel('/home/udineoffice/Desktop/dati.xlsx')
# Assumi che i dati siano nella colonna "Dati"
i=0
data = datetime.datetime.now() #prendo il tempo di inizio simulazione
cartella_radice = '/home/udineoffice/Desktop/Grafici_Gauss'
nome_sottocartella = 'Grafici Lane Offset ' + str(data)
cartella = os.path.join(cartella_radice, nome_sottocartella)
os.makedirs(cartella)

while(i<16):
    start_row = 0  # L'indice delle righe inizia da 0
    end_row = i  # L'indice delle righe inizia da 0
    # Estrai l'intervallo specificato di righe dal DataFrame
    dati = df.loc[start_row:end_row, colonne_fisse]
    print("\nDATI: " + str(dati))
    print('\n')
    #dati = df['travelTime (s)']
    media = dati.mean()
    deviazione_std = dati.std()
    print("MEDIA" + str(media))
    print("DEVIAZIONE STD" + str(deviazione_std))
    print('\n')
    # Calcola i valori della funzione gaussiana per i punti x dati
    y = 1 - gaussiana(dati, media, deviazione_std)
    print("VALORE NORMALIZZATO" + str(y))
    # Visualizza la funzione gaussiana
    plt.plot(dati, y)
    plt.title('Funzione Gaussiana')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)

    nome_grafico = f'grafico_iterazione_{i + 1}.png'
    percorso_grafico = os.path.join(cartella, nome_grafico)
    plt.savefig(percorso_grafico)

    plt.close()

    #plt.show()
    i = i + 1
    
