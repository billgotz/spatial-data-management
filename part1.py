import sys
import pymorton

class R_Tree:

    def __init__(self, nodes):
        self.nodes = nodes

    def add_node(self, node):
        self.nodes.append(node)

    def print_nodes(self):
        for node in self.nodes:
            print(f'{node} \n')
        
MAX_CAPACITY = 20
ID_INCR = 0

def main():
    if (len(sys.argv) < 3):
        print(f"Please enter the coordinates file and the offsets file as command line arguments.\n\
Usage: python part1.py <path to coords file> <path to offsets file>")
        return -1

    objects_coords = {}
    coords_lines = []   # will hold the coords file lines

    # Read coords file line by line remove whitespace and ',' and put it in coords_lines
    with open(sys.argv[1], "r") as coords:
        for line in coords.readlines():
            coords_lines.append(line.strip('\n').split(','))

    # Write coords lines in out_coords
    with open('files/out_coords.txt', "w") as out:
        for i, line in enumerate(coords_lines):
            out.write(f"{i}. {line}\n")

    # Read offsets file and 
    with open(sys.argv[2], "r") as offsets:
        for line in offsets.readlines():     
            offsets_line = line.strip('\n').split(',')
            coords_list = []
            for i in range(int(offsets_line[1]), int(offsets_line[2])+1):
                coords_list.append(coords_lines[i])
            objects_coords[offsets_line[0]] = coords_list

        with open('files/out_objects_coords.txt', "w") as out:
            for key,value in objects_coords.items():
                out.write(f"[KEY]: {key}\n[VALUES]: \n{value}\nEND OF VALUES\n")
        #print(objects_coords)
    
    all_objects_mbrs = []
    for key, value in objects_coords.items():
        mbr = []
        object_xs = []
        object_ys = []
        for n in value:
            object_xs.append(float(n[0]))
            object_ys.append(float(n[1]))
        # print(f'objects x are: {object_xs}\n')
        # print(f'objects y are: {object_ys}\n')
        # print(f'min x is: {min(object_xs)}\n')
        # print(f'min y is: {min(object_ys)}\n')
        # print(f'max x is: {max(object_xs)}\n')
        # print(f'max y is: {max(object_ys)}')
        mbr.append(min(object_xs))
        mbr.append(max(object_xs))
        mbr.append(min(object_ys))
        mbr.append(max(object_ys))
        #print(f'mbr are: {mbr}')
        all_objects_mbrs.append(mbr)

    z_order_mbrs = {}
    for index, mbr in enumerate(all_objects_mbrs):
        #print(f'{index} mbr is: {mbr}')
        # print (f'{index} diff x is: {mbr[1] - mbr[0]}')
        # print (f'{index} diff y is: {mbr[3] - mbr[2]}')
        x_middle = (mbr[0] + mbr[1]) / 2
        y_middle = (mbr[2] + mbr[3]) / 2
        #print(f'{index} pymorton is: {}')
        z_order_mbrs[index] = pymorton.interleave_latlng(y_middle, x_middle) 
        #z_order_mbrs.append(pymorton.interleave_latlng(x_middle, y_middle))
        #print(f'{index} y pymorton is: {pymorton.interleave_latlng(}')
    # for key,value in objects_coords.items():
    #     print(key.get[])
    #     mbrs.append()
    # with open('z_order_unsorted.txt', 'w') as fi:
    #     for i, val in enumerate(z_order_mbrs):
    #         fi.write(f'{val}\n')

    #z_order_mbrs = 
    #z_order_mbrs.sort(key = func)
    #sorted_mbrs = {}
    sorted_mbrs = []
    with open('files/z_order.txt', 'w') as fi:
        for key, val in sorted(z_order_mbrs.items(), key=func):
            fi.write(f'{key}. {val}\n')
            #sorted_mbrs[key] = (all_objects_mbrs[key])
            sorted_mbrs.append([key, all_objects_mbrs[key]])

    with open('files/sorted_Mbrs.txt', 'w') as f2:
        for mbr in sorted_mbrs:
            f2.write(f'{mbr}\n')
    # print(all_objects_mbrs[5868])
    # x_middle = all_objects_mbrs[5868][0] + all_objects_mbrs[5868][1] / 2
    # y_middle = all_objects_mbrs[5868][2] + all_objects_mbrs[5868][3] / 2
    # print(f'5868 pymorton is: {pymorton.interleave_latlng(x_middle, y_middle)}')
   
    #for key, val in z_order_mbrs.items():
    #    print(all_objects_mbrs[key])
    #for

    print(f'len of z_order mbrs: {len(z_order_mbrs)}')
    print(f'len of sorted_mbrs: {len(sorted_mbrs)}')

    #tmp_mbrs = []
    # with open('a.txt', 'w') as f:
    #     for m,v in sorted_mbrs.items():
    #         tmp_mbrs.append([m, v])

    with open('Rtree.txt', 'w') as r_tree:
        isnonleaf = 0
        create_tree(sorted_mbrs, len(sorted_mbrs), r_tree, 0)
    # tree = R_Tree(z_order_mbrs)
    # #tree.add_node(z_order_mbrs[0])
    # tree.print_nodes()

def create_tree(mbrs, msize, r_tree, isnonleaf):
    global ID_INCR
    list_mbrs = list(mbrs)
    lvl = 0
    if msize % MAX_CAPACITY == 0:
        print("YES IT CAN")
        nodes = msize//MAX_CAPACITY
        a_nodes = []
        
        for i in range(0, nodes):
            list_mbrs = mbrs[:MAX_CAPACITY]
            mbrs = mbrs[MAX_CAPACITY:]
            a_nodes.append(create_child(r_tree, list_mbrs, isnonleaf))

        print(f"{nodes} nodes at level {lvl}\n")
        create_tree(a_nodes, len(a_nodes), r_tree, 1)

    else:
        print("NO IT CAN'T")
        nodes = msize//MAX_CAPACITY 
        print(f'{nodes+1} nodes at level {lvl}\n')
        #create_tree()
         


def create_child(r_tree,mbrs, isnonleaf):
    global ID_INCR
    node_cont =[]
    for k in mbrs:
        node_cont.append(k)
    r_tree.write(f'[{isnonleaf}, {ID_INCR}, {mbrs}]\n')
    #r_tree.write(f'[0 , {ID_INCR}, {node_cont}\n')
    ID_INCR += 1
    return node_cont

def func(e):
    return e[1]

main()