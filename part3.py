################################################
#### Onomateponimo: Vasileios Gkotzagiannis ####
#### Arithmos Mitrwou: 2672                 ####
#### Part 3                                 ####
################################################

import sys
import ast
import heapq
import math

Rtree = []

def best_first_NN_search(q, Rtree, k):
    """
    Finds and returns the k nearest neighbors incrementally
    """
    p_queue = []    
    heapq.heapify(p_queue)
    for node_entry in Rtree[len(Rtree)-1][2]:
        heapq.heappush(p_queue, (dist(q, node_entry[1]), node_entry[0], 1))

    k_nns = []
    for _ in range(0,k):
        k_nns.append(next_BF_NN(q, p_queue))
    return k_nns

def next_BF_NN(q, p_queue):
    """
    Finds and returns the next nearest neighbor
    """
    while p_queue:
        elem = heapq.heappop(p_queue)
        # Node MBR
        if elem[2] == 1: 
            node = Rtree[elem[1]]
            # Non-leaf entry
            if node[0] == 1: 
                for entry in node[2]:
                    heapq.heappush(p_queue, (dist(q, entry[1]), entry[0], 1))
            # Leaf entry
            elif node[0] == 0:
                for entry in node[2]:
                    heapq.heappush(p_queue, (dist(q, entry[1]), entry[0], 0))
        # Object MBR
        elif elem[2] == 0: 
            return elem[1]

def dist(q, node_mbr):
    """
    Calculates the distance between the query and the MBR
    """
    x = float(q[0])
    y = float(q[1])
    dx = 0
    dy = 0
    x_low = float(node_mbr[0])
    x_high = float(node_mbr[1])
    y_low = float(node_mbr[2])
    y_high = float(node_mbr[3])

    if x < x_low: 
        dx = x_low - x
    if x > x_high: 
        dx = x - x_high

    if y < y_low: 
        dy = y_low - y
    if y > y_high: 
        dy = y - y_high

    return math.sqrt(dx**2 + dy**2)

def main():
    if (len(sys.argv) < 4):
        print(f"Please enter the Rtree and the Rtree queries as command line argument.\n\
Usage: python part3.py <path to Rtree file> <path to Rtree queries file> <number k>")
        return -1
    
    k = int(sys.argv[3])
    
    with open(sys.argv[1], 'r') as r_tree, open(sys.argv[2], 'r') as nn_queries:
        for line in r_tree.readlines():
            Rtree.append(ast.literal_eval(str(line).strip()))

        queries = []
        for query_line in nn_queries.readlines():
            query = []
            for number in query_line.strip().split(" "):
                query.append(float(number))
            queries.append(query)

    for i, query in enumerate(queries):
        k_nns = best_first_NN_search(query, Rtree, k)
        print((f'{i}: {str(k_nns)[1:-1]}'))

if __name__ == '__main__':
    main()