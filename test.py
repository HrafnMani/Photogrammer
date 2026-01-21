NODE_KEY = {
    0: 'A',  1: 'B',  2: 'C',  3: 'D',  4: 'E',
    5: 'F',  6: 'G',  7: 'H',  8: 'I',  9: 'J',
    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O',
    15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
    20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y',
    25: 'Z',
    26: 1,  27: 2,  28: 3,  29: 4,  30: 5,
    31: 6,  32: 7,  33: 8,  34: 9,  35: 0
}
NODE_ID = {
    'A': 0,  'B': 1,  'C': 2,  'D': 3,  'E': 4,
    'F': 5,  'G': 6,  'H': 7,  'I': 8,  'J': 9,
    'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14,
    'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
    'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
    'Z': 25,
    '1': 26,  '2': 27,  '3': 28,  '4': 29, '5': 30,  
    '6': 31,  '7': 32,  '8': 33,  '9': 34, '0': 35
}



def is_next(old_node, new_node):
    if NODE_ID[old_node[1]] == 35 and not NODE_ID[new_node[1]] == 0:
        return False
    if NODE_ID[old_node[1]] == 35 and not NODE_ID[new_node[0]] == NODE_ID[old_node[0]] + 1: # TODO this will be a problem for the 1296th node
        return False
    if not NODE_ID[new_node[1]] == ( NODE_ID[old_node[1]] + 1 ) % 36:
        return False
    return True

old_node = "AA"
for i in range(0,36):
    if not i: rng = range(1,36)
    else: rng = range(0,36)
    
    for j in rng:
        next_node = str(data[i]) + str(data[j])
        if not is_next(old_node, next_node):
            print(f'{old_node} != {next_node}')
            
        old_node = next_node