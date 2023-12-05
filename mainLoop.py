""" MainLoop.py - Store the looping for the console application,
    imports the data structures and file input from another file/module
        VLSI Project 1
    David Patenaude
    11.9.2023"""

import inputOutput as io;
import dataStructures as structs;
import time
DEBUG = False

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
                gen_seq = structs.Sequence('None')#does this declare a variable?

                in2 = input('Use top sort (yes) or random (no): ').lower().strip()
                if in2 == 'yes':
                    gen_seq = structs.findBetterSequences(graph)
                else:
                    # Would produce a valid sequence for this graph/netlist
                    #Initially, try using Djisktra's algroithm. 
                    # Pass the graph to the function to find a valid sequence
                    tic = time.perf_counter()
                    gen_seq = structs.findValidSequence(graph, False)
                    toc = time.perf_counter()
                    print('Successfully generated a random sequence: ' + gen_seq.name + f' in { (toc-tic)*1000 :2.4f} seconds')

                if structs.isValidSequence(gen_seq, graph):
                    import os
                    if not os.path.exists('./genSeqs/'):
                        os.mkdir('./genSeqs/')  #make a new directory for generated Sequences if not already created
                    new_path = io.getNewPath('./genSeqs/' + gen_seq.name)    #get next available sequence name
                    io.printSeqToFile(gen_seq, new_path)    #print to file
                    #Inform the user
                    print('Printed to: ' + new_path)
                    global seqs
                    seqs[gen_seq.name] = gen_seq
                    print('Imported Sequence!')
                else:
                    print('Error: Generated Sequence invalid!')

            case 'evaluate':
                # Prompt for an imported sequence from the global variable 'seqs' and determine the maximum memory consumption 
                seqName = input("Enter an imported sequence to determine worst-case memory consumption: ")
                #global seqs #seqs is in the global scope
                if seqName not in seqs:
                    print("Sequence '"+ seqName + "' not imported!")   #
                    userIn = '' #attempt to give help prompt on next iteration (could be scope issue)
                    continue
                #Otherwise pass seqs[seqName] 
                mem = structs.findMemCost(graph, seqs[seqName])
                if mem != -1:
                    print("The worst-case memory cost is " + str(mem) + " for graph '" + graph.name + "', using sequence '" + seqName + "'")
                # else is handled in function.
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
                # """ if graphName.find('/') != -1 or graphName.find(backslash) != -1:
                #     # it is a path if it has a / or \ 
                #     name = getFileName(graphName)
                #     global graphs

                #     try:
                #         idx = graphs.index(name)
                #     except ValueError:
                #         pass    #Pretty sure I'll end up with an error of scope again.
                #     if graphs.__contains__(name):
                #         seq.isValidSequence()
                #         pass
                # """
                global graphs
                evalOn = graphs[graphName]
                #out = seq.isValidSequence(evalOn)  # older function no longer used
                out = structs.isValidSequence(seq, evalOn)
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
    """ Unit tests for the adder1 graph to ensure correct code.
    """
    global graphs
    global seqs
    # make sure that the asserted value is correct! (flipped one of the bools)
    assert structs.isValidSequence(seqs['adder1a'], graphs['adder1']) == False
    assert structs.isValidSequence(seqs['adder1b'], graphs['adder1']) == True
    assert structs.findMemCost(graphs['adder1'], seqs['adder1b']) == 6

    print("Unit Tests Run Successfully.\n")

# "Main" equivalent => could make a function main, and then call it at end.
graphs = {}
seqs = {}

#To help with testing, pre-populate graphs and seqs with some graphs and sequences
gr = structs.Graph('adder1')
io.readGraph(gr, './graphs/adder1.graph')
graphs['adder1'] = gr

seq = structs.Sequence('adder1b')
io.readSequence(seq, './sequences/adder1b.seq')
seqs['adder1b'] = seq
seq = structs.Sequence('adder1a')
io.readSequence(seq, './sequences/adder1a.seq')
seqs['adder1a'] = seq

unitTestAdder1()    #Run unit tests

helpStr = "\nCommands are: 'readGraph', 'readSequence', 'show', 'select', 'quit', and 'help'"

print('*' * 50 + "\nWelcome to the Input Parser!" + helpStr)
userIn = input("==>").strip().lower().split(" ")   # could also .lower()
while userIn[0] != 'quit': # or 'q' or 'exit':     #only the first was working
    match userIn[0]:
        case 'readGraph':
            file_path = input("Enter graph file path: ")
            gr = structs.Graph(name=io.getFileName(file_path))
            out = io.readGraph(gr, file_path)
            #if failed
            if not out:
                print('Graph Import Failed. (Check file path?)')
                userIn[0] = ''
                continue #...the while loop
            #Success!
            graphs[gr.name] = gr    #map the string name (gId) to this graph object (gr)
            print('Successfully imported the graph!')
            graphLoop(gr)   #Prompt with further graph options - graph loop function
            #Print the helpStr to help user know where they are after returning from graphLoop
            print(helpStr)
        case 'readSequence':
            seq_path = input("Enter Sequence Path: ")
            seq = structs.Sequence(name=io.getFileName(seq_path))
            out = io.readSequence(seq, seq_path)    #returns true/false
            # if failed
            if not out:
                print('Failed to import sequence. (Check file name)')
                userIn[0] = '' #To reset user input, and avoid an infinite loop that leads here.
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
            grName = ''
            if len(userIn) == 2:
                grName = userIn[1]
            else:
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
            # add extra information to this command?
            print(helpStr)
        case _:
            print(helpStr)
    userIn = input('==>').strip().split(" ")
#End while
print("Goodbye! Have a nice day.")
# End 'main'