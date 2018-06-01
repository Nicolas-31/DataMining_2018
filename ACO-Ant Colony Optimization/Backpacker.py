
import random
import math
from matplotlib import pyplot as plt

MAXPHEROMONES = 1000000
MINPHEROMONES = 1
EVAPORATION = 0.99
MINEDGES = 9

#added new class City to original
# Country,City,AccentCity,Region,Population,Latitude,Longitude
class City:
    def __init__(self, line):
        self.countryCode = self.getItem(line, 0)
        self.city = self.getItem(line, 1)
        self.accentCity = self.getItem(line, 2)
        self.region = self.getItem(line, 3)
        self.population = self.getItem(line, 4)
        self.latitude = float(self.getItem(line, 5))
        self.longitude = float(self.getItem(line, 6))

    def getItem(self, line, n):
        parts = line.split(",")
        return parts[n]

    # Simplified. Should use great circle.
    def getLength(self, otherCity):
        dx = self.longitude - otherCity.longitude
        dy = self.latitude - otherCity.latitude
        return math.sqrt((dx) ** 2 + (dy) ** 2)

    def getName(self):
        return self.city


class Node:
    def __init__(self, city):
        self.city = city
        self.name = city.getName()
        self.edges = []
        self.isEndNode = False

    def rouletteWheel(self, visitedEdges, minNodeCount, startNode, endNode):
        visitedNodes = [oneEdge.toNode for oneEdge in visitedEdges]
        #print(visitedEdges)
        viableEdges = [oneEdge for oneEdge in self.edges if not oneEdge.toNode in visitedNodes and oneEdge.toNode != startNode]
        # and oneEdge.pheromones>MINPHEROMONES]

        #print("viable edges 1:", len(viableEdges))
        # modification to original code
        if len(visitedEdges) < minNodeCount:
            for e in viableEdges:
                if e.toNode == endNode:
                    # print("remove edge:", e)
                    viableEdges.remove(e)
            # for e in viableEdges:
            #    print(e)

        if len(viableEdges) == 0:
            return None

        allPheromones = sum([oneEdge.pheromones for oneEdge in viableEdges])
        num = random.uniform(0, allPheromones)
        #print("num:", num, allPheromones)
        s = 0
        i = 0

        selectedEdge = viableEdges[i]
        while s <= num:
            selectedEdge = viableEdges[i]
            s += selectedEdge.pheromones
            i += 1

        #print("rouletteWheel:", num, allPheromones, s, i)
        return selectedEdge

    def getCity(self):
        return self.city

    def __repr__(self):
        return self.name


class Edge:
    def __init__(self, fromNode, toNode):
        self.fromNode = fromNode
        self.toNode = toNode
        self.cost = fromNode.getCity().getLength(toNode.getCity())
        self.pheromones = MAXPHEROMONES
        self.maxPheromones = MAXPHEROMONES
        self.minPheromones = MINPHEROMONES

    def getCost(self):
        return self.cost

    def evaporate(self):
        if self.pheromones > self.maxPheromones:
            self.pheromones = self.maxPheromones
        self.pheromones *= float(EVAPORATION)
        if self.pheromones < self.minPheromones:
            self.pheromones = self.minPheromones

    def isEqual(self, other):
        return self.fromNode == other.fromNode and self.toNode == other.toNode

    def __repr__(self):
        return self.fromNode.name + "--(" + str(self.cost) + ")--" + self.toNode.name + ", pheromones: " + str(
            round(self.pheromones, 2))




class Ant:
    def __init__(self):
        self.visitedEdges = []
        self.chosenNodes = list()

    def walk(self, startNode, endNode, minEdgeCount):
        currentNode = startNode
        currentEdge = None
        prevEdge = None
        ntries = 0

        while (not self.checkAllNodesPresent(self.visitedEdges, minEdgeCount, endNode)):
            currentEdge = currentNode.rouletteWheel(self.visitedEdges, minEdgeCount, startNode, endNode)

            # print("currentEdge", currentEdge)
            if currentEdge == None:
                # End node returns None. If end node is selected before all all edges are visited, try again.
                # Otherwise we may select the end node too early
                #print("None")

                self.visitedEdges.remove(prevEdge)
                currentNode = prevEdge.fromNode
                if ntries > 3:
                    # Not a valid path, did not walk all nodes.
                    return False
                ntries += 1

                # currentEdge = self.visitedEdges[len(self.visitedEdges)-1]
            else:
                currentNode = currentEdge.toNode
                self.visitedEdges.append(currentEdge)
                prevEdge = currentEdge
        return True

    def pheromones(self):
        currentCost = getSum(self.visitedEdges)

        global minCost
        if currentCost < MAXCOST:
            if currentCost < minCost:
                minCost = currentCost
                global bestVisits
                bestVisits = self.visitedEdges

            score = 1000 ** (1 - float(currentCost) / MAXCOST)
            # print("score:", score, currentCost, MAXCOST)
            for oneEdge in self.visitedEdges:
                oneEdge.pheromones += score


    def checkAllNodesPresent(self, edges, minNodeCount, endNode):
        visitedNodes = [edge.toNode for edge in edges]
        return len(visitedNodes) >= minNodeCount and endNode in visitedNodes

    def printEdges(self):
        for edge in self.visitedEdges:
            print(edge, edge.pheromones)


