import numpy as np
import sys
import pickle

def calcSpeed(x):
    return (np.exp(0.5*x)/(1+np.exp(0.5*x)))+(15/(1+np.exp(0.5*x)))

#the environment
class Network:
    def __init__ (self,nVertex,networkMatrix,time,vehicle):
        self.nVertex=nVertex;
        self.networkMatrix=networkMatrix;
        self.time = time;
        self.vegicle = vehicle;
        self.vehicleCountOnRoad= np.zeros((10,10));
        self.events=[]

    def displaymatrix(self):
        print(self.networkMatrix)

    def calcVehicleCount(self):
        self.vehicleCount= len(time)
        print("there are ",self.vehicleCount," vehicles ")

    def getDist(x,y):
        return networkMatrix.item((x,y))


#the agent(s)
class Vehicle:
    def __init__(self,startNode,startTime,id,travelData):
        self.startNode=startNode
        self.currentNode = self.startNode
        self.startTime=startTime
        print("start node : ",self.startNode," start time: ",self.startTime)
        self.id= id
        self.travelData=travelData
        print(self.travelData)
        self.followingEvent=self.startTime

    def calcNextEvent(self,x):
        nextEvent=self.followingEvent


if __name__=="__main__":
    print("starting the programme");

    #loading the adjacency matrix of the road network
    netMat = pickle.load(open("roads/road.dat","r"))

    #loading the array which stores the time at which each vehicle starts from it's 
    time = pickle.load(open("roads/time","r"))

    #each vehicle will go through 5 nodes including the start
    vehicleTravelData = pickle.load(open("roads/vehicle","r"))

    roadNet=Network(10,netMat,time,vehicleTravelData)
    roadNet.displaymatrix();
    roadNet.calcVehicleCount();

    #loading the vehicle data
    vehicles = []
    for i in range(100):
        vehicles.append(   Vehicle(  vehicleTravelData.item((i,0))  ,time.item(i)  ,i  ,vehicleTravelData[i]  )   )



    #exiting the programme
    sys.exit(0)


