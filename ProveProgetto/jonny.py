import random

def simulate(driver):
    sim_time = random.random()
    lane_off = random.random()
    return sim_time, lane_off


def calc_ff(dsim_time, lane_offiver):
    return sim_time + lane_off


def mutate(driver):
    l = list(driver)
    random.shuffle(l)
    new_driver = ''.join(l)
    return new_driver
 

def compare(run, best_run):
    #run = runs[-1]
    if(run["ff"] > best_run["ff"]):
        best_run = run
    return best_run


def dump(run, best=False):
    if best:
        print("*** BEST")
    print("driver: " + run["driver"] + " - ff: " + str(run["ff"]) + " - st: " + str(run["sim_time"]) + " - lo: " + str(run["lane_off"]))


runs = []

driver = "DefaultDriver"
sim_time, lane_off = simulate(driver)
ff = calc_ff(sim_time, lane_off)
best_run = {"driver": driver, "sim_time": sim_time, "lane_off": lane_off, "ff": ff}
runs.append(best_run)

dump(best_run)

tot_runs = 10
num_runs = 1
while (num_runs < tot_runs):
    print("iteration #" + str(num_runs))
    new_driver = mutate(driver)
    sim_time, lane_off = simulate(new_driver)
    ff = calc_ff(sim_time, lane_off)
    new_run = {"driver": new_driver, "sim_time": sim_time, "lane_off": lane_off, "ff": ff}
    dump(new_run)
    runs.append(new_run)
    best_run = compare(new_run, best_run)
    dump(best_run, True)
    num_runs = num_runs + 1

best_driver = best_run["driver"]