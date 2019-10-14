Implementation of Thompson’s Construction that converts a regular expressions to it’s equivalent NFA

program takes a regular expression as a string in a text file and outputs a text representation of the equivilant NFA and 
also outputs an image of the NFA represented as graph.

The format of the output file:
  state(s) separated by commas
  alphabet separated by commas
  start state 
  final state(s) separated by commas 
  transition (s) in a tuple form separated by commas, tuples in the form-> (start state , alphabet , result state in array form) 

In the output image of the NFA the blue node represent the start state and green node represent a final state.

How to run:-
  
   from command line:
   python "script_name" --file "text_file_name"

   Example:
   python REGX2NFA.py --file Test.txt