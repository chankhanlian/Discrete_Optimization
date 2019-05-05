#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
import numpy as np
Item = namedtuple("Item", ['index', 'value', 'weight'])


def recursive_dp(row, column):
    global max_array

    if(row==0 or row < 0):
        return 0
    if(column==0):
        return 0
    
    #case where item was not taken
    #calculate max_array(row, column-1)
    if(max_array[row, column-1] < 0):
        temp1=recursive_dp(row, column-1)
    else:
        temp1=max_array[row, column-1]
    
    #item was possibly taken
    #calculate max_array(row-item.weight, column-1)
    if(row-items_list[column].weight<0): #item didn't fit; was not taken
        temp2=0 
        
    elif((max_array[row-items_list[column].weight, column-1] < 0) and \
           row-items_list[column].weight>=0): #item fit, but need to calculate previous cell
        temp2=recursive_dp(row-items_list[column].weight, column-1)+items_list[column].value
    
    else: #item fit, value was previously calculated 
        temp2=max_array[row-items_list[column].weight, column-1]+items_list[column].value

    max_value=max(temp1, temp2)
    max_array[row, column]=max_value

    return int(max_value)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    global max_array
    global items_list
    # parse the input
    lines = input_data.split('\n')
   
    firstLine = lines[0].split()
  
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items_list = []
    
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items_list.append(Item(i-1, int(parts[0]), int(parts[1])))
    
    items_list=sorted(items_list, key=lambda x: x.weight, reverse=False)
    items_list.insert(0, Item(0, 0, 0))
    taken = [0]*item_count
    taken_sorted=[0]*item_count

    
    #initialize max_array to -1s
    max_array=np.empty((capacity+1, item_count+1))  
    max_array[:]=-1
    max_recursion_depth=1000
    
    if(item_count > max_recursion_depth):
    ## Need to handle cases where item_count >1000 separately; will hit Python recursion limit
    #    step_size=max_recursion_depth
    #    step=0
        
    #    while(item_count>step_size*step):
    #        print("step:", step)
    #        if(item_count-step_size*step > step_size):
    #            value=recursive_dp(capacity, step_size*(step+1))
    #        else:
    #            #output=recursive_dp(capacity, item_count)
    #            value=0
    #        step=step+1
        value= 0
    else:
        value= recursive_dp(capacity, item_count)

    
    row=capacity
    for column in range(item_count, 0, -1):
        if(max_array[row][column]!=max_array[row][column-1]):
            if(not(max_array[row][column]==0 and max_array[row][column-1]==-1)):
                taken_sorted[column-1]=1
                row=row-items_list[column].weight

    for i in range(len(taken_sorted)):
        if(taken_sorted[i]==1):
            taken[items_list[i+1].index]=1
    

    with open('output_sorted4.txt', 'w') as f:
        for item in taken_sorted:
            f.write("%s\n" % item)      

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

