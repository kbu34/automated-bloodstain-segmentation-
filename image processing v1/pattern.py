import numpy as np

class Pattern:

    def __init__(self, stains=[]):
        self.stains = stains
        self.elliptical_stains = []
        for stain in self.stains:
            if stain.ellipse:
                self.elliptical_stains.append(stain)
    
    def add_stain(self, stain):
        self.stains.append(stain)
        if stain.major_axis != None:
            self.elliptical_stains.append(stain)

    def convergence(self):
        intersects = []
        stains = sorted(self.elliptical_stains, key= lambda s: s.major_axis[0])
        for i in range(len(stains) - 1):
            axis = stains[i].major_axis
            j = i + 1
            still_left = stains[j].major_axis[0][0] < axis[1][0]
            while  j < len(stains) - 1 and still_left:
                intersect = self.line_intersection(axis, stains[j].major_axis)
                if intersect:
                    intersects.append(intersect)
                j += 1
                still_left = stains[j].major_axis[0][0] < axis[1][0] 
        print("intersects:" ,intersects)
        # TODO work out what to do here and clean up the code!


    def line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) 

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return None

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y
    
    def linearity(self):
        pass

    def distribution(self):
        pass