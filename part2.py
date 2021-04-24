################################################
#### Onomateponimo: Vasileios Gkotzagiannis ####
#### Arithmos Mitrwou: 2672                 ####
#### Part 2                                 ####
################################################

import sys
import ast

Rtree = []
filter_step_nodes = []
filter_step_hits = 0

def range_query(Wquery, node):
    """
    The node is tested against the query
    """
    global Rtree
    global filter_step_nodes
    global filter_step_hits
    if node[0] == 1:
        for entry in node[2]:
            node_inter = intersects(Wquery, entry)
            if node_inter:
                range_query(Wquery, Rtree[node_inter])
    else:
        for entry in node[2]:
            node_inter = intersects(Wquery, entry)
            if node_inter:
                filter_step_hits += 1
                filter_step_nodes.append(node_inter)

def intersects(query, entry_with_id):
    """
    Checks if a window query intersects with a given node
    """
    entry = entry_with_id[1]    
    if adjacent(query, entry) or contains(query, entry) or inside(query, entry) or equals(query, entry):
        return entry_with_id[0]            
    return False

def adjacent(query, entry):
    """
    Util function that checks if a window query overlaps or is adjacent to a given node
    """
    x_low = entry[0]
    x_high = entry[1]
    y_low = entry[2]
    y_high = entry[3]

    xlow_q = query[0]
    ylow_q = query[1]
    xhigh_q = query[2]
    yhigh_q = query[3]

    return (xhigh_q > x_high and xlow_q < x_low and (y_low <= ylow_q <= y_high or y_low <= yhigh_q <= y_high)) or \
       (yhigh_q > y_high and ylow_q < y_low and (x_low <= xlow_q <= x_high or x_low <= xhigh_q <= x_high)) or \
       (x_low <= xlow_q <= x_high and (y_low <= ylow_q <= y_high or y_low <= yhigh_q <= y_high)) or \
       (x_low <= xhigh_q <= x_high and (y_low <= ylow_q <= y_high or y_low <= yhigh_q <= y_high))

def contains(query, entry):
    """
    Util function that checks if a window query contains a given node
    """
    x_low = entry[0]
    x_high = entry[1]
    y_low = entry[2]
    y_high = entry[3]

    xlow_q = query[0]
    ylow_q = query[1]
    xhigh_q = query[2]
    yhigh_q = query[3]

    return xlow_q < x_low and xhigh_q > x_high and ylow_q < y_low and yhigh_q > y_high

def inside(query, entry):
    """
    Util function that checks if a window query is inside a given node
    """
    x_low = entry[0]
    x_high = entry[1]
    y_low = entry[2]
    y_high = entry[3]

    xlow_q = query[0]
    ylow_q = query[1]
    xhigh_q = query[2]
    yhigh_q = query[3]

    return xlow_q > x_low and xhigh_q < x_high and ylow_q > y_low and yhigh_q < y_high

def equals(query, entry):
    """
    Util function that checks if a window query equals a given node
    """
    x_low = entry[0]
    x_high = entry[1]
    y_low = entry[2]
    y_high = entry[3]

    xlow_q = query[0]
    ylow_q = query[1]
    xhigh_q = query[2]
    yhigh_q = query[3]

    return xlow_q == x_low and xhigh_q == x_high and ylow_q == y_low and yhigh_q == y_high

def main():
    global filter_step_nodes
    global filter_step_hits
    
    if (len(sys.argv) < 3):
        print(f"Please enter the Rtree and the Rtree queries as command line argument.\n\
Usage: python part2.py <path to Rtree file> <path to Rtree queries file>")
        return -1

    with open(sys.argv[1], 'r') as r_tree, open(sys.argv[2], 'r') as r_queries:
        for line in r_tree.readlines():
            Rtree.append(ast.literal_eval(str(line).strip()))

        w_queries = []
        for query_line in r_queries.readlines():
            w_query = []
            for number in query_line.strip().split(" "):
                w_query.append(float(number))
            w_queries.append(w_query)

    for i, w_query in enumerate(w_queries):
        filter_step_nodes = []
        filter_step_hits = 0
        range_query(w_query, Rtree[len(Rtree)-1])
        print(f'{i} ({filter_step_hits}): {str(filter_step_nodes)[1:-1]}')

if __name__ == '__main__':
    main()