################################################
#### Onomateponimo: Vasileios Gkotzagiannis ####
#### Arithmos Mitrwou: 2672                 ####
#### Part 1                                 ####
################################################

import sys
import pymorton
import math

# ### Global Variables #### # 
ID_INCR = 0
TREE_LEVEL = 0
MAX_CAPACITY = 20
MIN_DATA_NUM = 8
# ######################### #

def calculate_mbrs(coords):
    """
    Calculates the mbrs from object coords (leafs only)
    """
    mbrs = []
    for coord in coords:
        mbr = []
        xs = []
        ys = []
        for n in coord:
            # x is in the first place and y in the second of the coord #
            xs.append(float(n[0]))
            ys.append(float(n[1]))
        # Find the min, max in all x's and y's of coords #
        mbr.append(min(xs))
        mbr.append(max(xs))
        mbr.append(min(ys))
        mbr.append(max(ys))
        # Append the new mbr in mbrs #
        mbrs.append(mbr)
    return mbrs

def calculate_z_order(all_mbrs):
    z_order_mbrs = []
    for index, mbr in enumerate(all_mbrs):
        # Find the middle for both x and y #
        x_middle = (mbr[0] + mbr[1]) / 2
        y_middle = (mbr[2] + mbr[3]) / 2
        # Interleave the y,x values and find z-order #
        z_order_mbrs.append([index, pymorton.interleave_latlng(y_middle, x_middle)])
    return z_order_mbrs

def write_to_file(filename, list_to_write, with_enum):
    """
    Util method that writes a list to a file
    """
    with open(f'testfiles/{filename}', "w") as out:
        if with_enum:
            for i, line in enumerate(list_to_write):
                out.write(f"{i}. {line}\n")
        else:
            for line in list_to_write:
                out.write(f"{line}\n")

