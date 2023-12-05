# inputOutput.py - A file for handling the I/O for the project
# David Patenaude
# VLSI Project 1 - Fall '23
# 11.9.2023

def readGraph(graph, file_name):
    """ Reads in a graph at the path given, file_name;
        Updates the graph object 'graph'
        Adds nodes for the input and output nodes given in file, 
        then adds the edges.
    """
    # Check if path is valid! - may be an OS method for this.
    if not isValidPath(file_name):
        return False    #if not, return false!
    # Get the name of the graph
    graph.name = getFileName(file_name)

    #Open file for reading
    with open(file_name, 'r') as inFile:
        lines = inFile.readlines()  #read all lines at once

        #sLine = inFile.readline().split(" ")   
        index = 0 
        while index < len(lines):
            splitLine = lines[index].split(" ")
            if splitLine[0] == "Inputs":
                numInputs = int(splitLine[1].strip())
                #inFile.readline()
                #iLine = inFile.readline().split(" ")    # .graph files have just a newline, \n (LF). Windows uses '\r\n' (CRLF). 
                index += 1
                iLine = lines[index].split(" ") #pre-increment index, split the line with the input node #'s
                for i in range(0, numInputs):   #range excludes the 2nd   #could simplfy and just do "for i in iLine:" 
                    #Add the nodes to the graph and a list for the input nodes
                    # Add an i to the front of the node number to denote it is an input (otherwise use inputNode list)
                    graph.inputNodes.append(iLine[i].strip())   #as of 11.16 there is an error for index out of range (iLine is empty?!?)
                    graph.add_node(iLine[i].strip())
            elif splitLine[0] == "Outputs":
                numOuts = int(splitLine[1].strip())
                #oLine = inFile.readline().split(" ")
                index += 1
                oLine = lines[index].split(" ")
                for i in range(numOuts):
                    #Similarly, add an 'o' to the fron as designation, or use the list. 
                    graph.outNodes.append(oLine[i].strip())
                    graph.add_node(oLine[i].strip()) 
            elif splitLine[0] == "Nodes":
                #Number of internal nodes? => # of non-input nodes
                numNodes = int(splitLine[1].strip())
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
            elif splitLine[0] == "Edges":
                numEdges = int(splitLine[1].strip())
                for i in range(numEdges):
                    index += 1
                    e = lines[index].split(" ")
                    n1, n2 = e[0].strip(), e[1].strip() #multiple assignment
                    graph.add_edge(n1, n2)   #edge from n1 to n2
            # else:
            #     index+=1    # in case we are stuck on a non if'ed input line
            index += 1  #else should be useless now.
        #sLine = inFile.readline().split(" ")
        #end while
    #end with
    graph.populateInternalGraph()   #populate the internal graph for use in other functions
    return True # successfully read the graph.
#end function

def readSequence(sequence, file_name):
    """ Reads in an execution sequence from the file passed,
        stores the data in the sequence provided
    """
    # Check if path is valid
    if not isValidPath(file_name):
        return False    #if not, return false!
    # Get the name of the sequence
    sequence.name = getFileName(file_name)

    with open(file_name, 'r') as inFile:
        line = inFile.readline().split(" ")
        numOps = int(line[1].strip())
        for i in range(numOps):
            # Since graph has node #'s as strings ('1', '3', etc.) store the number as a string here as well!
            sequence.add(inFile.readline().strip())
    return True

def printSeqToFile(seq, file_name):
    """ Prints the execution sequence to a file provided in the
        same format as the input
    """
    try:
        with open(file_name, 'w') as outFile:
            outFile.write('Operations ' + str(len(seq.order)) + '\n')
            for i in seq.order:
                outFile.write(i + '\n')
        # End of with automatically closes the file
        return True
    except OSError:
        print("Error while printing to file. Program lacks permissions or bad path.")
        #raise will interrupt the program
    except Exception as e:
        raise e #Raise the exception
#end function printSequence to File

def isValidPath(path):
    """ Try to open the file (path) with read permissions
        return false for any access denied or file not found errors
        raises any other exception
        Function sends True/False, without giving the why
    """
    try:
        with open(path, 'r'):
            pass
    except FileNotFoundError:
        return False
    except OSError:
        return False
    except Exception as e:
        print(e)
        raise e
    return True

def getNewPath(file_path):
    """ Check to see if a file at path exists, to avoid overwriting a generated sequence, 
        then return a path that doesn't interfere with it"""
    import os.path
    if os.path.isfile(file_path + '.seq'):
        i = 1
        while os.path.isfile(file_path + '_' + str(i) + '.seq'):
            i += 1
        return file_path + '_' + str(i) + '.seq'
    # File does not exist, so this path is free to use.
    return file_path + '.seq'

def getFileName(path):
    """ Gets the name of a file by extracting it from the path
        The extraction splits on '/' and then gets the file name (without the extension)
    """
    #Get the name of the file from the path (no extension or '/')
    str1 = path.split('/')  #Should also split on '\' as it could be used instead of '/'
    str2 = str1[-1].split('\\')[-1].split('.')
    # assumming only 1 '.' for the extension, we can return the first element.
    return str2[0]
    # import os;
    # base, ext = os.path.splitext(path)
    # head, tail = os.path.split(base)
    # return tail