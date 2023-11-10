""" MainLoop.py - Store the looping for the console application,
    imports the data structures and file input from another file/module
        VLSI Project 1
    David Patenaude
    11.9.2023"""

import inputOutput as io;
import dataStructures as structs;
DEBUG = False;

# Loop functions for console-based user input
def graphLoop(graph):
    gId = graph.name
    graphIdStr = "For Graph '" + gId + "'"
    graphHelpStr = "\nGraph commands are: 'print', 'solve', 'evaluate', and 'back' (go back)"
    print(graphIdStr + graphHelpStr)
    userIn = input('+==>').strip()
    while userIn != 'back' or userIn != 'q' or userIn != 'exit':
        match userIn:
            case 'print':
                print(graphIdStr + graph.nicePrint())
                #Print the reverse graph for debugging (it appears to be correct)
                if DEBUG:
                    print(graphIdStr + 'reverse!' + graph.nicePrintReverse())
            case 'solve':
                # Would produce a valid sequence for this graph/netlist
                #Initially, try using Djisktra's algroithm. 
                print("Not implemented (yet!)")
            case 'evaluate':
                # Prompt for an imported sequence from the global variable 'seqs' and determine the maximum memory consumption 
                seqName = input("Enter an imported sequence to determine worst-case memory consumption: ")
                global seqs #seqs is in the global scope
                if seqName not in seqs:
                    print("Sequence '"+ seqName + "' not imported!")   #
                    userIn = '' #attempt to give help prompt on next iteration (could be scope issue)
                    continue
                #Otherwise pass seqs[seqName] 
                mem = structs.findMemCost(graph, seqs[seqName])
                print("The worst-case memory cost is " + str(mem) + " for graph '" + graph.name + "', using sequence '" + seqName + "'")
            case 'back':
                return
            case _: 
                print(graphHelpStr)
        userIn = input('+==>')
    return
#End loop function

def seqLoop(seq):
    """ Loop function giving the user the valid commands/operations for a sequence
        Which are: print, write, evaluate, and back. 
    """
    seqId = seq.name
    seqIdStr = "For Sequence '" + seqId + "'"
    seqHelpStr = "\nSequence commands are: 'print', 'write', 'evaluate', and 'back' (go back)"
    print(seqIdStr + seqHelpStr)
    userIn = input('+==>').strip()  #Could put sedId in input string (before the '>')
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
                    print("Failed (check permissions in path). ;(")
            case 'evaluate':
                #Ask for a graph to test this sequence
                graphName = input("Enter an imported graph name: ") # or a file name for a new graph: ")
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
                    print("The Sequence " + seq.name +  " is INvalid for " + graphName + ".")
            case 'back':
                return
            case 'quit':
                return
            case _:
                print(seqHelpStr)
        #End Match
        userIn = input('+==>')
    #End while
    return
#End seq. loop function

def unitTestAdder1():
    global graphs
    global seqs
    assert structs.isValidSequence(seqs['adder1a'], graphs['adder1']) == False
    assert structs.isValidSequence(seqs['adder1b'], graphs['adder1']) == False
    assert structs.findMemCost(graphs['adder1'], seqs['adder1b']) == 6

    print("Unit Tests Run Successfully.")

# "Main" equivalent
graphs = {}
seqs = {}

#To help with testing, pre-populate graphs and seqs with some graphs and sequences
gr = structs.Graph('adder1')
gr.readGraph('./graphs/adder1.graph')
graphs['adder1'] = gr

seq = structs.Sequence('adder1b')
seq.readSequence('./sequences/adder1b.seq')
seqs['adder1b'] = seq
seq = structs.Sequence('adder1a')
seq.readSequence('./sequences/adder1a.seq')
seqs['adder1a'] = seq


helpStr = "\nCommands are: 'readGraph', 'readSequence', 'show', 'select', 'quit', and 'help'"

print('*' * 50 + "\nWelcome to the Input Parser!" + helpStr)
userIn = input("==>").strip()   # could also .lower()
while userIn != 'quit': # or 'q' or 'exit':     #only the first was working
    match userIn:
        case 'readGraph':
            file_path = input("Enter graph file path: ")
            gr = structs.Graph()
            out = io.readGraph(gr, file_path)
            #if failed
            if not out:
                print('Graph Import Failed. (Check file path?)')
                userIn = ''
                continue #...the while loop
            #Success!
            graphs[gr.name] = gr    #map the string name (gId) to this graph object (gr)
            print('Successfully imported the graph!')
            graphLoop(gr)   #Prompt with further graph options - graph loop function
            #Print the helpStr to help user know where they are after returning from graphLoop
            print(helpStr)
        case 'readSequence':
            seq_path = input("Enter Sequence Path: ")
            seq = structs.Sequence()
            out = io.readSequence(seq, seq_path)    #returns true/false
            # if failed
            if not out:
                print('Failed to import sequence. (Check file name)')
                userIn = '' #To reset user input, and avoid an infinite loop that leads here.
                continue
            # Success!
            seqs[seq.name] = seq #map the string name to this seq. object
            print('Successfully imported sequence')
            seqLoop(seq) # go into a loop of sequence functions for this sequence.

            # Print helpStr when returning from the seqLoop.
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
print("Goodbye! Have a nice day.")
# End 'main'