import random, simulate, json, logging, dumpPopulation, algoritmoGenetico, numpy as np, datetime
from deap import base, creator, tools 
from math import sqrt
from driver import Driver
from deap import base
from deap import creator
from deap import tools
logging.getLogger('matplotlib').setLevel(logging.WARNING)

def get_ga_costants():
    with open('/home/udineoffice/Desktop/OptiDriverEvo_PopulationBased/config.json', 'r') as file:
        config = json.load(file)
    return config["numberOfGenerations"], config["numberOfIndividuals"],\
            config["numberOfGens"], config["boundLow"],config["boundUp"],\
            config["probabilityOfCrossover"], config["probabilityOfMutation"] 

def get_initial_driver():
    with open('sim_config.json', 'r') as file:
        dati_json = json.load(file)
    sim_config = dati_json.get('Simone_Dario_SD_A4_2009_black', {})
    initial_driver = sim_config.get('initialDriver', None)
    with open('driver_config.json', 'r') as driver_file:
        driver_data = json.load(driver_file)
    driver_params = driver_data.get(initial_driver, {})
    lista_parametri = list(driver_params.values())
    return Driver(lista_parametri)

def generate_initial_individuals():
    initial_driver = get_initial_driver()
    gens_of_initial_driver = toolbox.mutate(initial_driver)    
    return creator.Individual(gens_of_initial_driver)

def evaluate(driver, num_runs):
    print('\nSIMULATION NUMBER ' + str(num_runs) + '\n')
    timeSim, mediaLaneOffset = simulate.simulate(driver, num_runs)
    driver.fitness.values = (timeSim, mediaLaneOffset) 

NGEN, MU, NDIM, BOUND_LOW, BOUND_UP, CXPB, MUTOPROB = get_ga_costants()

creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0)) 
creator.create("Individual", Driver, fitness=creator.FitnessMulti)
toolbox = base.Toolbox()
toolbox.register("individual", generate_initial_individuals)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mutate", algoritmoGenetico.mutate_individual)
toolbox.register("mate", algoritmoGenetico.crossover_gens, low=BOUND_LOW, up=BOUND_UP, eta=20.0) 

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("min", np.min, axis=0)
stats.register("max", np.max, axis=0)
stats.register("avg", np.mean, axis=0)
stats.register("std", np.std, axis=0)
logbook = tools.Logbook()

def pop_based_NSGA2():
    num_generations = 0
    best_populations = []

    population = toolbox.population(MU) 
    Driver.set_id_drivers(population, 0, num_generations)
    best_populations.append(population)

    for indice, individuo in enumerate(population):
        evaluate(individuo, indice+1)

    population = algoritmoGenetico.selNSGA2(population, len(population))

    record = stats.compile(population)
    logbook.record(gen=num_generations, evals=MU, **record)

    num_runs = MU + 1
    num_generations += 1
    while num_generations <= NGEN:
        
        offspring = algoritmoGenetico.selTournamentDCD(population, len(population)) #select t offspring with t < popsize
        offspring = [toolbox.clone(ind) for ind in offspring] #deep copy
        
        Driver.set_id_drivers(offspring, MU, num_generations)

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]): #iterate offsprings pair
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2) #crossover 

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
           
        for ind in offspring: #evaluate the individuals with an invalid fitness
            if not ind.fitness.valid:
                evaluate(ind, num_runs) 
                num_runs += 1

        new_population = population + offspring #select the next generation population
        population = algoritmoGenetico.selNSGA2(new_population, MU)
        best_populations.append(population)

        record = stats.compile(population) #update the statistics with the new population
        logbook.record(gen=num_generations, evals=len(new_population), **record)
        num_generations += 1       
    
    return best_populations

def pop_based_random():
    num_generations = 0
    best_populations = []
    population = toolbox.population(MU)  
    Driver.set_id_drivers(population, 0, num_generations)
    
    for indice, individuo in enumerate(population):
        evaluate(individuo, indice+1) 

    best_populations.append(population)
    record = stats.compile(population)
    logbook.record(gen=num_generations, evals=MU, **record)

    num_runs = MU + 1
    num_generations += 1
    while num_generations <= NGEN:
        offspring = [toolbox.clone(ind) for ind in population] #deep copy

        Driver.set_id_drivers(offspring, MU, num_generations)

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]): #iterate offsprings in pair
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2) #crossover 

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
           
        
        for ind in offspring: #evaluate the individuals with an invalid fitness
            if not ind.fitness.valid:
                evaluate(ind, num_runs) 
                num_runs += 1

        population = offspring #select the next generation population
        best_populations.append(population) 

        record = stats.compile(population) #update the statistics with the new population
        logbook.record(gen=num_generations, evals=len(population), **record)
        num_generations += 1       
    
    return best_populations

if __name__ == "__main__":    
    time_beginning_of_program = datetime.datetime.now()
    with open('/home/udineoffice/Desktop/OptiDriverEvo_PopulationBased/sim_config.json', 'r') as file:
        method_simulation = json.load(file)
        sim_config = method_simulation.get('Simone_Dario_SD_A4_2009_black', {})
    try:
        if sim_config["methodOfSimulation"] == "NSGA2":
            best_populations = pop_based_NSGA2()
        elif sim_config["methodOfSimulation"] == "Random":
            best_populations = pop_based_random()
    except KeyError:
        print("Key 'methodOfSimulation' is not in file sim_conf.json")
    
    dumpPopulation.dump_best_populations(best_populations, logbook) 
    duration = datetime.datetime.now() - time_beginning_of_program
    print('\n\nTOTAL TIME ELAPSED -> ' + "{:.2f}".format(duration.total_seconds()/60) + 'min')
    print("ALL DONE!")