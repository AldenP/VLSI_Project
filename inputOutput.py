

def readGraph(graph, file_name):
        """ Reads in a graph at the path given, file_name;
            Updates the graph object 'graph'
            Adds nodes for the input and output nodes given in file, 
            then adds the edges.
        """
    #Open file for reading
    with open(file_name, 'r') as inFile:
        sLine = inFile.readline().split(" ")
        while sLine[0] != '':
            if sLine[0] == "Inputs":
                numInputs = int(sLine[1].strip())
                iLine = inFile.readline().split(" ")
                for i in range(numInputs):
                    #Add the nodes to the graph and a list for the input nodes
                    # Add an i to the front of the node number to denote it is an input (otherwise use inputNode list)
                    graph.inputNodes.append(iLine[i].strip())
                    graph.add_node(iLine[i].strip())
            elif sLine[0] == "Outputs":
                numOuts = int(sLine[1].strip())
                oLine = inFile.readline().split(" ")
                for i in range(numOuts):
                    #Similarly, add an 'o' to the fron as designation, or use the list. 
                    graph.outNodes.append(oLine[i].strip())
                    graph.add_node(oLine[i].strip()) 
            elif sLine[0] == "Nodes":
                #Number of internal nodes? => # of non-input nodes
                numNodes = int(sLine[1].strip())
                newNodes = numNodes - len(graph.outNodes)   # # of output nodes (or numOuts)
                #i = 1
                #while str(i) not in graph.graphInO:
                #    nonlocal i #doesn't work! ugh. (give some error)
                #    i = i + 1
                    # Will not work if output nodes are not continuous numbers.
                    # Solution would be to check if (i in inputNodes or i in outNodes) then skip. if not, add to the graph.
                idx = 1
                count = 0
                while count < newNodes:
                # If this index is already in the graph, go to next index and continue
                    if str(idx) in graph.inputNodes or str(idx) in graph.outNodes:
                        idx = idx + 1
                        continue
                    # Else we will add this index to the graph
                    graph.internNodes.append(str(idx))
                    graph.add_node(str(idx))
                    #print('Added node: ' + str(idx))
                    idx += 1
                    count += 1
                #end while
            elif sLine[0] == "Edges":
                numEdges = int(sLine[1].strip())
                for i in range(numEdges):
                    e = inFile.readline().split(" ")
                    n1, n2 = e[0].strip(), e[1].strip() #multiple assignment
                    graph.add_edge(n1, n2)   #edge from n1 to n2
        sLine = inFile.readline().split(" ")
        #end while
    #end with
#end function
