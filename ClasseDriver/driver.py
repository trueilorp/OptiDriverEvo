import numpy as np
import random

class Driver:

    #driverConfig = np.array([0,0,0,0,0,0,0,0,0,0,0,0])

    LaneOffset = 0 ##Fitness Function 1 
    timePath = 0 #Fitness Function 2

    WIDTHLANE = 14

    def __init__(self, dv, da, dd, cs, osl, dk, lk, sk, lcd, uto, rttv, fd, si, okrr, cec, uoi, rt, ots, otl, s, ra):
       self.DesiredVelocity = dv
       self.DesiderAcceleration = da
       self.DesiderDeceleration = dd
       self.CurveSpeed = cs
       self.ObserveSpeedLimit = osl
       self.DistanceKeeping = dk
       self.LaneKeeping = lk
       self.SpeedKeeping = sk
       self.LaneChangeDynamic = lcd
       self.UrgeToOvertake = uto
       self.RespondToTailgatingVehicles = rttv
       self.ForesightDistance = fd
       self.SteeringIndicator = si
       self.ObserveKeepRightRule = okrr
       self.ConsiderEnvConditions = cec
       self.UseOfIndicator = uoi
       self.ReactionTime = rt
       self.ObeyTrafficSigns = ots
       self.ObeyTrafficLights = otl
       self.Swarm = s
       self.RouteAdherence = ra

    def computeLaneOffset (self, dist):
        self.LaneOffset = (self.WIDTHLANE/2) + abs (dist)

    def getLaneOffset(self):
        return self.LaneOffset
        
    def getTimePath(self):
        return self.timePath
    
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

