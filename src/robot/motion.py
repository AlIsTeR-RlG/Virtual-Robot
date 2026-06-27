import math

"""
A class to move the robot around and record/
print it's current state. This is done by using 
trignomatry with the math module.

"""

class RobotState:
    
    def __init__(self, x=0.0, y=0.0, heading=0):
        self.x = x
        self.y = y
        self.heading = heading 
        
    def move_forward(self, distance=1.0):
        self.x += distance*math.cos(self.heading)
        self.y += distance*math.sin(self.heading)
    
    def move_backward(self, distance=1.0):
        self.x -= distance*math.cos(self.heading)
        self.y -= distance*math.sin(self.heading)
    
    def turn_left(self, angle=15):
        self.heading += math.radians(angle)
        
        if self.heading < 0:
            self.heading = 2*math.pi + self.heading
        if self.heading > 2*math.pi:
            self.heading = self.heading - 2*math.pi
    
    def turn_right(self, angle=15):
        self.heading -= math.radians(angle)
        
        if self.heading < 0:
            self.heading = 2*math.pi + self.heading
        if self.heading > 2*math.pi:
            self.heading = self.heading - 2*math.pi
        
    def __str__(self):
        return "Position:\n",f"x: {self.x:.2f}",f"y: {self.y:.2f}",f"heading: {math.degrees(self.heading):.1f}"
        