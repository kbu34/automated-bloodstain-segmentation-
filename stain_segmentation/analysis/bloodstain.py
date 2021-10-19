import cv2
import json
import numpy as np
import csv
import math



class Stain:
    """
	Stores the contour, fitted ellipse and calculates statistics for a single stain.

	Also contains code to draw its ellipse on a given image.
	"""

    def __init__(self, id, contour, scale, image): 
        self.contour = contour
        self.id = id
        moment = cv2.moments(contour)
        self.image = image
        self.position = (int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00'])) if moment['m00'] > 0 else (10,10)
        self.area = cv2.contourArea(self.contour)
        self.area_mm = self.area * (1 / scale ** 2)
        self.ellipse, self.c = self.fit_ellipse()
        self.major_axis = None
        self.ratio = None

        if self.ellipse is not None:
            (self.x_ellipse, self.y_ellipse), (self.width, self.height), self.angle = self.ellipse
            self.ratio = self.width / self.height
            if self.ratio < 0.86:
                self.ellipse = None
            self.major_axis = self.calculate_major_axis()
        else:
            self.x_ellipse, self.y_ellipse, self.width, self.height, self.angle = [None] * 5
        
    def fit_ellipse(self):
        """
		Fits an ellipse to the contour of the stain.
		Carries out tail-culling on the contour before fitting the ellipse.

		:return: The fitted ellipse in form ((centreX, centreY), (width, height), angle)
		"""
        contour = self.contour
        if len(self.contour) >= 5 and self.area > 9:
            max_dist = 0
            extreme_i = 0
            for i in range(len(self.contour)):
                pt = self.contour[i][0]
                dist_center = ((self.position[0] - pt[0]) ** 2 + (self.position[1] - pt[1]) ** 2) ** 0.5
                if max_dist < dist_center:
                    max_dist = dist_center
                    extreme_i = i
                
            hull = cv2.convexHull(contour,returnPoints = False)
            concave_sections = cv2.convexityDefects(contour, hull)

            concave_pts = []
            if concave_sections is not None:
                for i in range(concave_sections.shape[0]-1):
                    s, e, f, d = concave_sections[i,0]
                    concave_pts.append(tuple(self.contour[f][0]))

            end_tail = None
            start_tail = None
            i = (extreme_i + 1) % len(self.contour)
            k = (extreme_i - 1) % len(self.contour)
            (_, _) , (max_width, height), angle = cv2.minAreaRect(self.contour)

            small_width = True

            while i < len(self.contour) and k > 0 and small_width:
                pt_1 = self.contour[i][0]
                pt_2 = self.contour[k][0]
                dist = ((pt_1[0] - pt_2[0]) ** 2 + (pt_1[1] - pt_2[1]) ** 2) ** 0.5
                if (dist / min(max_width, height)) > 0.5 :
                    small_width = False
                    end_tail = i
                    start_tail = k
                i += 1
                k -= 1

            if end_tail and start_tail:
                if start_tail <= end_tail:
                    contour = np.concatenate((self.contour[:start_tail + 1], self.contour[end_tail:]))
                else:
                    contour = self.contour[end_tail: start_tail + 1]
                if len(contour) > 5:
                    ellipse = cv2.fitEllipse(np.array(contour))
                    (x, y), (MA, ma), angle = ellipse
                    A = np.pi / 4 * MA * ma
                    if A > 0 and self.area / A > 0.3: 
                        return ellipse, contour
                    else:
                        p = cv2.minAreaRect(np.array(contour))
                        a1, (width, height), a2 = p
                        if width > height:
                            p = a1, (height, width), a2
                        return p, contour
            else:
                ellipse = cv2.fitEllipse(np.array(contour))
                (x, y), (MA, ma), angle = ellipse
                A = np.pi / 4 * MA * ma
                if A > 0 and self.area / A > 0.3: 
                    return ellipse, []
                else:
                    p = cv2.minAreaRect(np.array(self.contour))
                    _, (width, height), _ = p
                    a1, (width, height), a2 = p
                    if width > height:
                            p = a1, (height, width), a2
                    return p, []
     
        return None, []
        
    def draw_ellipse(self, image):
        """
		Draws this stain's fitted ellipse on the given image.

		:param image: The image to draw on.
		"""

        if self.ellipse is not None:
            cv2.ellipse(image, self.ellipse, (0,255,0), 2)

    def circularity(self):
        """
		Returns the circularity of the stain. Values closer to 0 indicate more elliptical, closer to 1 means more circular.

		:return: Circularity as a scalar in the range [0, 1]
		"""
        if self.ellipse:
            return min(self.width, self.height) / max(self.width, self.height)
        else:
            return float('inf')

    def orientaton(self):
        """
        Returns the gamma angle value of the stain. Return infinite if elipse is not found.

        :return: Orientation in the form of [angle, gamma]
        """
        if self.ellipse:
            if self.direction()[0] == "left":
                gamma = (self.angle + 180) % 360
            else:
                gamma = self.angle
            return [self.angle, gamma]
        return [float('inf'), float('inf')]


    def direction(self):
        """
        Returns the direction of the stain. First value indicates the x axis direction and 
        the second value indicates y axis direction.

        :return: Direction in the form of [x_direction, y_direction]
        """
        if self.ellipse:
            convex_hull = cv2.convexHull(self.contour)
            deltas = map(lambda pt: (pt - self.position)[0], convex_hull)
            extremity = max(deltas, key=lambda delta: math.sqrt(delta[0] ** 2 + delta[1] ** 2))
            self.extremity = self.position + extremity

            direction = [None, None]
            direction[0] = 'left' if extremity[0] < 0 else 'right'
            direction[1] = 'up' if extremity[1] < 0 else 'down'
            return direction
        return [None, None]

    def calculate_major_axis(self):
        """
        Calculates and returns the major axis of the stain.

        :return: Major axis in the form [x0, y0, x1, y1]
        """
        x = self.position[0] 
        y = self.position[1]
        direction = self.direction()

        if self.angle:
            pty = np.cos(np.deg2rad(self.angle)) * self.image.shape[1]
            ptx = np.sin(np.deg2rad(self.angle)) * self.image.shape[0]
            x0 = int(x + ptx)
            x1 = int(x - ptx)
            y0 = int(y - pty)
            y1 = int(y + pty)
            
            if direction != [None, None]:
                if direction[0] == "left":
                    x_use = max(x0, x1)
                else:
                    x_use = min(x0, x1)
                if direction[1] == "up":
                    y_use = max(y0, y1)
                else:
                    y_use = min(y0, y1)
                return sorted([(x, y), (int(x_use), int(y_use))], key=lambda x : x[0]) 
            return sorted([(int(x0), int(y0)), (int(x1), int(y1))], key=lambda x : x[0]) 

    def area_half(self, half_contour):
        if len(half_contour) > 0:
            hull_half = cv2.contourArea(cv2.convexHull(half_contour))
            if hull_half > 0:
                return cv2.contourArea(half_contour) / hull_half
        return -1

    def intensity(self):
        """
		Returns the average intensity (amount of colour) of the pixels contained within the stain.

		:return: Intensity as a scalar in the range [0, 1]
		"""
        grey = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        mask = np.zeros(grey.shape, np.uint8)
        cv2.drawContours(mask, [self.contour], 0, 255, -1)
        intensity = cv2.mean(grey, mask=mask)
        return intensity[0] / 255

    def solidity(self):
        """
		Returns the solidity of the stain, which represents the regularity of its margin.
		Calculated from the area of the stain's contour divided by the area of its convex hull.

		:return: Solidity as a scalar in the range [0, 1]
		"""
        if self.ellipse:
            hull = cv2.convexHull(self.contour)
            hull_area = cv2.contourArea(hull)
            if hull_area > 0:
                return self.area / hull_area
            else:
                return None
        return None
    
    def annotate(self, image, annotations={
        'ellipse':True, 'id':False, 'directionality':False, 
        'center':False, 'gamma':False, 'direction_line': False}):
        """
		Annotates the given image with the fitted ellipse for the stain and other properties depending on parameters.

		:param image: The image to annotate.
		:param annotations: A dictionary describing which annotations to include.
		"""

        font = cv2.FONT_HERSHEY_SIMPLEX
        text = ""

        if annotations['ellipse'] and self.ellipse:
            self.draw_ellipse(image)
        if annotations['id']:
            text += str(self.id)
        if annotations['directionality']:
            text += " " + str(self.direction())
        if annotations['center']:
            cv2.circle(image, (self.position[0], self.position[1]), 2, (255, 255, 255), -1)   
        if annotations['gamma']:
            text += " " + str(self.orientaton()[1])
        if annotations['direction_line'] and self.angle:
            cv2.line(image , self.major_axis[0], self.major_axis[1], (255,0,0), 2)
        cv2.putText(image, text, (int(self.position[0] + 10), int(self.position[1] + 30)), font, 1, (0,255,255), 2, cv2.LINE_AA)

    def label(self):
        points = [x[0] for x in self.contour.tolist() ]

        return [self.id] + points

    def obj_format(self, width, height):
        points = [x[0] for x in self.contour.tolist() ]
        str_points = ""
        for pt in points:
            str_points += "{} {} 0\n".format(pt[0] / width, pt[1] / height)
        return str_points

    def get_summary_data(self):
        summary_data = [self.id, self.position[0], self.position[1], int(self.area), self.area_mm, self.width, self.height, self.ratio, \
                self.orientaton()[0], self.orientaton()[1], str(self.direction()), self.solidity(), self.circularity(), self.intensity()]
        formatted = []
        for data in summary_data:
            if (data == float('inf')):
                data = None
            if (isinstance(data, float)):
                formatted.append("{:.3f}".format(data))
            else:
                formatted.append(data)
        return formatted
    
    def write_data(self, writer):
        writer.writerow(self.get_summary_data())

    
