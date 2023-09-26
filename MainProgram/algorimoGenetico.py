#22 valori
import random
import openpyxl
from NormalizzaDati import TimeSimNormalizzato
from NormalizzaDati import LaneOffsetNormalizzato

def generaValoriDefaultDriver(listaGeni):
    for _ in range(22):
        listaGeni.append("0.50")
    listaGeni[17] = "1"
    listaGeni[18] = "1"
    listaGeni[19] = "1"
    listaGeni[20] = "1"
    listaGeni[21] = "1"

def mutaGene(listaGeni):
    indiceGeneDaModificare = random.randint(0, len(listaGeni)-1) #scegli indice gene da mutare
    if 17 <= indiceGeneDaModificare <= 21:
        if listaGeni[indiceGeneDaModificare] == "1":
            listaGeni[indiceGeneDaModificare] = "0"
        else:
            listaGeni[indiceGeneDaModificare] = "1"
    else:
        valoreDiModifica = 0
        x = valoreDiModifica + float(listaGeni[indiceGeneDaModificare])
        while (valoreDiModifica == 0) or (x < 0 or x > 1): #per evitare che sia zero o che sfori 
            valoreDiModifica = round(random.uniform(-0.5, 0.5),2) #scelgo un valore di modifica che sta tra -0,1 e 0,1
            x = valoreDiModifica + float(listaGeni[indiceGeneDaModificare])
        
        listaGeni[indiceGeneDaModificare] = "{:.2f}".format(x) #modifico il parametro

def sopravvivenzaDriver(FF1, FF2):
    if FF1 <= FF2:
        return 1
    else:
        return 2

#normalizzazione delle fitness function
def normalizzaTimeSim(timeSim, i):
    timeSimNormalizzato = TimeSimNormalizzato.normalizzaTS(timeSim, i)
    return timeSimNormalizzato

#da definire max e min quando trovo la width lane 
def normalizzaLaneOffset(laneOffset, i):
    laneOffsetNormalizzato = LaneOffsetNormalizzato.normalizzaLO(laneOffset, i)
    return laneOffsetNormalizzato

def FitnessFunction(ts, mlo, i):
    x = normalizzaTimeSim(ts, i)
    y = normalizzaLaneOffset(mlo, i) 
    ff = x + y
    return ff
