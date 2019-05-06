#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import random 
from collections import namedtuple
import math

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    global points
    
    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    tour_list=list(range(0, nodeCount))
    min_solution=[]
    min_dist=-1

    if nodeCount>10000:
        cluster_size=2000
        clusters=int(nodeCount/cluster_size)
        x_values=list(map(lambda z: z.x, points))
        y_values=list(map(lambda z: z.y, points))
        X=np.column_stack((x_values,y_values))
        k_means=KMeans(n_clusters=clusters, random_state=0).fit(X)

        labels=k_means.labels_.tolist()
        tour=list(range(0, nodeCount))
        all_data=np.column_stack((labels, tour))


        for label in range(0, clusters):
            cl=all_data[all_data[:,0] ==label,1]
            cl=cl.tolist()
            random.shuffle(cl)
            temp=nearest_neighbor(cl, 1)

            temp=two_opt(temp, cluster_size, 1, 1)
            temp=two_opt(temp, cluster_size*10, 1, 0)
            min_solution=min_solution+temp[int(len(cl)/100):] + temp[:int(len(cl)/100)]

        min_solution=two_opt(min_solution, nodeCount, 1, 0)

    else:
        min_solution=[]
        min_dist=-1
        iterations=5 #max(50, int(nodeCount/30))
        tour=nearest_neighbor(tour_list, 1)
        
        for _ in range(0, iterations):
            tour=nearest_neighbor(tour_list, 1)
            temp=two_opt(tour, nodeCount**2, 1, 1) 
            for __ in range(0, iterations):                          
                temp=two_opt(temp, nodeCount**2, 1, 0)
                test_length=length_of_tour(temp, points)
        
                if(min_dist==-1 or test_length<min_dist):
                    min_solution=temp
                    min_dist=test_length
    
    obj=length_of_tour(min_solution, points)
    solution=min_solution

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    return output_data

    
def length_of_tour(node_list, points_list):
    obj = length(points[node_list[-1]], points[node_list[0]])
    for index in range(0, len(node_list)-1):
        obj += length(points[node_list[index]], points[node_list[index+1]])
    return obj


def two_opt(nodes_list, edges, iterations, deterministic):
    global points
    
    nodeCount=len(nodes_list)
    min_dist=length_of_tour(nodes_list, points)
    min_tour=nodes_list.copy()
    tour=nodes_list.copy()
    #import pdb; pdb.set_trace()
    for k in range(0, iterations):
    #a-b-....-c-d-...
    #a-c-....-b-d
        if(not deterministic):
            rand_indices=[(random.randrange(0, nodeCount), random.randrange(0, nodeCount)) for _ in range(edges)]
            #print(rand_indices)
            for pair in rand_indices:
                indexa=min(pair)
                indexb=(indexa+1)%nodeCount
                indexc=max(pair)
                indexd=(indexc+1)%nodeCount
                if(indexa+2<indexd):
                    vertexa=tour[indexa]
                    vertexb=tour[indexb]
                    vertexc=tour[indexc]
                    vertexd=tour[indexd]

                    old_edge1=length(points[vertexa], points[vertexb])
                    old_edge2=length(points[vertexc], points[vertexd])

                    new_edge1=length(points[vertexa], points[vertexc])
                    new_edge2=length(points[vertexb], points[vertexd])

                    current=old_edge1+old_edge2
                    candidate=new_edge1+new_edge2

                    if(candidate < current):

                        if(indexd!=0):
                            tour=tour[:indexb]+tour[indexc:indexb:-1]+tour[indexb:indexb+1]+tour[indexd:]
                        else:
                            tour=tour[:indexb]+tour[indexc:indexb:-1]+tour[indexb:indexb+1]
                
        else:
            for i in range(0, nodeCount):
                for j in range(i+2, nodeCount):
                    indexa=i
                    indexb=(indexa+1)%nodeCount
                    indexc=j
                    indexd=(indexc+1)%nodeCount
                    vertexa=tour[indexa]
                    vertexb=tour[indexb]
                    vertexc=tour[indexc]
                    vertexd=tour[indexd]

                    old_edge1=length(points[vertexa], points[vertexb])
                    old_edge2=length(points[vertexc], points[vertexd])

                    new_edge1=length(points[vertexa], points[vertexc])
                    new_edge2=length(points[vertexb], points[vertexd])

                    current=old_edge1+old_edge2
                    candidate=new_edge1+new_edge2

                    if(candidate < current):

                        if(indexd!=0):
                            tour=tour[:indexb]+tour[indexc:indexb:-1]+tour[indexb:indexb+1]+tour[indexd:]
                        else:
                            tour=tour[:indexb]+tour[indexc:indexb:-1]+tour[indexb:indexb+1]


        test_length=length_of_tour(tour, points)
        if(test_length<min_dist):
            min_tour=tour
            min_dist=test_length
        
    return min_tour
        
def nearest_neighbor(neighborhood, iterations):
    w=len(neighborhood)
    min_tour_dist=-1
    min_tour=[]

    
    start_nodes=random.sample(range(w),iterations)
    
    for j in range(0, iterations):
        visited=[0]*w
        remaining_nodes=neighborhood.copy()
        curr_vertex=neighborhood[start_nodes[0]]
        visited[start_nodes[0]]=1
        tour=[]
        tour.append(curr_vertex)

        remaining_nodes.remove(curr_vertex)

    
        while(remaining_nodes):
            min_index=-1
            min_dist=99999999
            for i in range(0, w):
                if(length(points[curr_vertex],points[neighborhood[i]])<min_dist and neighborhood[i]!=curr_vertex and visited[i]==0):
                    min_index=i
                    min_dist=length(points[curr_vertex],points[neighborhood[i]])
            
                
            visited[min_index]=1 
            remaining_nodes.remove(neighborhood[min_index])
            curr_vertex=neighborhood[min_index]
            tour.append(curr_vertex)
        
        test_length=length_of_tour(tour, points)
        if(min_tour_dist==-1 or test_length<min_tour_dist):
            min_tour=tour
            min_tour_dist=length_of_tour(tour, points)

    return min_tour





import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

