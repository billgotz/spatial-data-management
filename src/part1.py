import sys
import pymorton
from src import consts

def calculate_mbrs(coords):
    mbrs = []
    for coord in coords:
        mbr = []
        xs = []
        ys = []
        
        for n in coord:
            xs.append(float(n[0]))
            ys.append(float(n[1]))

        mbr.append(min(xs))
        mbr.append(max(xs))
        mbr.append(min(ys))
        mbr.append(max(ys))

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
            objects_coords.append(coords_list)

        with open('files/out_objects_coords.txt', "w") as out:
            for coord in objects_coords:
                out.write(f"{coord}\n")
    
    all_objects_mbrs = calculate_mbrs(objects_coords)
    
    with open("files/objects_mbrs.txt", 'w') as f:
        for objmbr in all_objects_mbrs:
            f.write(f'{objmbr}\n')

    z_order_mbrs = calculate_z_order(all_objects_mbrs)

    with open('test.txt', 'w') as f:
        for z_order in z_order_mbrs:
            f.write(f'{z_order}\n')

    sorted_mbrs = []
    # With the z-order sort all objects mbrs in a new list #
    with open('files/z_order.txt', 'w') as fi:
        for z_order in sorted(z_order_mbrs, key=lambda x: x[1]):
            fi.write(f'{z_order}\n')
            sorted_mbrs.append([z_order[0], all_objects_mbrs[z_order[0]]])

    with open('files/sorted_Mbrs.txt', 'w') as f2:
        for mbr in sorted_mbrs:
            f2.write(f'{mbr}\n')
    
    print(f'len of z_order mbrs: {len(z_order_mbrs)}')
    print(f'len of sorted_mbrs: {len(sorted_mbrs)}')
    
    with open('Rtree.txt', 'w') as r_tree:
        r_tree.write("Tree is being constructed...\n")
        
        construct_r_tree(sorted_mbrs, r_tree, isnonleaf=0)

def construct_r_tree(mbrs, r_tree, isnonleaf):
    global ID_INCR
    new_mbrs = []
    mbrs_copy = mbrs[:]
    size_of_mbrs = len(mbrs)
    if size_of_mbrs <= 2:
        # TODO create root node here
        return
    
    if size_of_mbrs % consts.MAX_CAPACITY == 0: 
        # We have size_of_mbrs/MAX_CAPACITY nodes  with capacity: MAX_CAPACITY   
        for node in range(0, size_of_mbrs//consts.MAX_CAPACITY):
            # create entry for node
            node_data = mbrs_copy[node*consts.MAX_CAPACITY:(node+1)*consts.MAX_CAPACITY]
            #[isnonleaf, node-id, [[id1, MBR1], [id2, MBR2], …, [idn, MBRn]]]
            r_tree.write(f"[{isnonleaf}, {ID_INCR}, {node_data}]\n")
            new_mbrs.append([ID_INCR, node_data])
            ID_INCR += 1
            # add entry to new_mbrs 
    
    elif size_of_mbrs % consts.MAX_CAPACITY >= 8:
        pass
    else:
        pass

    
    with open('files/new_mbrs_in_tree.txt', 'w') as f:
        for mbr in new_mbrs:
            l = []
            for x in mbr[1]:
                l.append(x[1])
            #f.write(f'{l}\n')
            l = calculate_mbrs_nonleafs(l)
            f.write(f'{l}\n')
    
    #new_mbrs = calculate_mbrs_nonleafs(new_mbrs)
    #construct_r_tree(new_mbrs, r_tree, isnonleaf=1)

def calculate_mbrs_nonleafs(mbrs):
    for mbr in mbrs:
        for node_mbr in mbr:
            pass
main()