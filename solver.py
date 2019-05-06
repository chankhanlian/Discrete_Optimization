#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
global edges #list
global coloring #list
global min_color #integer for minimum number of colors used 
global edge_matrix #matrix
global node_count
import pdb
import random
global curr_coloring
global curr_min

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    global edges
    global coloring
    global edge_matrix
    global min_color
    global node_count
    global curr_min
    global curr_coloring

    
    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    
    edges=[]
    edge_matrix = np.zeros((node_count, node_count))
    #coloring=np.zeros((node_count, node_count))
    assign_color=[-1]*node_count
    #assign_color=[0]
    min_color=node_count
    coloring=[]

    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
        edge_matrix[int(parts[0])][int(parts[1])]=1
        edge_matrix[int(parts[1])][int(parts[0])]=1
        
    for loops in range(0, 100):
        random.seed(loops)
        curr_min=node_count
        curr_coloring=[]
        vertex_order=sort_vertices()
        #vertex_order=list(range(0, node_count))
        #print("vertex_order", vertex_order)

        index=0
        assign_color[vertex_order[0]]=0
        graph_color(assign_color, vertex_order, index)
        if(curr_min<min_color):
            min_color=curr_min
            coloring=curr_coloring
        
    #print("feasible: ", feasible(coloring))
    solution = coloring
    #solution=range(0, node_count)
    # prepare the solution in the specified output format
    output_data = str(min_color) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def graph_color(assign, vertex_order, index):
    global curr_min
    global curr_coloring
    global loops
    global node_count
    
    #if coloring is feasible and all vertices have been assigned a color, then
    #update global min if coloring is better than the current solution
    if(all(i >=0 for i in assign)): # and feasible(assign)):
    #if(len(assign)==node_count):
        num_colors=max(assign)+1
        if(num_colors < curr_min):
            curr_min= num_colors
            curr_coloring= assign
    else:
        #determine domain of colors for the next vertex
        #for each color in domain, try
        #call graph_color on new coloring
        domain=calc_domain(vertex_order[index+1], assign) #domain contains only feasible colors
        
        for color in domain:
            if(curr_min < node_count):
                return
            else:
                test_assign=assign.copy()
                test_assign[vertex_order[index+1]]=color
                graph_color(test_assign, vertex_order, index+1)

                
def calc_domain(vertex, coloring):
    global node_count
    #print("calc domain ", vertex, coloring)
    #given a vertex and a current feasible coloring, return a list of possible colors for that vertex
    #vertex is a integer, coloring is a list (of length n) of the current coloring
    
    #start with the list of colors used in the current coloring plus one new color
    color_domain=list(range(0, max(coloring)+2))
    #eliminate any bad colors (colors of vertices connected to the vertex in question)
    for check_vert in range(len(coloring)):
        if(edge_matrix[vertex][check_vert]==1): #there is an edge connecting vertex and check_vert
            color_to_remove=coloring[check_vert]
            if(color_to_remove in color_domain): #remove that color from the domain if it exists
                color_domain.remove(color_to_remove)
    
    return color_domain


def sort_vertices():
    vertex_order=[]
    edge_matrix_copy=edge_matrix.copy()
    #print("edge matrix", edge_matrix)
    remaining_vertices=list(range(0, node_count))
    sort_helper(edge_matrix_copy,vertex_order, remaining_vertices)
    return vertex_order


def sort_helper(edges_copy, vertex_list, remaining_list):
    if(len(vertex_list)<node_count):
        degrees=edges_copy.sum(axis=1)
        degree_pairs=[]
    
        for i in range(node_count):
            degree_pairs.append((i, degrees[i]))

        degree_pairs.sort(key=lambda x: -x[1])
        
        max_degree_list=[]
        max_degree=degree_pairs[0][1]
    
        #print(max_degree)
        #find list of vertices with max degrees
        if(max_degree==0):
            for x in remaining_list:
                vertex_list.append(x)
        else:
            i=0
            while(degree_pairs[i][1]==max_degree and i<node_count):
                max_degree_list.append(degree_pairs[i])
                i=i+1
                    #print("max_degree_list", max_degree_list)
            #pick random vertex
            remove_vertex=random.choice(max_degree_list)
            #print("random vert to remove", remove_vertex)
            remaining_list.remove(remove_vertex[0])
            vertex_list.append(remove_vertex[0])
            #print("remaining", remaining_list)
        
            #zero out row and column of edges_copy
            edges_copy[remove_vertex[0],:]=0
            #print("edges_copy row", edges_copy)
            edges_copy[:,remove_vertex[0]]=0
            #print("edges copy", edges_copy)
            sort_helper(edges_copy, vertex_list, remaining_list)
            
            
    
def feasible(color):
# color is an assignment coloring, in the form of a list; check that it is feasible
# color=[0, 1, 2, 1] means that node 0 has color 0, nodes 1 and 3 color 1 and node 2 is colored 2

    feasible_boolean=True
    for i in range(len(edges)):
        vertex_1=edges[i][0]
        vertex_2=edges[i][1]
        if((color[vertex_1]==color[vertex_2]) and color[vertex_1]>-1 and color[vertex_2]>-1):
            feasible_boolean=False
            return feasible_boolean
    
    return feasible_boolean

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

