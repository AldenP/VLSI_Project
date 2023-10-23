
# Define a graph class (adjacency list)
class Graph:
    def __init__(self) -> None:
        self.graph = {}
        self.numNodes = 0

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
            self.numNodes += 1
        
    def add_edge(self, node1, node2):
        if node1 in self.graph and node2 in self.graph:
            self.graph[node1].append(node2)
            #self.graph[node2].append(node1) # for undirected

    # Reads in a graph from file_name (a path)    
    def readGraph(self, file_name):
        """ Reads in a graph at the path given, file_name;
            Adds nodes for the input and output nodes given
        """
        # Open file for reading
        with open(file_name, 'r') as inFile:
            sLine = inFile.readline().split(" ")
            while sLine != '':
                if sLine[0] == "Inputs":
                    numInputs = int(sLine[1].strip())
                    iLine = inFile.readline().split(" ")
                    for i in range(numInputs):
                        #Add the nodes to the graph and a list for the input nodes
                        self.inputNodes = []
                        # Add an i to the front of the node number to denote it is an input (otherwise use inputNode list)
                        self.inputNodes.append(iLine[i])
                        self.add_node(iLine[i])

                elif sLine[0] == "Outputs":
                    numOuts = int(sLine[1].strip())
                    oLine = inFile.readline().split(" ")
                    for i in range(numOuts):
                        self.outNodes = []
                        #Similarly, add an 'o' to the fron as designation, or use the list. 
                        self.outNodes.append(oLine[i])
                        self.add_node(oLine[i]) 

                elif sLine[0] == "Nodes":
                    #Number of internal nodes? => # of non-input nodes
                    numNodes = int(sLine[1].strip())
                    newNodes = len(self.outNodes)   # # of output nodes (or numOuts)
                    i = 1
                    while str(i) not in self.graph:
                        i += 1
                    for j in range(i, i+newNodes):
                        self.internNodes = []
                        self.internNodes.append(j)
                        self.add_node(str(j))

                elif sLine[0] == "Edges":
                    self.numEdges = int(sLine[1].strip())
                    for i in range(self.numEdges):
                        e = inFile.readline().split(" ")
                        n1, n2 = e[0], e[1] #multiple assignment
                        self.add_edge(n1, n2)   #edge from n1 to n2
                sLine = inFile.readline().split(" ")
            #end while
        #end with
    #end function

    def __str__(self):
        return str(self.graph)
    
    
file_path = input("Enter file path: ")

graph = Graph()
graph.readGraph(file_path)

print(graph)


