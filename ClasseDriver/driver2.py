import numpy as np
import random

class Driver:

    #driverConfig = np.array([0,0,0,0,0,0,0,0,0,0,0,0])

    WIDTHLANE = 14

    def __init__(self, lg):
       self.listaGeni = lg
       self.LaneOffset = 0
       self.timePath = 0
    
    def setGeni(self, lista):
        self.listaGeni = lista

    def computeLaneOffset (self, dist):
        self.LaneOffset = (self.WIDTHLANE/2) + abs (dist)
    
    def setLaneOffset(self, lo):
        self.LaneOffset = lo

    def setTimePath(self, tp):
         self.timePath = tp
        
    def creaListaParametriDriver(self):
        listAttributi = [self.DesiredVelocity,self.DesiderAcceleration, self.DesiderDeceleration,
        self.CurveSpeed, self.ObserveSpeedLimit ,self.DistanceKeeping,
        self.LaneKeeping, self.SpeedKeeping, self.LaneChangeDynamic, self.UrgeToOvertake,
        self.RespondToTailgatingVehicles , self.ForesightDistance,
        self.SteeringIndicator,
        self.ObserveKeepRightRule ,
        self.ConsiderEnvConditions ,
        self.UseOfIndicator ,
        self.ReactionTime,]

        return listAttributi

    def mutateDriver (self):
        listAttributi = self.creaListaParametriDriver()
        parametroDaModificare = random.choice(listAttributi)
        
        valoreDiModifica = random.uniform(-0.1, 0.1)#scelgo un valore di modifica che sta tra 0,01 e 0,1
        parametroDaModificare = parametroDaModificare + valoreDiModifica #modifico il parametro
        
        #controlla se la mutazione mi va bene 
        #if valoreDiModifica == 0 or parametroDaModificare > 1 or parametroDaModificare < 0:
            #rifai mutazione 
        print(listAttributi)

