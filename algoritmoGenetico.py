import random, copy

###############
# GA MUTATION #
###############

######################
# PARAMETERS TO MUTATE:
# DesiredVelocity, DesiredAcceleration, DesiredDeceleration, 
# CurveBehavior, ObserveSpeedLimits, LaneKeeping, SpeedKeeping
#######################

def mutate(driver):
    gens =  copy.deepcopy(driver.parameters)
    range = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (6, 6), (7, 7)]
    choose_range = random.choice(range)
    low_bound, upper_bound = choose_range
    gen_to_modify_index = random.randint(low_bound, upper_bound) #scegli indice gene da mutare
    if 17 <= gen_to_modify_index <= 21:
        if gens[gen_to_modify_index] == "1":
            gens[gen_to_modify_index] = "0"
        else:
            gens[gen_to_modify_index] = "1"
    else:
        value_of_modify = 0
        value_modified = value_of_modify + float(gens[gen_to_modify_index])
        while (value_of_modify == 0) or (value_modified < 0 or value_modified > 1): #per evitare che sia zero o che sfori 
            value_of_modify = round(random.uniform(-0.5, 0.5),2) #scelgo un valore di modifica che sta tra -0,1 e 0,1
            value_modified = value_of_modify + float(gens[gen_to_modify_index])
        
        gens[gen_to_modify_index] = "{:.2f}".format(value_modified) #modifico il parametro
    return gens

def get_best_driver(driver_parent, driver_offspr):  #copio oggetti 
    if driver_parent.total_fitness_function < driver_offspr.total_fitness_function:
        print("\nSOPRAVVIVE OFFSPRING")
        print("Lista parametri nuovo Parent" + str(driver_offspr.parameters))
        #return copy.deepcopy(driver_offspr)
        return driver_offspr
    else:
        print("\nSOPRAVVIVE PARENT")
        print("Lista parametri Parent" + str(driver_parent.parameters))
        return driver_parent