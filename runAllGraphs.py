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
            #if usedSeqs
            # import re
            # re.search(graph, seq)
            if graph == seqs[seq].graphName:    #if the graphs name is contained in the sequence name.
                #bug: adder1 is contained in adder16a/b ... go on ahead and add a graph name to the sequence object.    
                if structs.isValidSequence(seqs[seq], graphs[graph]):
                    print(f'Sequence \'{seq}\' is VALID for graph \'{graph}\'')
                else:
                    print(f'Sequence \'{seq}\' is INVALID for graph \'{graph}\'')
    return

def runRandomSeqGen(graphs, trueRandom):
    """ Generates a random valid execution sequence for each graph.
        Includes runtime.
    """
    for graph in graphs.values():
        import time
        tic = time.perf_counter()   #Start time
        gen_seq = structs.findValidSequence(graph, trueRandom)
        toc = time.perf_counter()   #end time

        import os
        # Check if path exists before trying to mkdir.
        if not os.path.exists(AUTO_GEN_FOLDER):
            os.mkdir(AUTO_GEN_FOLDER)  #make a new directory for generated Sequences if not already
        new_path = io.getNewPath(AUTO_GEN_FOLDER + gen_seq.name)    #get next available sequence name
        io.printSeqToFile(gen_seq, new_path)    #print to file
        #Inform the user
        print('Successfully generated a sequence: ' + gen_seq.name + f' in { (toc-tic)*1000 :3.3f} milliseconds')
        print('Printed to: ' + new_path)

    return True
def findMemCost():
    """ Run the memory cost function for the valid sequences on each graph

    """
    pass

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
    print('\nRunning isValidSequence on all Sequences...')
    runValidSequences(graphs, seqs)
    print('...Done running validity checker')
    print('\nGenerating a random sequence for each graph...')
    runRandomSeqGen(graphs, False)
    print('... done generating random (valid) sequences');
    # Find the memory consumption of each sequence
    print('\nEvaluating memory cost for each graph with their valid sequences...')
    
    # Now create better sequences 

    pass

def __main__():
    main()

main()