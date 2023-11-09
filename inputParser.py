# David Patenaude 
# EEE4334 CAD for VLSI Project Part 1 (input parsing)
# 10.23.2023

#This is the all in one file 
#as of 11.9.2023, moving to multiple files. 

#Import copy to make deep copies of objects
import copy
# Define a graph class (adjacency list)
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
                    #while str(i) not in self.graphInO:
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
        """Determine if this sequence is valid for the graph selected
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

    def readSequence(self, file_name):
        """ Reads in an execution sequence from the file passed"""
        # Bad file name exception handled prior
        with open(file_name, 'r') as inFile:
            line = inFile.readline().split(" ")
            numOps = int(line[1].strip())
            for i in range(numOps):
                # Since graph has node #'s as strings ('1', '3', etc.) store the number as a string here as well!
                self.add(inFile.readline().strip())
    
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

#Define some functions for the user to interact with the program (in a console setting)
def graphLoop(graph):
    gId = graph.name
    graphIdStr = "For Graph '" + gId + "'"
    graphHelpStr = "\nGraph commands are: 'print', 'solve', 'evaluate', and 'back' (go back)"
    print(graphIdStr + graphHelpStr)
    userIn = input('+==>').strip()
    while userIn != 'back' or 'q' or 'exit':
        match userIn:
            case 'print':
                print(graphIdStr + graph.nicePrint())
                #Print the reverse graph for debugging (it appears to be correct)
                print(graphIdStr + 'reverse!' + graph.nicePrintReverse())
            case 'solve':
                # Would produce a valid sequence for this graph/netlist
                print("Not implemented!")
            case 'evaluate':
                # Prompt for an imported sequence from the global variable 'seqs'
                #determine the minimum memory consumption 
                seqName = input("Enter an imported sequence to determine minimum memory consumption: ")
                global seqs
                if seqName not in seqs:
                    print("Sequence '"+ seqName + "' not imported!")   #
                    userIn = '' #attempt to give help prompt on next iteration
                    continue
                #Otherwise pass seqs[seqName] 
                mem = findMemCost(graph, seqs[seqName])
                print("The memory cost is " + str(mem) + " for graph '" + graph.name + "', using sequence '" + seqName + "'")
            case 'back':
                return
            case _: 
                print(graphHelpStr)
        userIn = input('+==>')
    return
#End loop function

def seqLoop(seq):
    seqId = seq.name
    seqIdStr = "For Sequence '" + seqId + "'"
    seqHelpStr = "\nSequence commands are: 'print', 'write', 'evaluate', and 'back' (go back)"
    print(seqIdStr + seqHelpStr)
    userIn = input('+==>').strip()
    while userIn != 'back' or 'q' or 'exit':
        match userIn:
            case 'print':
                print(seqIdStr + seq.nicePrint())
            case 'write':
                print_path = input("Enter a Path to Print Sequence to: ")
                out = seq.printToFile(print_path)
                if out:
                    print("Success!")
                else:
                    print("Failed. ;(")
            case 'evaluate':
                #Ask for a graph to test this sequence
                graphName = input("Enter an imported graph name or a file name for a new graph: ")
                # Check if it is just a name
                #Could use the getFileName(path) function to see if the path has been imported. 
                """if graphName.find('/') != -1 or graphName.find('\\') != -1:
                    # it is a path if it has a / or \.
                    name = getFileName(graphName)
                    global graphs

                    try:
                        idx = graphs.index(name)
                    except ValueError:
                        pass    #Pretty sure I'll end up with an error of scope again.
                    if graphs.__contains__(name):
                        seq.isValidSequence()
                        pass
                """
                global graphs
                evalOn = graphs[graphName]
                out = seq.isValidSequence(evalOn)
                #print("The Sequence is " + ( out ? "not ":"") + "valid!")
                if out: 
                    print("The Sequence " + seq.name +  " is VALID for " + graphName + ".")
                else:
                    print("The Sequence " + seq.name +  " is NOT valid for " + graphName + ".")
                #print("Not Implemented!")
            case 'back':
                return
            case _:
                print(seqHelpStr)
        #End Match
        userIn = input('+==>')
    #End while
    return
#End seq. loop function
def isValidPath(path):
    """ Try to open the file (path) with read permissions
    return false for any access denied or file not found errors"""
    try:
        with open(path, 'r'):
            pass
    except OSError:
        return False
    except FileNotFoundError:
        return False
    except Exception as e:
        print(e)
        raise e
    return True

def getFileName(path):
    #Get the name of the file from the path (no extension or '/')
    str1 = path.split('/')
    str2 = str1[-1].split('.')
    # assumming only 1 '.' for the extension, we can return the first element.
    return str2[0]

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

    print("Initial Edge Count Array: ")
    for n in graph.graphInO:
        print("'" + str(n) + "': " + str(edgeCount[n]))    
    #gr = copy.deepcopy(graph.InO)
    seq = copy.deepcopy(sequence)   #copy not needed
    #loop while there is a next node to process. 
    for next in seq.order:
        #Assume order is valid. compute 'next', add to set (check if new max)
        print("DEBUG> For seq. Node " + str(next))
        inUse.add(next) #compute 'next'

        def printSet(set):
            print('{', end=' ')
            for e in set:
                print(str(e), end=', ')
            print('}')

        printSet(inUse)
        #Update maxMem if set is larger now.
        if len(inUse) > maxMem:
            maxMem = len(inUse)
        print('Max Mem so far: ' + str(maxMem) + '-----')
        #Use graph to reduce edge counter, if any edges go to zero, remove from set
        for e in graph.graphOIn[next]:  #loop edges leading into current node (by looking backwards)
            edgeCount[e] -= 1
            if edgeCount[e] == 0:   #changed logic to <= 0, input nodes have zero edges initially?
                #Free this from the set/memory
                inUse.remove(e)
        print('Set after edge removal');
        printSet(inUse)
    #End For
    return maxMem
        
# "Main" equivalent
graphs = {}
seqs = {}

#To help with testing, pre-populate graphs and seqs with some graphs and sequences
gr = Graph('adder1')
gr.readGraph('./graphs/adder1.graph')
graphs['adder1'] = gr

seq = Sequence('adder1b')
seq.readSequence('./sequences/adder1b.seq')
seqs['adder1b'] = seq
seq = Sequence('adder1a')
seq.readSequence('./sequences/adder1a.seq')
seqs['adder1a'] = seq

helpStr = "\nCommands are: 'readGraph', 'readSequence', 'show', 'select', 'quit', and 'help'"

print('*' * 50 + "\nWelcome to the Input Parser!" + helpStr)
userIn = input("==>").strip()   # could also .lower()
while userIn != 'quit': # or 'q' or 'exit':     #only the first was working
    match userIn:
        case 'readGraph':
            file_path = input("Enter graph file path: ")
            # I could have try go over the readGraph function call instead... might be better ( more robust)
            try:
                with open(file_path, 'r') as f:
                    pass
            except FileNotFoundError as ex:
                print("File not found: '" + ex.filename + "'\nPlease try again")
                continue #continue to next while iteration (userIn should be same - 'readGraph')

            gId = getFileName(file_path)
            gr = Graph(gId)
            gr.readGraph(file_path)
            #graphs.append(gr)
            graphs[gId] = gr    #map the string name (gId) to this graph object (gr)
            #Prompt for further graph options - graph loop function
            print('Success!')   #add success/fail logic and exception handling later
            graphLoop(gr)
            #Print the helpStr to help user know where they are.
            print(helpStr)

        case 'readSequence':
            seq_path = input("Enter Sequence Path: ")

            try:
                with open(seq_path, 'r') as f:
                    pass
            except FileNotFoundError as ex:
                print("File not found: '" + ex.filename + "'\nPlease try again")
                continue #continue to next while iteration (userIn should be same - 'readSequence')

            sId = getFileName(seq_path)
            seq = Sequence(sId)
            seq.readSequence(seq_path)
            #seqs.append(seq)
            seqs[sId] = seq #map the string name to this seq. object
            #Prompt for sequence options
            print('Success!')
            seqLoop(seq)

            print(helpStr)
        case 'show':
            #Show all graphs and sequences with a number (or their name) assigned to them 
            #for g in graphs:
            print("Imported Graphs: ")
            first = True
            #Changed from a list to a dictionary. 
            for g in graphs.values():
                if first:
                    first = False
                    print("'"+ g.name + "'", end=' ')
                else:
                    print(", '" + g.name + "'", end = ' ')
            #if graphs.values == 0:
            #    print('(None)')
            print("\nImported Sequences: ")
            first = True
            for s in seqs.values():
                if first:
                    first = False
                    print("'"+s.name + "'", end=' ')
                else:
                    print(", '" + s.name + "'", end = ' ')
            #if seqs.count == 0:
            #    print('(None)')
            print("\n" + "-" * 10) #newline / divider

        case 'select':
            #Add option to select a sequence!
            grName = input("Enter an imported graph or sequence name: ")
            found = False
            for g in graphs.values():
                if g.name == grName:
                    found = True
                    graphLoop(g)
                    print(helpStr)
                    break #the for loop
            for s in seqs.values():
                if s.name == grName:
                    found = True
                    seqLoop(s)
                    print(helpStr)
                    break
            if not found:
                print("Name not found")
        case 'quit':
            break
        case 'help':
            # add extra information to this command.
            print(helpStr)
        case _:
            print(helpStr)
    userIn = input('==>')
#End while
print("Goodbye!")