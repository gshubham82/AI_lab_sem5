import numpy as np
import sys
import pickle

def getEventTime(evnt):
    return evnt[0]

def calcSpeed(x):
    return (np.exp(0.5*x)/(1+np.exp(0.5*x)))+(15/(1+np.exp(0.5*x)))

#the environment
# environment store the following datas
# graph corresponding tom length of each roads in the raod network
# number of vehicles per road
# reference of each vehicle so that they can be called later when each one's event arrives to perform
# the next action
#=================
class Network:
    def __init__ (self,nVertex,networkMatrix,time,vehicleTravelData):
        #number of vertecies
        self.nVertex=nVertex;

        #the network matrix
        self.networkMatrix=networkMatrix;

        #stores the time array at which each vehicle will start it's journey
        self.time = time;

        #store the array of nodes throgh which vehicle travels
        self.vehicleTravelData = vehicleTravelData;

        #store the number of vehicles on the road i,j as a matrix of the same dimension as roadNetwork
        self.vehicleCountOnRoad= np.zeros((10,10));

        #the event array for calculating event driven actions
        #event array consists of tuples of the format (time,id_of_car)
        #brute force defenition of for loop because number of elements in array is already known
        self.events=[]
        for i in range(0,100):
            self.events.append((time[i],i))
            print(time[i],i)

    #this is used by the agent(vehicle) to get the current distance of the raod in which it is travelling
    def getDist(self,x,y):
        return self.networkMatrix.item((x,y))

    #used by agent to get the vehicle density in the road (x,y)
    def getVehicleDensity(self,x,y):
        return self.vehicleCountOnRoad.item((x,y))

    #executing the next event in event queue
    def executeNextEvent(self):
        #sorting the event array to get the next event to be executed
        self.events.sort(key=getEventTime)
        #taking the least element (ie, the next event to be executed)
        nextEventToExec=self.events.pop(0)
        print("next event: ",nextEventToExec)

        #calling the agent to perform the appropriate action
        #extracting carID
        carID=nextEventToExec[1]
        #event to push is the next event which is returned by the vehicle after it performs this event
        eventToPush=self.vehicles[carID].calcNextEvent()

        #event push is -1 when vehicle reaches the end so such events are discarded
        if not eventToPush == -1:
            #appending the event queue with event returned by agent this need not be sorted because
            #while accessing this function it first sorts the queue anyway
            self.events.append((eventToPush,carID))

    #used by agents when they enter any road
    def addCarInRoad(self,x,y):
        self.vehicleCountOnRoad[x][y]=self.vehicleCountOnRoad[x][y]+1

    #used by agents when they leave a road
    def removeCarOnRoad(self,x,y):
        self.vehicleCountOnRoad[x][y]=self.vehicleCountOnRoad[x][y]-1

    #all vehicles have reached their endpoints when the event queue is empty
    def isDone(self):
        if len(self.events)==0:
            return 1
        else:
            return 0

    #vehicle array cannot be added in the constructor because construccting the vehicle array
    #needs reference to the roadNet object so the roadnet is later populated with vehicle data
    def addVehicleArray(self,vehicle):
        self.vehicles=vehicle


#the agent(s)
#agent contains datas like current node(location) path(set of nodes) to be traveled
#and an array of times representing the time at which it reached the node (array is called reachTimes)
#there will be multiple agents in this examples all of which interacts with environment
#=====================
class Vehicle:
    def __init__(self,startNode,startTime,id,travelData,roadNetwork):
        #starting node ie, the first one in the path
        self.startNode=startNode

        #initialised with startnode
        self.currentNode = self.startNode

        #from the given data
        self.startTime=startTime

        #print("start node : ",self.startNode," start time: ",self.startTime)
        #storing the id of the object inside itself so that it can be refered later
        self.id= id

        #the path through which the agent travels
        self.travelData=travelData

        #print(self.travelData)
        #the followin event initaily will be the car staring at it's respective star time
        self.followingEvent=self.startTime

        #reference of the environment so that the car can access certain functions like
        #the ones which were pointed out in the environment class
        self.roadNetwork=roadNetwork

        #the position in the path goes from 0 to 4
        self.position=0

        #the array which stores the time at which agent reaches each node contains five elements by
        #the end of the program
        self.reachTimes=[]
        self.reachTimes.append(self.followingEvent)

    def calcNextEvent(self):
        p=self.position
        if p == 4:
            #the agent has reached end of it's path
            #NodeNow and NodePrev represents the two nodes in the path
            NodeNow=self.travelData.item(p)
            NodePrev=self.travelData.item(p-1)
            #so we remove the agent from the road by decreasing the vehicle density(see environment class)
            self.roadNetwork.removeCarOnRoad(NodePrev,NodeNow)
            #returns -1 because no more events to be procesed next (see environment class)
            return -1
        else:
            #consecutive nodes in path
            NodeNow=self.travelData.item(p)
            NodeNext=self.travelData.item(p+1)
            if p>0:
                #for all times except the starting time where ther is no previous node
                NodePrev=self.travelData.item(p-1)
                #removing agent from current road
                self.roadNetwork.removeCarOnRoad(NodePrev,NodeNow)
            #ading agent in the next road
            self.roadNetwork.addCarInRoad(NodeNow,NodeNext)
            #distance obtained from environment
            distance=self.roadNetwork.getDist(NodeNow,NodeNext)
            #x is the vehicle density obtained from environment
            x=self.roadNetwork.getVehicleDensity(NodeNow,NodeNext)
            #time at which next event is to be happened
            nextEvent=self.followingEvent+(distance/calcSpeed(x))
            #updating event and position data
            self.followingEvent=nextEvent
            #appending the calculated time into the array
            self.reachTimes.append(self.followingEvent)
            self.position=self.position+1
            #returning the value to the environment so that it can append it on the event queue
            #(see environment class)
            return nextEvent


if __name__=="__main__":
    print("starting the programme");

    #loading the adjacency matrix of the road network
    #netMat = pickle.load(open("roads/road","r"))
    netMat = np.load("roads/road")

    #loading the array which stores the time at which each vehicle starts from it's 
    #time = pickle.load(open("roads/time","r"))
    time = np.load("roads/time",encoding='latin1')

    #each vehicle will go through 5 nodes including the start
    #vehicleTravelData = pickle.load(open("roads/vehicle","r"))
    vehicleTravelData = np.load("roads/vehicle")

    roadNet=Network(10,netMat,time,vehicleTravelData)
    #roadNet.calcVehicleCount();

    #loading the vehicle data
    vehicles = []
    for i in range(100):
        vehicles.append(   Vehicle(  vehicleTravelData.item((i,0))  ,time.item(i)  ,i  ,vehicleTravelData[i]  ,roadNet  )   )

    roadNet.addVehicleArray(vehicles)

    print("starting event calculations")
    while not roadNet.isDone():
        roadNet.executeNextEvent()
    
    for i in vehicles:
        print(i.reachTimes)

    #print(roadNet.vehicleCountOnRoad)
    #print(netMat)

    #exiting the programme
    sys.exit(0)
