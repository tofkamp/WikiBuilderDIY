import math

class Polygon:
    def __init__(self,startx = 0.0,starty = 0.0,direction = 0):
        self.x = startx
        self.y = starty
        self.direction = direction
        self.points = [(self.x,self.y)]
        self.stack = []

    def forward(length):
        self.x += math.cos(math.radians(self.direction)) * length
        self.y += math.sin(math.radians(self.direction)) * length
        self.points.append((self.x,self.y))
        
    def forward(length,width):
        self.x += math.cos(math.radians(self.direction)) * length
        self.y += math.sin(math.radians(self.direction)) * length
        self.x += math.cos(math.radians(self.direction + 90)) * width
        self.y += math.sin(math.radians(self.direction + 90)) * width
        self.points.append((self.x,self.y))

    def left(self,angle = 90):
        self.direction += angle

    def right(self.angle = 90):
        self.left(-angle)
    
"""
    def push(self):
        self.stack.append((self.x,self.y,self.direction))

    def pull(self):
        if self.stack:
            self.x, self.y, self.direction = self.stack.pop()
        else:
            print("ERROR stack empty")

    def close(self):
        self.x, self.y = self.points[0]
        self.points.append((self.x,self.y))
"""
        
