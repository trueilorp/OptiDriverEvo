#22 valori
import random

def generaValoriDefaultDriver(listaGeni):
    for _ in range(22):
        listaGeni.append("0.50")
    listaGeni[17] = "1"
    listaGeni[18] = "1"
    listaGeni[19] = "1"
    listaGeni[20] = "1"
    listaGeni[21] = "1"

def mutaGene(listaGeni):
    indiceGeneDaModificare = random.randint(0, len(listaGeni) - 5) #scegli indice gene da mutare
    valoreDiModifica = 0
    while valoreDiModifica == 0: #per evitare che sia zero
        valoreDiModifica = random.uniform(-0.5, 0.5) #scelgo un valore di modifica che sta tra -0,1 e 0,1
    x = valoreDiModifica + float(listaGeni[indiceGeneDaModificare])
    if x >= 0 and x <= 1:
        listaGeni[indiceGeneDaModificare] = str(x) #modifico il parametro

def sopravvivenzaDriver(FF1, FF2):
    if FF1 < FF2:
        return 1
    else:
        return 2

#normalizzazione delle fitness function
def normalizzaTimeSim(fftimesim):
    min_tempo_simulazione = 0.0  # Valore minimo per tempoSimulazione
    max_tempo_simulazione = 100.0  # Valore massimo per tempoSimulazione
    tempoSimulazione_normalizzato = (fftimesim - min_tempo_simulazione) / (max_tempo_simulazione - min_tempo_simulazione)
    return tempoSimulazione_normalizzato

#da definire max e min quando trovo la width lane 
def normalizzaLaneOffset(fflaneoffset):
    min_lane_offset = -2.0  # Valore minimo per laneOffset
    max_lane_offset = 5.0  # Valore massimo per laneOffset
    laneOffset_normalizzato = (fflaneoffset - min_lane_offset) / (max_lane_offset - min_lane_offset)
    return laneOffset_normalizzato

def FitnessFunction(ff1, ff2):
    #x = normalizzaTimeSim(ff1)
    #y = normalizzaLaneOffset(ff2) 
    ff = ff1 + ff2
    return ff
