# David Patenaude 
# EEE4334 CAD for VLSI Project Part 1
# 10.23.2023

# Define a graph class (adjacency list)
class Graph:
    def __init__(self) -> None:
        self.graph = {}
        self.numNodes = 0
        self.numEdges = 0
        self.inputNodes = []
        self.outNodes = []
        self.internNodes = []

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
            self.numNodes += 1
        
    def add_edge(self, node1, node2):
        if node1 in self.graph and node2 in self.graph:
            self.graph[node1].append(node2)
            #self.graph[node2].append(node1) # for undirected
        #else:
            # Is there a log we can print to?
            #print("A node was not in the graph")
        self.numEdges += 1

    # Reads in a graph from file_name (a path)    
    def readGraph(self, file_name):
        """ Reads in a graph at the path given, file_name;
            Adds nodes for the input and output nodes given
        """
        # Open file for reading
        with open(file_name, 'r') as inFile:
            sLine = inFile.readline().split(" ")
            while sLine[0] != '':
                if sLine[0] == "Inputs":
                    numInputs = int(sLine[1].strip())
                    iLine = inFile.readline().split(" ")
                    for i in range(numInputs):
                        #Add the nodes to the graph and a list for the input nodes
                        # Add an i to the front of the node number to denote it is an input (otherwise use inputNode list)
                        self.inputNodes.append(iLine[i].strip())
                        self.add_node(iLine[i].strip())

                elif sLine[0] == "Outputs":
                    numOuts = int(sLine[1].strip())
                    oLine = inFile.readline().split(" ")
                    for i in range(numOuts):
                        #Similarly, add an 'o' to the fron as designation, or use the list. 
                        self.outNodes.append(oLine[i].strip())
                        self.add_node(oLine[i].strip()) 

                elif sLine[0] == "Nodes":
                    #Number of internal nodes? => # of non-input nodes
                    numNodes = int(sLine[1].strip())
                    newNodes = numNodes - len(self.outNodes)   # # of output nodes (or numOuts)
                    #i = 1
                    #while str(i) not in self.graph:
                    #    nonlocal i #doesn't work! ugh. (give some error)
                    #    i = i + 1
                        # Will not work if output nodes are not continuous numbers.
                        # Solution would be to check if (i in inputNodes or i in outNodes) then skip. if not, add to the graph.
                    idx = 1
                    count = 0
                    while count < newNodes:

                        # If this index is already in the graph, go to next index and continue
                        if str(idx) in self.inputNodes or str(idx) in self.outNodes:
                            idx = idx + 1
                            continue
                        # Else we will add this index to the graph
                        self.internNodes.append(str(idx))
                        self.add_node(str(idx))
                        #print('Added node: ' + str(idx))
                        idx += 1
                        count += 1
                    #end while
                    
                    #print('i is ' + str(i)) #We have an issue of scope!

#                    for j in range(i, i+newNodes):
#                        self.internNodes.append(j)
#                        self.add_node(str(j))
#                        print('Added node: ' + str(j))

                elif sLine[0] == "Edges":
                    numEdges = int(sLine[1].strip())
                    for i in range(numEdges):
                        e = inFile.readline().split(" ")
                        n1, n2 = e[0].strip(), e[1].strip() #multiple assignment
                        self.add_edge(n1, n2)   #edge from n1 to n2
                sLine = inFile.readline().split(" ")
            #end while
        #end with
    #end function

    def nicePrint(self):
        """ Prints the graph object, listing the number of input nodes and then printing them
            followed by number of output nodes and printing them.
            It then continues to list the of internal nodes, followed by the edges of the graph
        """
        div = '*' * 26 + '\n'
        iLine = str(len(self.inputNodes)) + ' Inputs: '
        for i in self.inputNodes:
            iLine += str(i) + ' '
        oLine = '\n' + str(len(self.outNodes)) + ' Outputs: '
        for o in self.outNodes:
            oLine += str(o) + ' '
        nLine = '\n' + str(len(self.internNodes)) + ' Internal Nodes: '
        for i in self.internNodes:
            nLine += str(i) + ' '
        # Now for the edges!
        edges = '\n'+ str(self.numEdges) + ' Edges:\n'
        for node in self.graph:
            edges += '\t' + node + ': '
            first = True
            for e in self.graph[node]:
                if first:
                    edges += e
                    first = False
                else:
                    edges += ', ' + e    #will leave a comma at end... only thought is to have a flag for first. -- FIXED
            edges += '\n'
        # Print or return as string?
        return div + iLine + oLine + nLine + edges + div

    #A 'raw' print
    def __str__(self):
        ret = 'Graph: ' + str(self.graph) + '\nInputs: ' + str(self.inputNodes) + '\nOutputs: ' + str(self.outNodes)
        ret += '\nInternal Nodes: ' + str(self.internNodes)
        return ret
    
    
file_path = input("Enter file path: ")

graph = Graph()
graph.readGraph(file_path)

#print(graph)

print(graph.nicePrint())

