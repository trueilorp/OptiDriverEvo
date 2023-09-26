import numpy as np
import random

class Driver:

    #driverConfig = np.array([0,0,0,0,0,0,0,0,0,0,0,0])

    WIDTHLANE = 3.500 #ho verificato dallo scenario editor 

    def __init__(self, lg):
       self.listaGeni = lg
       self.LaneOffset = 0
       self.timePath = 0
    
    def setGeni(self, lista):
        self.listaGeni = lista

    def setLaneOffset(self, lo):
        self.LaneOffset = lo

    def setTimePath(self, tp):
         self.timePath = tp

# Controllo se va fuori strada andando a calcolarmi la meta' della strada e poi vedo se il check e' minore o maggiore di 0
    def computeLaneOffset (self, laneOffsetTimeStamp):
        check = (self.WIDTHLANE/2) - abs (laneOffsetTimeStamp)
        if check < 0:
            return 0 # vuol dire che e' fuoristrada
        else:
            print("apposto")
        
    """def creaListaParametriDriver(self):
        listAttributi = [self.DesiredVelocity,self.DesiderAcceleration, self.DesiderDeceleration,
        self.CurveSpeed, self.ObserveSpeedLimit ,self.DistanceKeeping,
        self.LaneKeeping, self.SpeedKeeping, self.LaneChangeDynamic, self.UrgeToOvertake,
        self.RespondToTailgatingVehicles , self.ForesightDistance,
        self.SteeringIndicator,
        self.ObserveKeepRightRule ,
        self.ConsiderEnvConditions ,
        self.UseOfIndicator ,
        self.ReactionTime,]

        return listAttributi"""