def construct_r_tree(mbrs, r_tree, isnonleaf):
    """
    Creates the Rtree from the leafs to the root
    """
    global ID_INCR
    global TREE_LEVEL
    global MAX_CAPACITY
    global MIN_DATA_NUM

    new_mbrs = []
    size_of_mbrs = len(mbrs)

    if math.ceil(size_of_mbrs/MAX_CAPACITY) == 1:
        #print("In root")
        r_tree.write(f"[{isnonleaf}, {ID_INCR}, {mbrs}]\n")
        print(f'1 node at level {TREE_LEVEL}.')
        return

    if size_of_mbrs % MAX_CAPACITY == 0: 
        # We have size_of_mbrs/MAX_CAPACITY nodes  with capacity: MAX_CAPACITY  
        for node in range(0, size_of_mbrs//MAX_CAPACITY):
            # create entry for node
            node_data = mbrs[node*MAX_CAPACITY:(node+1)*MAX_CAPACITY]
            #[isnonleaf, node-id, [[id1, MBR1], [id2, MBR2], …, [idn, MBRn]]]
            r_tree.write(f"[{isnonleaf}, {ID_INCR}, {node_data}]\n")
            new_mbrs.append([ID_INCR, node_data])
            ID_INCR += 1
            
    elif size_of_mbrs % MAX_CAPACITY >= MIN_DATA_NUM:
        #print("Fill the remain with the last")
        remain = MAX_CAPACITY - size_of_mbrs % MAX_CAPACITY
        num_of_nodes = math.ceil(size_of_mbrs/MAX_CAPACITY)
        for node in range(0, num_of_nodes):
            # if in last node add the remaining mbrs in node_data
            if node == num_of_nodes - 1:
                node_data = mbrs[node*MAX_CAPACITY:(node+1)*MAX_CAPACITY - remain]
            else:
                node_data = mbrs[node*MAX_CAPACITY:(node+1)*MAX_CAPACITY]
            # [isnonleaf, node-id, [[id1, MBR1], [id2, MBR2], …, [idn, MBRn]]]
            r_tree.write(f"[{isnonleaf}, {ID_INCR}, {node_data}]\n")
            new_mbrs.append([ID_INCR, node_data])
            ID_INCR += 1

    elif size_of_mbrs % MAX_CAPACITY < MIN_DATA_NUM:
        #print("Take from the previous and add to the last")
        remain = MIN_DATA_NUM - size_of_mbrs % MAX_CAPACITY
        num_of_nodes = math.ceil(size_of_mbrs/MAX_CAPACITY)
        for node in range(0, num_of_nodes):
            if node == num_of_nodes - 2:
                node_data = mbrs[node*MAX_CAPACITY:(node+1)*MAX_CAPACITY - remain]
            elif node == num_of_nodes -1:
                node_data = mbrs[node*MAX_CAPACITY - remain:(node+1)*MAX_CAPACITY]
            else:
                node_data = mbrs[node*MAX_CAPACITY:(node+1)*MAX_CAPACITY]
            # [isnonleaf, node-id, [[id1, MBR1], [id2, MBR2], …, [idn, MBRn]]]
            r_tree.write(f"[{isnonleaf}, {ID_INCR}, {node_data}]\n")
            new_mbrs.append([ID_INCR, node_data])
            ID_INCR += 1

    print(f'{len(new_mbrs)} nodes at level {TREE_LEVEL}.')
    TREE_LEVEL += 1

    create_nodes(new_mbrs)        
    construct_r_tree(new_mbrs, r_tree, isnonleaf=1)

def create_nodes(new_mbrs):
    # write_to_file(f'new_mbrs_level{TREE_LEVEL}.txt', new_mbrs, 0)        
    for mbrs in new_mbrs:
        l = []
        for mbr in mbrs[1]:
            l.append(mbr[1])
        mbrs[1] = calculate_mbrs_nonleafs(l)

def calculate_mbrs_nonleafs(mbrs):
    mbr_x_low = []
    mbr_x_high =[]
    mbr_y_low = []
    mbr_y_high = []

    for mbr in mbrs:
        mbr_x_low.append(mbr[0])
        mbr_x_high.append(mbr[1])
        mbr_y_low.append(mbr[2])
        mbr_y_high.append(mbr[3])

    return [min(mbr_x_low), max(mbr_x_high), min(mbr_y_low), max(mbr_y_high)]

def main():
    if (len(sys.argv) < 3):
        print(f"Please enter the coordinates file and the offsets file as command line arguments.\n\
Usage: python part1.py <path to coords file> <path to offsets file>")
        return -1

    objects_coords = []
    coords_lines = []   # will hold the coords file lines

    # Read coords file line by line remove whitespace and ',' and put it in coords_lines
    with open(sys.argv[1], "r") as coords:
        for line in coords.readlines():
            coords_lines.append(line.strip('\n').split(','))

    # Write coords lines in out_coords
    # write_to_file('out_coords.txt', coords_lines, 1)

    # Read offsets file and 
    with open(sys.argv[2], "r") as offsets:
        for line in offsets.readlines():     
            offsets_line = line.strip('\n').split(',')
            coords_list = []
            for i in range(int(offsets_line[1]), int(offsets_line[2])+1):
                coords_list.append(coords_lines[i])
            objects_coords.append(coords_list)

    # write_to_file('out_objects_coords.txt', objects_coords, 0)
    
    all_objects_mbrs = calculate_mbrs(objects_coords)
    # write_to_file('objects_mbrs.txt', all_objects_mbrs, 0)

    z_order_mbrs = calculate_z_order(all_objects_mbrs)
    # Sort the z_orders and save to new list #
    sorted_z_orders = sorted(z_order_mbrs, key = lambda x: x[1])

    # write_to_file('sorted_z_orders.txt', sorted_z_orders, 1)

    # With the sorted z-orders, sort all objects mbrs in a new list #
    sorted_mbrs = []
    for z_order in sorted_z_orders:
        sorted_mbrs.append([z_order[0],all_objects_mbrs[z_order[0]]])

    # write_to_file('sorted_mbrs.txt', sorted_mbrs, 0)
    
    with open('Rtree.txt', 'w') as r_tree:        
        construct_r_tree(sorted_mbrs, r_tree, isnonleaf=0)

if __name__ == '__main__':
    main()
