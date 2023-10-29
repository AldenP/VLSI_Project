# David Patenaude 
# EEE4334 CAD for VLSI Project Part 1 (input parsing)
# 10.23.2023

# Define a graph class (adjacency list)
class Graph:

    #Adding variables here would be accessible for all instances of the class
    def __init__(self) -> None:
        #While variables here are accessible to each instance of the Class individually!
        self.graph = {}
        self.numNodes = 0
        self.numEdges = 0
        self.inputNodes = []
        self.outNodes = []
        self.internNodes = []
        self.name = None

    def __init__(self, name) -> None:
        self.graph = {}
        self.numNodes = 0
        self.numEdges = 0
        self.inputNodes = []
        self.outNodes = []
        self.internNodes = []
        self.name = name

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
        div = '*' * 26  # + '\n'
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
        return '\n' + div + iLine + oLine + nLine + edges + div

    #A 'raw' print
    def __str__(self):
        ret = 'Graph: ' + str(self.graph) + '\nInputs: ' + str(self.inputNodes) + '\nOutputs: ' + str(self.outNodes)
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
            case 'solve':
                # Would produce a valid sequence for this graph/netlist
                print("Not implemented!")
            case 'evaluate':
                # Prompt for an imported sequence from the global variable 'seqs'
                print("Not Implemented!")
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
                #Ask for a sequence to run for this graph.
                print("Not Implemented!")
            case 'back':
                return
            case _:
                print(seqHelpStr)
        #End Match
        userIn = input('+==>')
    #End while
    return
#End seq. loop function

def getFileName(path):
    #Get the name of the file from the path (no extension or '/')
    str1 = path.split('/')
    str2 = str1[-1].split('.')
    # assumming only 1 '.' for the extension, we can return the first element.
    return str2[0]

# "Main" equivalent
graphs = []
seqs = []

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
            graphs.append(gr)
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
            seqs.append(seq)
            #Prompt for sequence options
            print('Success!')
            seqLoop(seq)

            print(helpStr)
        case 'show':
            #Show all graphs and sequences with a number (or their name) assigned to them 
            #for g in graphs:
            print("Imported Graphs: ")
            first = True
            for g in graphs:
                if first:
                    first = False
                    print("'"+g.name + "'", end=' ')
                else:
                    print(", '" + g.name + "'", end = ' ')
            if graphs.count == 0:
                print('(None)')
            print("\nImported Sequences: ")
            first = True
            for s in seqs:
                if first:
                    first = False
                    print("'"+s.name + "'", end=' ')
                else:
                    print(", '" + s.name + "'", end = ' ')
            if seqs.count == 0:
                print('(None)')
            print("\n" + "-" * 10) #newline / divider

        case 'select':
            grName = input("Enter an imported graph name: ")
            found = False
            for g in graphs:
                if g.name == grName:
                    found = True
                    graphLoop(g)
                    print(helpStr)
                    break #the for loop
            if not found:
                print("Name not found")
        case 'quit':
            break
        case _:
            print(helpStr)
    userIn = input('==>')
#End while
print("Goodbye!")