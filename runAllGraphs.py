""" VLSI Project (#2)
    David Patenaude
    File Description: Runs all provided graphs and sequences and reports
        the validity of sequences. Also generates new sequences from a graph.
"""
import dataStructures as structs
import inputOutput as io

BASE = 'adder'
GR_FOLDER = './graphs/'
SEQ_FOLDER = './sequences/'
AUTO_GEN_FOLDER = './autoGenSeqs/'

def importGraphs(graphs):
    """ Imports all the graphs"""
    
    for i in range(0, 6):
        name = BASE + str(2**i)
        file_name = GR_FOLDER + name + '.graph'
        gr = structs.Graph(name)
        out = io.readGraph(gr, file_name)
        
        if not out:
            print('Error reading graph i= ' + str(i))
            return False
        graphs[name] = gr
    print('Graphs Imported Successfully!')
    return True

def importSequences(seqs):
    """ Imports all sequences """

    for i in range(0, 6):
        for j in range(0,2):
            name = BASE + str(2**i)
            if j == 0:
                name = name + 'a'
            else:
                name = name + 'b'
            file_name = SEQ_FOLDER + name + '.seq'
            seq = structs.Sequence(name)
            out = io.readSequence(seq, file_name)

            if not out:
                print('Error reading sequence, i= ' + str(i) + ', j= ' + str(j))
                return False
            seqs[name] = seq
    print('Sequences Imported Successfully!')
    return True

def runValidSequences(graphs, seqs):
    """ Runs all the sequences for each of the graphs.
        input params are dictionaries."""
    usedSeqs = list()
    for graph in graphs:    #gives the keys, not the objects
        for seq in seqs:
            # skip if used already to improve runtime =>premature optimization!
            
            if graph == seqs[seq].graphName:    #if this is the graph for this sequence, check if valid
                #bug: adder1 is contained in adder16a/b ... go on ahead and add a graph name to the sequence object.    
                if structs.isValidSequence(seqs[seq], graphs[graph]):
                    print(f'Sequence \'{seq}\' is VALID for graph \'{graph}\'')
                else:
                    print(f'Sequence \'{seq}\' is INVALID for graph \'{graph}\'')
    return

import time
def runRandomSeqGen(graphs, trueRandom):
    """ Generates a random valid execution sequence for each graph.
        Prints the runtime in milliseconds.
    """
    for graph in graphs.values():
        
        tic = time.perf_counter()   #Start time
        gen_seq = structs.findValidSequence(graph, trueRandom)
        toc = time.perf_counter()   #end time

        import os
        # Check if path exists before trying to mkdir.
        if not os.path.exists(AUTO_GEN_FOLDER):
            os.mkdir(AUTO_GEN_FOLDER)  #make a new directory for generated Sequences if not already exists
        new_path = io.getNewPath(AUTO_GEN_FOLDER + gen_seq.name)    #get next available sequence name
        io.printSeqToFile(gen_seq, new_path)    #print to file
        #Inform the user
        print('Successfully generated a sequence: ' + gen_seq.name + f' in { (toc-tic)*1000 :3.3f} milliseconds')
        print('Printed to: ' + new_path)
    return True

def topSortSequences(graphs):
    """ Runs topological sort on all graphs and then creates a sequence object out of it. 
        It will then return these sequences.
    """
    seqs = {}
    for gr in graphs.values():
        tic = time.perf_counter()
        topSort = gr.topologicalSort()  # perform the sort
        toc = time.perf_counter()

        name = 'top_' + gr.name 
        seq = structs.Sequence(name)    # create sequence structure
        # add each of the nodes in the top sort to the sequence
        for i in range(len(topSort)):
            seq.add(topSort[i])
        seqs[name] = seq    #add the sequence to the dictionary
        print(f'Sequence \'{name}\' generated in {(toc-tic) * 1000 :3.3f} ms')
    
    return seqs

def findMemCost(graphs, sequences):
    """ Run the memory cost function for the valid sequences on each graph
    """
    # function structs.findMemCost will check if the sequence is valid. So we can pass all the sequences and graphs.
    # Loop over each graph structure
    for gr in graphs.values():
        for seq in sequences.values():
            # First see if the sequence goes with the graph.
            if seq.graphName != gr.name:
                continue    #continue to the next sequence
            memCost = structs.findMemCost(gr, seq)
            if memCost != -1:
                print("Sequence '{0}' has a memory cost of {1} for the graph '{2}'".format(seq.name, memCost, gr.name))
            # otherwise a print statement already occurs
    return True

