import driver 

if __name__ == "__main__":
    driverDefault = driver.Driver(0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50, True, True, True, True)
    #faccio partire la simulazione con questo driver
    #mi faccio tornare LaneOffset e TimePath
    tp = input("Inserisci timePath: ")
    lo = input("Inserisci laneOffset: ")
    driverDefault.setTimePath(tp)
    driverDefault.setLaneOffset(lo)
    driverDefault.mutateDriver()
    