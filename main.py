import cv2
from pathlib import Path
from math import sqrt

import image

IMG_PATH = Path("./img_02")
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

nodes = {}


def main():
    # Load and annotate images
    images = load_img(IMG_PATH)
    for img in images:
        annotate_image(img)
    
    # Triangulate the image positions
    
    # Create a meshnet based on images


def load_img(path: Path):
    desired_height = 700
    images = []
    for i,file in enumerate(path.iterdir()):
        img = cv2.imread(file, 1)
        h,w = img.shape[:2]
        
        scale = desired_height/h
        
        img = cv2.resize(img, None, fx=scale,fy=scale)
        img = image.Image(i, img, (scale*h,scale*w), scale)
        
        images.append(img)
    return images


def annotate_image(img: image.Image):
    print("[annotate_image] Entering")
    offset = 10
    def click_event(event, x, y, flags, img):
        if event == cv2.EVENT_LBUTTONDOWN:
            node = get_node(img,x,y)
            valid = add_node(node,img,x,y)
            if not valid:
                return
            
            cv2.circle(img.img, (x, y), 8, (0,0,255),-1)
            cv2.putText(img.img,node,(x+offset,y+offset),cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,0,0),2)
            cv2.imshow('Image', img.img)
    
    while True:
        cv2.imshow("Image", img.img)
        cv2.setMouseCallback('Image', click_event, img)
        if cv2.waitKey(1) == ord('q'):
            break


def get_node(img, x, y):
    print("[get node] Entering")
    radius = 50
    POS = {
    0: (int(x+radius), int(y)),
    1: (int(x+radius//sqrt(2)),int(y+radius//sqrt(2))),
    2: (int(x), int(y+radius)),
    3: (int(x-radius//sqrt(2)),int(y+radius/sqrt(2))),
    4: (int(x-radius), int(y)),
    5: (int(x-radius//sqrt(2)),int(y-radius//sqrt(2))),
    6: (int(x), int(y-radius)),
    7: (int(x+radius//sqrt(2)),int(y-radius//sqrt(2)))
}
    circle_size = 12
    node = {'node': None,}
    
    def click_event(event, x, y, flags, param):
        global node
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, posis in enumerate(POS.values()):
                item_x, item_y = posis
                if x < item_x+circle_size/2 and x > item_x-circle_size/2:
                    if y < item_y+circle_size/2 and y > item_y-circle_size/2:
                        param['node'] = i

    existing_nodes = list(nodes.keys())
    if len(existing_nodes) == 0:
        nds = ['AA']
    elif len(existing_nodes) < 7:
        nds = existing_nodes
    else:
        nds = existing_nodes[-7:]
    
    nds.append(get_next(nds[-1]))
    print(nds)
    
    img_copy = img.img.copy() # Save current state
    
    for i,nd in enumerate(nds):
        print((POS[i][0],POS[i][1]))
        cv2.circle(img.img, (POS[i][0],POS[i][1]), circle_size, (0,0,255), -1)
        cv2.putText(img.img,nd, (POS[i][0],POS[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0), 2)
        cv2.imshow("Image", img.img)
    
    while True:
        cv2.imshow("Image", img.img)
        cv2.setMouseCallback('Image', click_event, node)
        cv2.waitKey(1)
        if not node['node'] is None or cv2.waitKey(1) == ord('q'):
            print("[get node] Exiting")
            break
    
    img.img = img_copy
    return nds[node['node']]


def add_node(node,img,x,y):
    node_nums = list(nodes.keys())
    if not len(node) == 2:
        print("[add_node] Error: Node code invalid, must be two chars")
        return False
    
    if not node in node_nums:
        if len(node_nums) == 0:
            nodes[node] = []
        else:
            last_node = node_nums[-1]   
            if is_next(last_node, node):
                nodes[node] = []
            else:
                print("[add_node] Error: Must be sequential, Z->1, 9->0, 0->A")
                return False
        
    if not img.add_node(node,x,y):
        print("[add_node] Error: image could not add node")
        return False
    nodes[node].append(img)
    return True


def is_next(old_node, new_node):
    if NODE_ID[old_node[1]] == 35 and not NODE_ID[new_node[1]] == 0:
        return False
    if NODE_ID[old_node[1]] == 35 and not NODE_ID[new_node[0]] == NODE_ID[old_node[0]] + 1: # TODO this will be a problem for the 1296th node
        return False
    if not NODE_ID[new_node[1]] == ( NODE_ID[old_node[1]] + 1 ) % 36:
        return False
    return True


def get_next(node):
    if NODE_ID[node[1]] == 35:
        return (NODE_KEY[NODE_ID[node[0]]+1],NODE_KEY[0])
    return "".join([NODE_KEY[NODE_ID[node[0]]], NODE_KEY[NODE_ID[node[1]]+1]])


if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()

