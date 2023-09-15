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
    indiceGeneDaModificare = random.randint(0, len(listaGeni) - 1) #scegli indice gene da mutare
    valoreDiModifica = 0

# or 0 <= (float(listaGeni[indiceGeneDaModificare]) + valoreDiModifica) <= 1
    while valoreDiModifica == 0:
        valoreDiModifica = random.uniform(-0.1, 0.1) #scelgo un valore di modifica che sta tra -0,1 e 0,1
    
    listaGeni[indiceGeneDaModificare] = str(float(listaGeni[indiceGeneDaModificare]) + valoreDiModifica) #modifico il parametro
    

'''def generaValoriDriver(listaValori):
    x = input("Inserisci il valore che vuoi mutare: ") #deve stare nell'intervallo tra 0 e 1
    for i in range(len(listaValori)):
        listaValori[i] = x
    listaValori[17] = "1"  
    listaValori[18] = "1"
    listaValori[19] = "1"
    listaValori[20] = "1"
    listaValori[21] = "1"
    '''

def sopravvivenzaDriver(FF1, FF2):
    if FF1 < FF2:
        return 1
    else:
        return 2

#normalizzazione delle fitness function

def FitnessFunction(ff1, ff2):
    #normalizzo prima i due valori 
    ff = ff1 + ff2
    return ff