def findRandomMemCosts(graphs):
    """ Runs the generated (random) sequences by importing them first.
    """
    # import sequences from the AUTO_GEN_FOLDER. split file name by '_' to get graph name.
    genSeqs = []
    import glob, os
    file_names = glob.glob(AUTO_GEN_FOLDER + '*.seq')   #glob returns all files that have a .seq extension/ending
    for fileName in file_names:
        grName = fileName.split('_')[1].split('.')[0]   #first split '_', take right substring, then split '.' take left.
        #Extract the name of the sequence
        head, tail = os.path.split(fileName)
        name, ext = os.path.splitext(tail)

        newSeq = structs.Sequence(name)
        newSeq.graphName = grName
        out = io.readSequence(newSeq, fileName)
        if not out:
            print(f'Error reading a generated Sequence. File name {fileName}')
        # Sequence imported successfully, now run the memCost function
        genSeqs.append(newSeq)
    
    #now loop graphs again...
    for gr in graphs.values():
        for gSeq in genSeqs:    #genSeqs is a list, and so gSeq is an object not a string
            if gSeq.graphName != gr.name:
                continue
            memCost = structs.findMemCost(gr, gSeq) #find the memory cost.
            if memCost != -1:   #report the memcost if it is a valid sequence
                print("Sequence '{0}' has a memory cost of {1} for the graph '{2}'".format(gSeq.name, memCost, gr.name))
    return True     #it ran successfully

def main():
    """ The main function of this file. """
    graphs = dict()
    seqs = dict()

    if not importGraphs(graphs):
        print('Aborting after failure')
        return
    if not importSequences(seqs):
        print('Aborting after sequence failure')
        return
    # Successfully imported graphs and sequences, now run is valid on the graphs and sequences.
    userIn = input('Do you want to check the validity of all sequences? (y/n): ')
    if userIn.lower() == 'y':
        print('\nRunning isValidSequence on all Sequences...')
        runValidSequences(graphs, seqs)
        print('...Done running validity checker')

    userIn = input('Do you want to DELETE existing random sequences? (y/n): ')
    if userIn.lower() == 'y':
        import os,glob
        #os.chdir(AUTO_GEN_FOLDER)  #changes dir for rest of execution!
        for file in glob.glob(AUTO_GEN_FOLDER +'*.seq'):
            os.remove(file)
            print(f'File {file} has been deleted.')
        print('Files Deleted\n')

    userIn = input('Do you want to create random valid sequences? (y/n): ')
    if userIn.lower() == 'y':
        uIn2 = input('Do you want true randomness? (y/n): ')
        print('\nGenerating a random sequence for each graph...')
        if uIn2.lower() == 'y':        
            runRandomSeqGen(graphs, True)
        else:
            runRandomSeqGen(graphs, False)
        print('... done generating random (valid) sequences')
    
    # Find the memory consumption of each sequence
    userIn = input('Do you want to find the memory cost of each graph? (y/n): ')
    if userIn.lower() == 'y':
        print('\nEvaluating memory cost for each graph...')
        findMemCost(graphs, seqs)
        print('\nFor the random Sequences:')
        findRandomMemCosts(graphs)  #find cost of the randoms
        print('\n...done evaluating memory cost for the graphs')

    # Now create 'better' sequences 
    print('\nTopologically Sorting the Graphs, and then finding memory consumption...')
    topSeqs = topSortSequences(graphs)  #sort the graphs topologically and store the result in a sequence, returns a dictionary
    findMemCost(graphs, topSeqs)        #find the memory cost and print/report it.
    print('\n...Finished finding topological memory costs')

    print('\nFinished Running Tasks, Goodbye')
    return 0

def promptUser(prompt):
    """ Prompt the user for a true/false answer and check different versions of yes/no"""

    pass

def __main__():
    main()

main()

### To delete all auto generated sequences:
# import os,glob
# os.chdir(AUTO_GEN_FOLDER) #note that it changes for all subsequent calls to os.
# for file in glob.glob(AUTO_GEN_FOLDER +'*.seq'):
#     os.remove(file)