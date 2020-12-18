import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.stats import kde
from scipy.spatial import ConvexHull
import cv2
import os
import csv
import time


class Pattern:
    def __init__(self, image, thresh, filename, scale=7.0):
        
        self.image = image
        self.thresh = thresh
        self.name = filename
        self.contours = []
        self.stains = []

        self.scale = scale
        self.elliptical_stains = []
                
        self.summary_data = []
        self.plots = {}

    
    def add_stain(self, stain):
        self.stains.append(stain)
        if stain.major_axis != None:
            self.elliptical_stains.append(stain)

    def convergence(self):
        height, width = self.image.shape[:2]
        intersects = []
        stains = [stain for stain in self.elliptical_stains if stain.major_axis is not None ]

        stains = sorted(stains, key= lambda s: s.major_axis[0])
        for i in range(len(stains) - 1):
            axis = stains[i].major_axis
            j = i + 1
            still_left = stains[j].major_axis[0][0] < axis[1][0]
            while  j < len(stains) - 1 and still_left:
                intersect = self.line_intersection(axis, stains[j].major_axis)
                if intersect and intersect[0] < width and intersect[1] < height and intersect[0] > 0 and intersect[1] > 0:
                    intersects.append(intersect)
                j += 1
                still_left = stains[j].major_axis[0][0] < axis[1][0] 

        return self.plot_convergence(intersects)

    def plot_convergence(self, intersects, figsize=(18, 12)):
        if len(intersects):
            x = [i[0] for i in intersects]
            y = [j[1] for j in intersects]
            fig = plt.figure(figsize=figsize)

            fig.canvas.set_window_title('Convergence ' + self.name)
            self.plots['convergence'] = fig
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)

            self.plot_intersection_scatter(ax1, x, y)
            nbins = 25
            k = kde.gaussian_kde([x,y])
            xi, yi = np.mgrid[min(x):max(x):nbins*1j, min(y):max(y):nbins*1j]
            point_density = k([xi.reshape(-1), yi.reshape(-1)])

            box, convergence_point = self.calculate_convergence_box(point_density, xi, yi)
            self.plot_density_heatmap(ax2, x, y, xi, yi, point_density, box, fig)
            plt.tight_layout()
            
            return box, convergence_point
        else:
            return None, None

    def plot_intersection_scatter(self, ax1, x, y):
        height, width = self.image.shape[:2]
        ax1.plot(x, y, '*', markersize=0.5, color='g')
        ax1.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB), extent=[0, width, height, 0], aspect='auto') 
        ax1.set_xlim(0, max(x))
        ax1.set_ylim(max(y), 0)
        ax1.set_title("Scatter Plot of Directional Major Axis Intersections")
        ax1.set_xlabel("pixels")
        ax1.set_ylabel("pixels")

    def plot_density_heatmap(self, ax2, x, y, xi, yi, point_density, box, fig):
        im = ax2.pcolormesh(xi, yi, point_density.reshape(xi.shape), cmap='jet')
        ax2.add_patch(box)        
        ax2.set_ylim(max(y), 0)
        ax2.set_xlim(0, max(x))
        ax2.set_title("Heat Map of Convergence")
        ax2.set_xlabel("pixels")
        ax2.set_ylabel("pixels")
        cb = fig.colorbar(im, ax=ax2)
        cb.set_label('mean number of intersections')

    def calculate_convergence_box(self, point_density, xi, yi):
        most_dense = np.unravel_index(np.argmax(point_density), point_density.shape) # index
        convergence_point = (xi.flatten()[most_dense], yi.flatten()[most_dense])

        bound = point_density[most_dense] * 0.6
        most_dense_points_x = xi.flatten()[np.where(point_density > bound)]
        most_dense_points_y = yi.flatten()[np.where(point_density > bound)]
        
        box_min_x = min(most_dense_points_x)
        box_min_y = min(most_dense_points_y)
        box_width = max(most_dense_points_x) - box_min_x 
        box_height = max(most_dense_points_y) - box_min_y
        box = patches.Rectangle((box_min_x, box_min_y), box_width, box_height, linewidth=1, edgecolor='black', facecolor='none')
        return box, convergence_point

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
    
    def linearity(self,  figsize=(18, 12)):
        stain_centers_x = np.array([stain.position[0] for stain in self.stains])
        stain_centers_y = np.array([stain.position[1] for stain in self.stains])

        fig = plt.figure(figsize=figsize)
        fig.canvas.set_window_title('Linearity ' + self.name)
        self.plots['linearity'] = fig

        xp = np.linspace(0, max(stain_centers_x))
        fitted = np.polyfit(stain_centers_x, stain_centers_y, 2)
        poly = np.poly1d(fitted)
        _fitted_plot = plt.plot(stain_centers_x, stain_centers_y, '.', xp, poly(xp), '-')
        plt.ylim(max(stain_centers_y), 0)

        y_fit = poly(stain_centers_x)                         
        yi = np.sum(stain_centers_y) / len(stain_centers_y)          
        ssreg = np.sum((y_fit - yi) ** 2)   
        sstot = np.sum((stain_centers_y - yi) ** 2)   
        r_squared = ssreg / sstot

        plt.text(100, 100, "R^2 = " + str(r_squared))
        plt.xlabel("pixels")
        plt.ylabel("pixels")
        plt.title("Stain Centers fitted to a degree 2 polynomial")
        
        str_poly = str(poly).split('\n')[1]
        squared_term = str_poly.find('x') + 1
        str_poly = str_poly[:squared_term] + "^2" + str_poly[squared_term:]
        return str_poly, r_squared        

    def distribution(self,  figsize=(18, 12)):
        stain_number = len(self.stains)
        stains_area = 0
        points = []
        for stain in self.stains:
            points += (stain.contour[:,0]).tolist()
            stains_area += stain.area
        points = np.array(points)
        hull = ConvexHull(points)

        fig = plt.figure(figsize=figsize)
        fig.canvas.set_window_title('Distribution ' + self.name)
        self.plots['distribution'] = fig

        plt.plot(points[:,0], points[:,1], 'o')
        for simplex in hull.simplices:
            plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
        plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
        plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')

        plt.xlabel("pixels")
        plt.ylabel("pixels")
        plt.ylim(max(points[:,1]), 0)
        plt.title("Convex Hull of the stains")

        ratio_stain_number = stain_number / hull.volume
        ratio_stain_area = stains_area / hull.volume
        
        return ratio_stain_number, ratio_stain_area

    def calculate_summary_data(self, to_calculate):
        poly, r_squared,  ratio_stain_number, ratio_stain_area, str_convergence, str_box = [""]*6       

        if to_calculate['linearity']:
            print("computing linearity...")

            a = time.time()
            poly, r_squared = self.linearity()
            r_squared = "{:.4f}".format(r_squared)
        
        if to_calculate['distribution']:
            print("computing distribution...")

            a = time.time()
            ratio_stain_number, ratio_stain_area = self.distribution()
            ratio_stain_area = "{:.3e}".format(ratio_stain_area)
            ratio_stain_number = "{:.3e}".format(ratio_stain_number)

        if to_calculate['convergence']:
            print("computing convergence...")
            
            a = time.time()
            box, convergence_point = self.convergence()
            if convergence_point == None:
                str_box = "None"
                str_convergence = "None"
            else:
                str_box = "lower left (x,y) : ({:.1f},{:.1f}) Width : {:.1f} Height : {:.1f}".format(
                    box.get_x(), box.get_y(), box.get_width(), box.get_height())
                str_convergence = "({:.1f}, {:.1f})".format(*convergence_point)

 
        self.summary_data = [poly, r_squared,  ratio_stain_number, ratio_stain_area, str_convergence, str_box]
        return self.summary_data

    def get_summary_data(self, to_calculate):
        return self.summary_data if len(self.summary_data) > 0 else self.calculate_summary_data(to_calculate)
        

    def export(self, data, save_path, options):
        pattern_file = os.path.join(save_path, 'pattern.csv')

                
        with open(pattern_file, 'w', newline='') as csvfile:
            data_writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            metrics = ["Linearity - Polyline fit", "R^2", "Distribution - ratio stain number to convex hull area", 
                                    "ratio stain area to convex hull area", "Convergence - point of highest density", "box of %60 of intersections"]
            for i in range(len(metrics)):
                data_writer.writerow([metrics[i], data[i]])
    
        for name, figure in self.plots.items():
            figure_file = os.path.join(save_path, name + ".pdf")
            figure.savefig(figure_file)
        
