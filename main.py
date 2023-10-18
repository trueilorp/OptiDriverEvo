import random, simulate, json, selNSGA2, crossover, logging, dumpPopulation, algoritmoGenetico, numpy as np, matplotlib as plt
from deap import base, creator, tools 
from math import sqrt
from driver import Driver
from deap import algorithms
from deap import base
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools
logging.getLogger('matplotlib').setLevel(logging.WARNING)

# how to plot Pareto Front:
# https://notebook.community/locie/locie_notebook/ml/multiobjective_optimization

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)


def get_costants_of_ga():
    with open('/home/udineoffice/Desktop/SimulationLauncher_PopulationBased/config.json', 'r') as file:
        config = json.load(file)
    return config["numberOfGenerations"], config["numberOfIndividuals"], config["numberOfGens"], config["boundLow"],config["boundUp"], config["probabilityOfCrossover"] 

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
    modify_value = random.uniform(0.0, 0.3)   
    for gen in range(len(params_list)-5):  # Utilizziamo un ciclo con gli indici
        operation = random.choice(['+', '-'])
        if operation == '+':            
            params_list[gen] = str(round((float(params_list[gen]) + modify_value),2))
        else:
            params_list[gen] = str(round((float(params_list[gen]) - modify_value),2))
    return params_list

def generate_driver():
    gens_list = get_gens_of_driver()
    driver = creator.Individual(gens_list)
    return driver

def evaluate(driver, num_runs):
    print('\nSIMULATION NUMBER ' + str(num_runs) + '\n')
    timeSim, mediaLaneOffset = simulate.simulate(driver, num_runs)
    driver.fitness.values = (timeSim, mediaLaneOffset) 
    print("\n############FITNESS VALUE###############\n" + str(driver.fitness.values) + "\n###############################")

NGEN, MU, NDIM, BOUND_LOW, BOUND_UP, CXPB = get_costants_of_ga() # numero generazioni, numero individui della popolazione 

# Definizione del problema e dei tipi di fitness (essendo multi-objective ora devo minimizzare le due fitness)
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))  # Due funzioni di fitness
creator.create("Individual", Driver, fitness=creator.FitnessMulti)
toolbox = base.Toolbox()
# Creazione variabili --> def register(self, alias, function, *args, **kargs):
toolbox.register("individual", generate_driver)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mutate", algoritmoGenetico.mutate_individual)
toolbox.register("mate", crossover.crossover_gens, low=BOUND_LOW, up=BOUND_UP, eta=20.0) 
# Operatori genetici
#toolbox.register("evaluate", evaluate)


def get_best_population(seed=None):

    random.seed(seed)
    best_population = []
    # Creazione di una popolazione iniziale
    population = toolbox.population(MU)  # Creiamo una popolazione di 100 individui
    best_population.append(population)

    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    # Valutazione della popolazione iniziale (usa le tue due funzioni di fitness)
    for indice, individuo in enumerate(population):
        evaluate(individuo, indice+1) # Sostituisci con i tuoi valori effettivi per le due funzioni di fitness

    population = selNSGA2.selNSGA2(population, len(population))

    num_runs = MU + 1
    num_generations = 1
    while num_generations <= NGEN:
        # Vary the population
        # La + basata su torneo coinvolge la scelta casuale di un certo numero di individui (generalmente due) 
        # dalla popolazione corrente. Gli individui selezionati partecipano a un "torneo", e quello con la fitness migliore 
        # viene selezionato come genitore per la generazione successiva. Questo processo viene ripetuto per creare tutti 
        # gli individui della generazione successiva.
        offspring = selNSGA2.selTournamentDCD(population, len(population)) #seleziona t offspring in numero sempre minore alla popsize
        offspring = [toolbox.clone(ind) for ind in offspring] #deep copy

        #Nuovi ID per i driver 
        for i,off in enumerate(offspring):
            off.id_driver = num_generations * MU + i + 1

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]): #itera gli offspring in coppia
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2) #crossover 

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
            # Alla fine del processo di crossover e mutazione, le fitness dei nuovi genitori vengono contrassegnate come non 
            # valide (fitness.values viene eliminato) perché le loro caratteristiche genetiche sono state modificate. 
            # Questo significa che durante la prossima valutazione della fitness, i nuovi valori di fitness verranno 
            # calcolati per questi individui.
           
        # Evaluate the individuals with an invalid fitness
        for ind in offspring:
            if not ind.fitness.valid: #per gli individui la cui fitness e' invalida 
                evaluate(ind, num_runs)  #ri valu
                num_runs += 1

        print("Population:")
        for i, individuo in enumerate(population, 1):  # Partiamo dall'indice 1
            print(f"Individuo {i}: {individuo.fitness.values}")
        # Select the next generation population
        new_population = population + offspring
        print("\nNew population:")
        for i, individuo in enumerate(new_population, 1):  # Partiamo dall'indice 1
            print(f"Individuo {i}: {individuo.fitness.values}")

        population = selNSGA2.selNSGA2(new_population, MU)

        best_population.append(population) #ogni giro mi da la popolazione migliore 
        result_data = stats.compile(population)

        dumpPopulation.dump_population_inside_while(new_population) 

        num_generations += 1       
    #print("Final population is " + str(population))
    print(result_data)
    return population, best_population

if __name__ == "__main__":
    
    final_population, best_population = get_best_population()
    dumpPopulation.dump_population_inside_while(final_population) 
    dumpPopulation.dump_population(best_population) 

    pop, log = algorithms.eaSimple(best_population, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, stats=stats, halloffame=None, verbose=True)
    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")
    plt.show()   