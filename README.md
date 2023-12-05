# VLSI_Project
Class Project for Computer-Aided Design for VLSI. Tasks are to read in a Directed Acyclic Graph (DAG) as well as an execution sequence, 
determine if the sequence meets predecessor constraints for a graph, calculate the memory cost of the sequence on a graph, and finally to
synthesize a valid sequence. Optionally, the synthesized sequence can be made to minimize the memory cost of the sequence.

Programmed in Python, the files each perform some common functions. 
### InputOutput.py
The inputOutput.py deals with reading the data structures in from a file, as well as writing a sequence to a file, along with some auxiliary functions. 
### DataStructures.py
The dataStructures.py file houses the graph and sequences data structures, along with functions that determine if a sequence is valid, 
finding the memory cost of a sequence, and finally creating a valid sequence.
### MainLoop.py
The mainloop.py acts as a console menu based program that allows the user to import graphs and sequences from the file system and perform these functions on them.
### runAllGraphs.py
The runAllGraphs.py acts as a tester program that runs the provided graphs and sequences with each of the functions.
### inputParser.py
This file is outdated. It was the basis for many function, but was getting to large to work with.