minCost = 10000000


def getCities(filename): #leser fra fil og returnerer byer
    cities = dict()
    inFile = open(filename,'r')#"rt", encoding="iso-8859-1"
    for line in inFile:
        city = City(line)
        cities[city.getName()] = city

    inFile.close()
    return cities



# create edges between nodes. Nodes must have less distance that maxNodeDist.
# startcity is not added as an to-edge
def getEdges(nodeList, maxNodeDist, startCity):
    print("getEdges")
    _edges = list()
    for _fromNode in nodeList:
        # _fromNode = nodeList[n]
        for k in range(1, len(nodeList)):
            _toNode = nodeList[k]
            dist = _fromNode.city.getLength(_toNode.city)  #
            if dist < maxNodeDist:
                # Ensure no edge from self to self
                if _fromNode != _toNode and _toNode.city != startCity:
                    newEdge = Edge(_fromNode, _toNode)
                    # This is a hack to make list of edges unique. MUST be a different way.
                    doAdd = True
                    for existinEdge in _edges:
                        if newEdge.isEqual(existinEdge):
                            doAdd = False
                            break

                    if doAdd == True:
                        _edges.append(newEdge)
                        if _fromNode.city != startCity:
                            _edges.append(Edge(_toNode, _fromNode))

    return _edges


# Cost function
def getSum(edges):
    return sum([e.getCost() for e in edges]) #/ 2

filename = "61cities.txt"
#filename = "morecities.txt"
allCities = getCities(filename)
cityList = list(allCities.values())
cityCount = len(allCities)

print("No of cities:", cityCount)
startCity = allCities.get("oslo")
endCity = allCities.get("bergen")

totalDist = startCity.getLength(endCity)
print("Dist: ", totalDist)

edges = []
nodes = list()
MAXCOST = 0

nodes = list()

for city in cityList:
    nodes.append(Node(city))

maxNodeDist = totalDist / 3

edges = getEdges(nodes, maxNodeDist, startCity)
for e in edges:
    print(e)

print("Assign edges to nodes")
# Assign to nodes
for oneEdge in edges:
    for oneNode in nodes:
        if (oneEdge.fromNode == oneNode):
            oneNode.edges.append(oneEdge)

# list of ant's walks. One entry consist of a list of edges, the best result should be stored.
bestVisits = []

startNode = None
for node in nodes:
    if node.name == 'oslo':
        startNode = node
        break

endNode = None
for node in nodes:
    if node.name == 'bergen':
        endNode = node
        break


def plotGraph(results, ylabel):
    x = []
    y = []
    for key, value in results.items():
        x.append(key)
        y.append(value)

    plt.plot(x, y)
    plt.title("ACO")
    plt.ylabel(ylabel)
    plt.xlabel("Iteration")
    # plt.legend()
    plt.grid(True, color='g')
    plt.show()


def printVisits(visitedEdges):
    print("")
    cost = getSum(visitedEdges)
    length = len(visitedEdges)
    if length == MINEDGES or length < 15:

        print("Vists number and cost: ", length, cost)
        for e in visitedEdges:
            print(e)


resultsCount = dict()
resultsCost = dict()


def walkRandomPaths(max):
    for n in range(0, max):
        global MAXCOST
        MAXCOST = getSum(edges)
        for edge in edges:
            edge.evaporate()

        ant = Ant()
        isValid = ant.walk(startNode, endNode, MINEDGES)
        if isValid:
            ant.pheromones()
            # ant.printEdges()
            cost = getSum(ant.visitedEdges)
            resultsCost[n] = cost                  #sette inn verdiene (skal gå til y-aksen)
            resultsCount[n] = len(ant.visitedEdges) #sette inn verdiene (skal gå til y-aksen)
            # print("n", n, "Cost",  len(ant.visitedEdges), cost)
            printVisits(ant.visitedEdges)


walkRandomPaths(30000) #repetasjon 20000 ganger
#plotter to forskjellige grafer
plotGraph(resultsCost, "Cost") #(y-aksen)
plotGraph(resultsCount, "Edges") #(y-aksen i graf)

print("The best result:")
printVisits(bestVisits)

print("")
print("")
print("")


