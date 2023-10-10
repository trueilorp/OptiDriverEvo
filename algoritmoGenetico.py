#22 valori
import random, copy

def muta_gene(driver):
    lista_geni =  copy.deepcopy(driver.Lista_parametri)
    #intervalli = [(0, 3), (6, 8), (13, 13)]
    #intervallo_scelto = random.choice(intervalli)
    indice_gene_da_modificare = random.randint(0,3) #scegli indice gene da mutare
    if 17 <= indice_gene_da_modificare <= 21:
        if lista_geni[indice_gene_da_modificare] == "1":
            lista_geni[indice_gene_da_modificare] = "0"
        else:
            lista_geni[indice_gene_da_modificare] = "1"
    else:
        valore_di_modifica = 0
        valore_modificato = valore_di_modifica + float(lista_geni[indice_gene_da_modificare])
        while (valore_di_modifica == 0) or (valore_modificato < 0 or valore_modificato > 1): #per evitare che sia zero o che sfori 
            valore_di_modifica = round(random.uniform(-0.5, 0.5),2) #scelgo un valore di modifica che sta tra -0,1 e 0,1
            valore_modificato = valore_di_modifica + float(lista_geni[indice_gene_da_modificare])
        
        lista_geni[indice_gene_da_modificare] = "{:.2f}".format(valore_modificato) #modifico il parametro
    return lista_geni

def get_best_driver(driver_parent, driver_offspr):  #copio oggetti 
    if driver_parent.Fitness_function_totale < driver_offspr.Fitness_function_totale:
        print("\nSOPRAVVIVE OFFSPRING")
        print("Lista parametri nuovo Parent" + str(driver_offspr.Lista_parametri))
        return copy.deepcopy(driver_offspr)
    else:
        print("\nSOPRAVVIVE PARENT")
        print("Lista parametri Parent" + str(driver_parent.Lista_parametri))
        return driver_parent