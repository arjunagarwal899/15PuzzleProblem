#!/usr/bin/env python3
import time
import numpy
from heapq import * # See heapq_test.py file to learn how to use. Visit : https://docs.python.org/3/library/heapq.html

### Don't use fancy libraries. Evaluators won't install fancy libraries. You may use Numpy and Scipy if needed.
### Send an email to the instructor if you want to use more libraries.


# ********************************************************************


#                 YOUR CODE SHOULD GO HERE.

#                 WRITE YOUR CODE IN AN EASY TO READ MANNER.

#                 YOU MAY USE SEVERAL CLASSES AND FUNCTIONS 


#                 MODIFY THE BODY OF THE FUNCTION FindMinimumPath()



def FindMinimumPath(initialState,goalState):
    minPath=[] # This list should contain the sequence of actions in the optimal solution
    nodesGenerated=0 # This variable should contain the number of nodes that were generated while finding the optimal solution
    
    ### Your Code for FindMinimumPath function
    ### Write your program in an easy to read manner. You may use several classes and functions.
    ### Your function names should indicate what they are doing
    
    
    ### Your Code ends here. minPath is a list that contains actions.
    ### For example, minPath = ['Up','Right','Down','Down','Left']
    
    return minPath, nodesGenerated



#**************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
    with open("initial_state4.txt", "r") as file: #IMP: If you change the file name, then there will be an error when
                                                        #               evaluators test your program. You will lose 2 marks.
        initialState = [[x for x in line.split()] for i,line in enumerate(file) if i<4]
    return initialState

def ShowState(state,heading=''):
    print(heading)
    for row in state:
        print(*row, sep = " ")

def main():
    initialState = ReadInitialState()
    ShowState(initialState,'Initial state:')
    goalState = [['0','1','2','3'],['4','5','6','7'],['8','9','A','B'],['C','D','E','F']]
    ShowState(goalState,'Goal state:')
    
    start = time.time()
    minimumPath, nodesGenerated = FindMinimumPath(initialState,goalState)
    timeTaken = time.time() - start
    
    if len(minimumPath)==0:
        minimumPath = ['Up','Right','Down','Down','Left']
        print('Example output:')
    else:
        print('Output:')

    print('   Minimum path cost : {0}'.format(len(minimumPath)))
    print('   Actions in minimum path : {0}'.format(minimumPath))
    print('   Nodes generated : {0}'.format(nodesGenerated))
    print('   Time taken : {0} s'.format(round(timeTaken,4)))

if __name__=='__main__':
    main()
