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

def main():
    if (len(sys.argv) < 4):
        print(f"Please enter the Rtree and the Rtree queries as command line argument.\n\
Usage: python part3.py <path to Rtree file> <path to Rtree queries file> <number k>")
        return -1
    
    k = int(sys.argv[3])
    
    with open(sys.argv[1], 'r') as r_tree, open(sys.argv[2], 'r') as nn_queries:
        for line in r_tree.readlines():
            Rtree.append(ast.literal_eval(str(line).strip()))
    
    # for node_entry in Rtree[len(Rtree)-1][2]:
    #     print(node_entry[1])
        queries = []
        for query_line in nn_queries.readlines():
            query = []
            for number in query_line.strip().split(" "):
                query.append(float(number))
            queries.append(query)
        with open('testfiles/output.txt', 'w') as outp:

            for i, query in enumerate(queries):
                k_nns = best_first_NN_search(query, Rtree, k)
                outp.write((f'{i}: {str(k_nns)[1:-1]}\n'))
    best_first_NN_search([-86.6036, 32.4001], Rtree, k)

def best_first_NN_search(q, Rtree, k):
    p_queue = []    
    heapq.heapify(p_queue)
    for node_entry in Rtree[len(Rtree)-1][2]:
        heapq.heappush(p_queue, (dist(q, node_entry[1]), node_entry[0]))

    print(f'queue is: {p_queue}')

    k_nns = []
    for i in range(0,k):
        k_nns.append(next_BF_NN(q, p_queue))
    return k_nns


def next_BF_NN(q, p_queue):
    while p_queue:
        elem = heapq.heappop(p_queue)
        try:
            node = Rtree[elem[1]]
            for entry in node[2]:                    
                heapq.heappush(p_queue, (dist(q, entry[1]), entry[0])) 
        except IndexError:
            return elem[1]

def dist(q, node_mbr):
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


# def inc_near(q, Rtree):
#     p_q = []
#     heapq.heapify(p_q)
#     for node_entry in Rtree[len(Rtree)-1][2]:
#         heapq.heappush(p_q, (dist(q, node_entry[1]), node_entry[0]))

#     for i in range(0,10):
#         while p_q:
#             elem = heapq.heappop(p_q)
#             try:
#                 node = Rtree[elem[1]]
#                 for entry in node[2]:
#                     heapq.heappush(p_q, (dist(q, entry[1]), entry[0]))
#             except IndexError:
#                 if p_q and p_q[0][0] < elem[0]:
#                     heapq.heappush(p_q, (elem[1], elem[0]))
#                 else:
#                     print(elem[1], end=', ')
#                     break



main()