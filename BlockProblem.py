from copy import deepcopy
import time


class State: #Each State object represents a possible arrangement of the blocks on the table.
    

    def __init__(self,  layout,  parent  =  None,  move=[],  distance  =  0): 
        self.layout = layout
        self.parent = parent #parent of the current state
        self.move  =  move #represents the move from which the current state is created. 
        self.distance = distance #distance from the inital state.

        values = list(self.layout.values())
        self.id  =  ''.join([str(i)  for  s  in  values  for  i  in  s]) # A string which is unique for each state. 

    def __eq__(self, other_state):
        if  other_state  !=  None:
            return self.id == other_state.id #Two states are equal if and only if they have the same id.
        else:
            return False

    def calcChildren(self):
        # moves all free blocks to all free destinations to create all possible combinations
        layout = self.layout 
        children = []

        free_blocks  =  [key  for  key  in  layout  if  layout[key][1]  ==  'c']  #The blocks that can be moved
        
        for block in free_blocks:    #For each free block that will be moved
            for target in free_blocks:
                if block != target:
                    temp = deepcopy(layout)  #Copy the current layout in order to alter it.
                    move = []
                    distance = 0
                    released_block  =  temp[block][0]  #The 'released_block' is the first item of the list in layout with key == moving_block.
                    temp[block][0]  =  target #The 'moving block' now is on top of the 'target_block'.
                    temp[target][1]  =  'u'    #And the 'target_block' is now unclear.
                    move.append(block) #Add the 'moving_block' to 'move' list.

                    if released_block != '-':  #If the 'released_block' is not on the table.
                        temp[released_block][1]  =  'c' #Set the block clear.
                        move.append(released_block) #Add the 'released_block' to 'move' list.
                    else:
                        move.append('table')  

                    move.append(target) #Add the 'target_block' to 'move' list.
                    distance = self.distance + 1 #The distance of the child is the distance of the parent plus 1.

                    children.append(State(layout  =  temp,  parent  =  self,  move  =  move,  distance = distance))  #Add to 'children' list a new State object.

            if  layout[block][0]  !=  '-':  #If the 'moving_block' is not currently on the table, create a state that it is.
                temp = deepcopy(layout) 
                move = []
                distance = 0
                released_block  =  temp[block][0] #The 'released_block' is the first item of the list in layout with key == moving_block.
                temp[block][0]  =  '-'
                temp[released_block][1]  =  'c'  #Set the block clear.

                move.append(block) #Add the 'moving_block' to 'move' list.
                move.append(released_block)  #Add the 'released_block' to 'move' list.
                move.append('table')

                distance = self.distance + 1  #The distance of the child is the distance of the parent plus 1.

                children.append(State(layout  =  temp,  parent  =  self,  move  =  move,  distance = distance)) #Add to 'children' list a new State object.

        return children #Return the children list.


def depth_first_search(current_state, goal_state, timeout, defined_depth, depth):
    
        S = []     #A stack fot storing the nodes/states
        discovered = set()     #A set for keeping the ids of the discovered states.

        S.append(current_state)     #Add the current/initial state to the stack.


        st = time.perf_counter()     

        while S:     
            if time.perf_counter() - st > timeout:     #If the execution time exceeds the timeout
                print('Timeout!')
                return None       #Break.

            state = S.pop()      #Pop an element from the top of S.

            if state == goal_state:      #If the state is the goal state, return it and break.
                steps = []
                while state != None:
                    steps.append(state.layout)
                    if(state != initial_state):
                        steps.append('\nmove block '+str(state.move[0])+' from '+str(state.move[1])+' to '+str(state.move[2])+':')

                    state = state.parent
                steps.reverse()
                for step in steps:
                    print(step)
                return goal_state

            if state.id in discovered:      #If the state has been discovered, do nothing.
                continue
        
            if defined_depth and state.distance >= depth: #for depth limited search if it exceeds specified depth continue 
                continue

            children = state.calcChildren()     #Else, calculate the children of this state.

            for child in children:     #For each child append it to S
                S.append(child)     

            discovered.add(state.id)     #Mark state as discovered.

initial_state = State(layout = {'A': ['-', 'u'], 'B': ['-', 'c'], 'C': ['A', 'c']}) 
goal_state = State(layout = {'A': ['-', 'u'], 'B': ['A', 'u'], 'C': ['B', 'c']})

soln = depth_first_search(initial_state, goal_state, 300, False, -1)
 
if  soln  ==  None:
    print('No  solution  found  upto  depth '+ str(depth))
