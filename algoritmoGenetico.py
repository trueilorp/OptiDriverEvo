#22 valori
import random, copy

def mutaGene(driver):
    listaGeni =  copy.deepcopy(driver.Lista_parametri)
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
    return listaGeni

def setNewDriverParent(driverParent, driverOffspring): 
    ffParent = driverParent.Fitness_function_totale
    ffOffspring = driverOffspring.Fitness_function_totale
    if (ffParent > ffOffspring): #sopravvive parent
        print("\nSOPRAVVIVE PARENT") 
        driverParent.Lista_parametri = driverParent.Lista_parametri
        driverParent.setPerformance(driverParent.TimeSim, driverParent.LaneOffset)
        driverParent.Fitness_function_totale = driverParent.Fitness_function_totale
        print("Lista parametri Parent" + str(driverParent.Lista_parametri))
    else:
        print("\nSOPRAVVIVE OFFSPRING")
        driverParent.Lista_parametri = driverOffspring.Lista_parametri
        driverParent.setPerformance(driverOffspring.TimeSim, driverParent.LaneOffset)
        driverParent.Fitness_function_totale = driverOffspring.Fitness_function_totale
        print("Lista parametri nuovo Parent" + str(driverOffspring.Lista_parametri))
