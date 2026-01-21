class Image:
    def __init__(self, id, image, size, scale=1):
        self.id = id
        self.img = image
        self.size = size
        self.scale = scale
        
        self.nodes = {}
    
    def add_node(self, node, x, y):
        # Ensures a node is not repeated
        if node in list(self.nodes.keys()):
            return False
        self.nodes[node] = (x,y)
        return True

    def __str__(self):
        return f"#{self.id}:\n\t" + "\n\t".join([ f"{node}: {v}" for node, v in self.nodes.items() ])
    

if __name__ == "__main__":
    img1 = Image(0, "photo1", size=(0,0))
    img1.add_node("AA", 50, 75)
    img1.add_node("AB", 60, 75)
    img1.add_node("AC", 100, 230)
    
    print(img1)