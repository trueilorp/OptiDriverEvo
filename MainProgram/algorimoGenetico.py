#22 valori

def generaValoriDefaultDriver(listaValori):
    for _ in range(22):
        listaValori.append("0.50")
    listaValori[17] = "1"
    listaValori[18] = "1"
    listaValori[19] = "1"
    listaValori[20] = "1"
    listaValori[21] = "1"

def scegliValoreDaMutare():
    return

def generaValoriDriver(listaValori):
    x = input("Inserisci il valore che vuoi mutare: ") #deve stare nell'intervallo tra 0 e 1
    for i in range(len(listaValori)):
        listaValori[i] = x
    listaValori[17] = "1"
    listaValori[18] = "1"
    listaValori[19] = "1"
    listaValori[20] = "1"
    listaValori[21] = "1"