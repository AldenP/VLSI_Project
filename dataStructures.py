# dataStructures.py - Stores the graph and sequence structures,
#   and the functions that can be used on them.
#David Patenaude, VLSI Project 1, 11.9.2023
DEBUG = False

class Graph:
    def __init__(self) -> None:
        self.graphInO = {}  #Edges go from input nodes to output nodes
        self.graphOIn = {}  #Edges go from output nodes to input nodes
        self.numNodes = 0
        self.numEdges = 0
        self.inputNodes = []
        self.outNodes = []
        self.internNodes = []
        self.name = None

    def __init__(self, name) -> None:
        self.graphInO = {}
        self.graphOIn = {}  #Edges go from output nodes to input nodes
        self.numNodes = 0
        self.numEdges = 0
        self.inputNodes = []
        self.outNodes = []
        self.internNodes = []
        self.name = name

    def add_node(self, node):
        if node not in self.graphInO:
            self.graphInO[node] = []
            self.graphOIn[node] = []
            self.numNodes += 1
        
    def add_edge(self, node1, node2):
        if node1 in self.graphInO and node2 in self.graphInO:
            self.graphInO[node1].append(node2)
            # Do not add an edge to an input node for the reversed graph
            #if node1 not in self.inputNodes:    #logic prevents findMemCost from working!
            self.graphOIn[node2].append(node1)  # put edge in reverse order
            #self.graphInO[node2].append(node1) # for undirected
        #else:
            # Is there a log we can print to?
            #print("A node was not in the graph")
        self.numEdges += 1

    def nicePrint(self):
        """ Prints the graph object, listing the number of input nodes and then printing them
            followed by number of output nodes and printing them.
            It then continues to list the of internal nodes, followed by the edges of the graph
        """
        div = '*' * 26  # + '\n'
        iLine = '\n'+ str(len(self.inputNodes)) + ' Inputs: '
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
        for node in self.graphInO:
            edges += '\t' + node + ': '
            first = True
            for e in self.graphInO[node]:
                if first:
                    edges += e
                    first = False
                else:
                    edges += ', ' + e    #will leave a comma at end... only thought is to have a flag for first. -- FIXED
            edges += '\n'
        # Print or return as string?
        return '\n' + div + iLine + oLine + nLine + edges + div

    def nicePrintReverse(self):
        """ Prints the reversed graph object, listing the number of input nodes and then printing them
            followed by number of output nodes and printing them.
            It then continues to list the of internal nodes, followed by the edges of the graph
        """
        div = '*' * 26  # + '\n'
        iLine = '\n' + str(len(self.inputNodes)) + ' Inputs: '
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
        for node in self.graphOIn:
            edges += '\t' + node + ': '
            first = True
            for e in self.graphOIn[node]:
                if first:
                    edges += e
                    first = False
                else:
                    edges += ', ' + e    #will leave a comma at end... only thought is to have a flag for first. -- FIXED
            edges += '\n'
        # Print or return as string?
        return '\n' + div + iLine + oLine + nLine + edges + div

    #A 'raw' print
    def __str__(self):
        ret = 'Graph: ' + str(self.graphInO) + '\nInputs: ' + str(self.inputNodes) + '\nOutputs: ' + str(self.outNodes)
        ret += '\nInternal Nodes: ' + str(self.internNodes)
        return ret

class Sequence:
    def __init__(self) -> None:
        self.order = [] #a list of the order of execution.
        self.isValid = False    #to be determined later! (requires an input graph)
        self.name = None
    
    def __init__(self, name) -> None:
        self.order = [] #a list of the order of execution.
        self.isValid = False    #to be determined later! (requires an input graph)
        self.name = name

    def add(self, node):
        """ Adds node to this execution sequence (appends to the end). 
            Checks if node is in the list already
        """
        if node not in self.order:
            self.order.append(node)
            return True
        return False    #node already in list

    def isValidSequence(self, graph):
        """ Determine if this sequence is valid for the graph selected
            Start by navigating the graph in the 'reversed' direction. If no edges then 
            that node can be executed (it does not depend on any internal nodes)"""
        #First remove the edges that go to the input nodes. => This will run multiple times on the same object! (Pass by reference!)
        # this should be handled in the input function. 
        # This is convoluted with this implementation. I recommend doing two things:
        # 1) have a bi-directional graph to start with; 2) make mulitple modules (code over multiple files)
         #This is now handled in the add_node function (it skips adding input nodes to graphOIn)
        """ Eliminate the input nodes from the O->In graph"""
        import copy
        graphCopy = copy.deepcopy(graph.graphOIn)   #Deep copy copies ALL the data from reversed graph
        for inNode in graph.inputNodes:
            # For each ending node of the input node edges, ...
            for node in graph.graphInO[inNode]:
                #...remove the input node from the list.
                #graph.graphOIn[node].remove(inNode)
                graphCopy[node].remove(inNode)
        
        #Now we can check if the sequence of nodes is valid by seeing if the list of nodes for that node is empty
        #Needed to be above the for loop.
       # graphCopy = copy.deepcopy(graph.graphOIn)   #Deep copy copies ALL the data from reversed graph
        for node in self.order: #For nodes in sequence
            #graphCopy = graph.graphOIn.copy()   #gives a shallow copy...the lists will be the same data
            #print(graphCopy.nicePrintReverse())     #doesn't work because copy is a dictionary not a graph obj!
            #print("len of node '" + str(node) + "': " + str(len(graphCopy[node])))
            if len(graphCopy[node]) == 0:   #If there is a dependancy (edge) leading into this node (len !=0), not valid 
                #This node can be processed, so we must remove it from the graph.
                for edge in graph.graphInO[node]: # these are the nodes dependent on 'node' (nodes upstream)
                    graphCopy[edge].remove(node) 
                    #print('removed edge: ' + str(node) + " from " + str(edge)) #debug print: had copy in the for loop. needed to be above it
            else:
                self.isValid = False
                return False
        self.isValid = True
        return True
  
    def nicePrint(self):
        out = str(len(self.order)) + ' Operations: '
        first = True
        for node in self.order:
            if first:
                out += node
                first = False
            else:
                out += ' -> ' + node
        return '\n' + out + '\n'

    # Move to inputOutput.py ? 
    def printToFile(self, file_name):
        """ Prints the execution sequence to a file provided in the
            same format as the input
        """
        try:
            with open(file_name, 'w') as outFile:
                outFile.write('Operations ' + str(len(self.order)) + '\n')
                for i in self.order:
                    outFile.write(i + '\n')
            # End of with automatically closes the file
            return True
        except OSError:
            print("Error while printing to file. Program lacks permissions or bad path.")
            #raise will interrupt the program
        except Exception as e:
            raise e #Raise the exception

    def __str__(self):
        return self.order
