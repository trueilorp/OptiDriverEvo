import random, simulate, json, selNSGA2, algoritmoGenetico, crossover
from deap import base, creator, tools 
from math import sqrt
from driver import Driver
from deap import algorithms
from deap import base
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools

def muta_gene(driver):
    lista_geni =  driver.Lista_parametri
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

def default_driver_generate_value():
        with open('sim_config.json', 'r') as file:
            dati_json = json.load(file)
        sim_config = dati_json.get('Simone_Dario_SD_A4_2009_black', {})
        initial_driver = sim_config.get('initialDriver', None)
        with open('driver_config.json', 'r') as driver_file:
            driver_data = json.load(driver_file)
        driver_params = driver_data.get(initial_driver, {})
        lista_parametri = list(driver_params.values())
        return lista_parametri

def get_gens_of_driver():
    params_list = default_driver_generate_value()
    modify_value = random.uniform(BOUND_LOW, BOUND_UP/2)   
    for gen in range(len(params_list)-5):  # Utilizziamo un ciclo con gli indici
        operation = random.choice(['+', '-'])
        if operation == '+':            
            params_list[gen] = str(round((float(params_list[gen]) + modify_value),2))
        else:
            params_list[gen] = str(round((float(params_list[gen]) - modify_value),2))
    return params_list

def generate_driver():
    Driver.id_driver =+ 1
    gens_list = get_gens_of_driver()
    driver = creator.Individual(gens_list)
    return driver

def evaluate(driver, num_runs):
    print('\nSIMULATION NUMBER ' + str(num_runs) + '\n')
    timeSim, mediaLaneOffset = simulate.simulate(driver, num_runs)
    driver.fitness.values = (timeSim, mediaLaneOffset) 
    print("\n############FITNESS.VALUE###############\n" + str(driver.fitness.values) + "\n###########")

BOUND_LOW, BOUND_UP = 0.0, 1.0
NDIM = 22 # geni driver
NGEN = 5 # iterazioni 
MU = 4  # numero individui della popolazione
CXPB = 0.9

# Definizione del problema e dei tipi di fitness (essendo multi-objective ora devo minimizzare le due fitness)
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))  # Due funzioni di fitness
creator.create("Individual", Driver, fitness=creator.FitnessMulti)
toolbox = base.Toolbox()
# Creazione variabili --> def register(self, alias, function, *args, **kargs):
toolbox.register("individual", generate_driver)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mutate", algoritmoGenetico.muta_gene)
toolbox.register("mate", crossover.crossover_gens, low=BOUND_LOW, up=BOUND_UP, eta=20.0) 
# Operatori genetici
#toolbox.register("evaluate", evaluate)


def main_population_based(seed=None):

    random.seed(seed)

    # Creazione di una popolazione iniziale
    population = toolbox.population(MU)  # Creiamo una popolazione di 100 individui

    # Valutazione della popolazione iniziale (usa le tue due funzioni di fitness)
    for indice, individuo in enumerate(population):
        evaluate(individuo, indice) # Sostituisci con i tuoi valori effettivi per le due funzioni di fitness

    population = selNSGA2.selNSGA2(population, len(population))
    num_runs = 4
    num_generations = 1

    while num_generations <= NGEN:
        offspring = tools.selTournamentDCD(population, len(population)) #vuole due parametri: la popolazione e quanti individui tenere 
        offspring = [toolbox.clone(ind) for ind in offspring] #deep copy

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]): #itera gli offspring in coppia
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2) #crossover 

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        # Evaluate the individuals with an invalid fitness
        for ind in offspring:
            if not ind.fitness.valid: #per gli individui la cui fitness e' invalida 
                evaluate(individuo, num_runs)  #ri valu
                num_runs += 1

        print("Population:\n")
        for i, individuo in enumerate(population, 1):  # Partiamo dall'indice 1
            print(f"Individuo {i}: {individuo.parameters}")
        # Select the next generation population
        new_population = population + offspring
        print("\nNew population:\n")
        for i, individuo in enumerate(new_population, 1):  # Partiamo dall'indice 1
            print(f"Individuo {i}: {individuo.parameters}")

        population = selNSGA2.selNSGA2(new_population, MU)

        num_generations += 1
        
    print("Final drivers is " + str(population))
    return population

if __name__ == "__main__":
    pop = main_population_based()