#End Sequence Class

import copy
# Project Functions: sequence evaluation, graph evaluation with a sequence, and solving a graph. 
def findMemCost(graph, sequence):
    """ Finds the minimum memory cost of evaluating the graph using the sequence provided
        Sequence should be valid"""
    """Two  ideas: Use a set, track the size each iteration for the max. Remove from set
        when node no longer needed (by checking if any edges left.)
        Other idea: I forgot! but it probably deals with the graph and edges"""
    inUse = set()  #Set to store nodes in use
    #Populate with input nodes to start. 
    for iNode in graph.inputNodes:
        inUse.add(iNode)
    maxMem = len(inUse) #initial maximum
    # could iterate over set elements and see if any edges leaving it. -> not efficient
    # could count number of edges and remove one each time it is used, at zero remove it. 
    # (better - takes the hit at the start) but it should iterate the whole graph...
    edgeCount = dict()
    for node in graph.graphInO:
        count = 0
        for e in graph.graphInO[node]:
            count += 1
        #Scope issue?
        #if count == 0:
        #   raise Exception("Count is Zero")    #Would raise on an output node...
        #print("Number of edges for '" + node + "': " + str(count))
        edgeCount[node] = count

    if DEBUG:   #Print to console some debug info.
        print("Initial Edge Count Array: ")
        for n in graph.graphInO:
            print("'" + str(n) + "': " + str(edgeCount[n]))    
    
    seq = copy.deepcopy(sequence)   #copy not needed
    #loop while there is a next node to process. 
    for next in seq.order:
        #Assume order is valid. compute 'next', add to set (check if new max)
        print("DEBUG> For seq. Node " + str(next))
        inUse.add(next) #compute 'next'

        #Re locate to a larger scope?
        def printSet(set):
            print('{', end=' ')
            for e in set:
                print(str(e), end=', ')
            print('}')

        if DEBUG:
            printSet(inUse)
        #Update maxMem if set is larger now.
        if len(inUse) > maxMem:
            maxMem = len(inUse)
        
        if DEBUG:
            print('Max Mem so far: ' + str(maxMem) + '-----')
        
        #Use graph to reduce edge counter, if any edges go to zero, remove from set
        for e in graph.graphOIn[next]:  #loop edges leading into current node (by looking backwards)
            edgeCount[e] -= 1
            if edgeCount[e] == 0:
                inUse.remove(e) #Free this from the set/memory
        
        if DEBUG:
            print('Set after edge removal');
            printSet(inUse)
    #End for loop over sequence nodes.
    return maxMem
#End findMemCost(graph, seq)

def isValidSequence(sequence, graph):
        """ Determine if this sequence is valid for the graph selected
            Start by navigating the graph in the 'reversed' direction. If no edges then 
            that node can be executed (it does not depend on any internal nodes)"""
        #First remove the edges that go to the input nodes. => This will run multiple times on the same object! (Pass by reference!)
        # this should be handled in the input function. 
        # This is convoluted with this implementation. I recommend doing two things:
        # 1) have a bi-directional graph to start with; 2) make mulitple modules (code over multiple files)
         #This is now handled in the add_node function (it skips adding input nodes to graphOIn)
        """ Eliminate the input nodes from the O->In graph"""

        graphCopy = copy.deepcopy(graph.graphOIn)   #Deep copy copies ALL the data from reversed graph
        for inNode in graph.inputNodes:
            # For each ending node of the input node edges, ...
            for node in graph.graphInO[inNode]:
                #...remove the input node from the list.
                #graph.graphOIn[node].remove(inNode)
                graphCopy[node].remove(inNode)
        
        #Now we can check if the sequence of nodes is valid by seeing if the list of nodes for that node is empty
        #Needed to be above the for loop.
       # graphCopy = copy.deepcopy(graph.graphOIn)   #Deep copy copies ALL the data from reversed graph
        for node in sequence.order: #For nodes in sequence
            #graphCopy = graph.graphOIn.copy()   #gives a shallow copy...the lists will be the same data
            #print(graphCopy.nicePrintReverse())     #doesn't work because copy is a dictionary not a graph obj!
            #print("len of node '" + str(node) + "': " + str(len(graphCopy[node])))
            if len(graphCopy[node]) == 0:   #If there is a dependancy (edge) leading into this node (len !=0), not valid 
                #This node can be processed, so we must remove it from the graph.
                for edge in graph.graphInO[node]: # these are the nodes dependent on 'node' (nodes upstream)
                    graphCopy[edge].remove(node) 
                    #print('removed edge: ' + str(node) + " from " + str(edge)) #debug print: had copy in the for loop. needed to be above it
            else:
                #sequence.isValid = False
                return False
        #sequence.isValid = True
        return True
#end isValidSequence(sequence, graph)