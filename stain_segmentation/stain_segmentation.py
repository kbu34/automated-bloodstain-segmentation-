import cv2
import numpy as np
import sys
import os
from matplotlib import pyplot as plt
import bloodstain
import json
import csv
from parse_arguments import parse_args
from pattern import Pattern
from os import path
import pathlib

from tqdm import tqdm

default_options = {'linearity': True, 'convergence': True, 'distribution': True}

def process_image(filename, save_path, scale=7.0, show=False, options=None):
    image = cv2.imread(filename)

    if image is None:
        print("Failed to load image: ", filename)
        return

    output_path = path.join(save_path, path.basename(filename))
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    print("Segmenting stains")
    pattern = stain_segmentation(image, output_path, filename, scale=scale)

    cv2.drawContours(image, pattern.contours, -1, (255,0,255), 1)

    result = image.copy()
    for stain in pattern.stains:
        stain.annotate(result)

    if show:
        result_preview(result)

    cv2.imwrite(path.join(output_path, 'result.jpg'), result)
    print("Analysing Stains")
    export_stain_data(output_path, pattern)

    
    export_obj(output_path, pattern)

    print("\nCalculating Pattern Metrics")
    pattern.export(output_path, options or default_options)


image_types = ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']
def find_images(folder, file_types=image_types):
    images = []
    files = os.listdir(folder)
    for file in files:
        _, ext = path.splitext(file) 
        if ext.lower() in file_types:
            images.append(path.join(folder, file))
    return images




def batch_process(input_path, output_path=None, scale=7.0, show=False, options=None):
    save_path = output_path or path.join(input_path, "output")

    image_files = find_images(input_path)
    print(f"Batch processing {input_path}, found {len(image_files)} image files, output path: {save_path}")
    
    for i, image_file in enumerate(image_files):
        print(f"Processing image {i}/{len(image_files)}: {input_path}")
        process_image(image_file, save_path, scale, show, options=options)



def CLI(args={}):
    args = parse_args() if not args else args

    options = dict(
        convergence = not args.no_convergence,
        linearity = not args.no_linearity,
        distribution = not args.no_distribution,
    )

    if args.scale < 1:
        print("Warning scale is less than 1")

    if path.isfile(args.filename):
        save_path = args.output or path.join(path.dirname(args.filename), "output")
        print(f"Processing {args.filename}, output path: {save_path}")

        process_image(args.filename, save_path, args.scale, args.show, options=options)

    elif path.isdir(args.filename):
        batch_process(args.filename, args.output, args.scale, args.show, options=options)
    else:
        assert False, f"{args.filename} does not exist"

    print("Done :)")

    

def stain_segmentation(image, output_path,  filename, scale=7.0):
    pattern = Pattern(image, filename, scale=scale)
    
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    blur = cv2.GaussianBlur(image, (3,3), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    gray_hsv = cv2.cvtColor(hsv_img, cv2.COLOR_BGR2GRAY)
    
    thresh = binarize_image(image, gray)
    # cv2.imwrite('./binary.jpg', thresh) # uncomment to export a binary image

    # hist = cv2.calcHist( [gray_hsv], [0], None, [256], [0, 256] )
    remove_circle_markers(gray, thresh)
    # kernel = np.ones((3,3),np.uint8)
    cv2.imwrite(path.join(output_path, 'flipped-binary.jpg'), thresh)

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)     
    analyseContours(pattern, contours, hierarchy, image, pattern.scale)

    return pattern
    

def analyseContours(pattern, contours, hierarchy, image, scale):
    count = 0
    outer_contours = []
    for i in range(len(contours)):
        contour = contours[i]
        if hierarchy[0,i,3] == -1:
            outer_contours.append(contour)
            if cv2.contourArea(contour) > 5:
                stain = bloodstain.Stain(count, contour, scale, image)
                pattern.add_stain(stain)
                count += 1
    pattern.contours = outer_contours  

    print("Found {} stains".format(count))

def export_stain_data(save_path, pattern):    
    data_file = path.join(save_path, 'data.csv')
    csv_file = path.join(save_path, "stains.csv")

    with open(data_file, 'w', newline='') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(["id", "position x", "position y", "area px", "area_mm", "width ellipse", "height ellipse", \
                        "angle", "gamma", "direction", "solidity", "circularity", "intensity"])
        with open(csv_file, 'w') as point_file:
            points_writer = csv.writer(point_file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            i = 0
            for stain in tqdm(pattern.stains):
                stain.write_data(data_writer)
                points_writer.writerow(stain.label())


def export_obj(save_path, pattern):
    height, width, _ = pattern.image.shape

    file_name = path.join(save_path,  'points.pts')
    print("save path:", file_name)

    with open(file_name, 'w', newline='') as f:
        for stain in pattern.stains:
            f.write(stain.obj_format(width, height) )

def result_preview(img_original) :
    print("Press 'q' to close preview")
    while True:
        small = cv2.resize(img_original, (0,0), fx=0.25, fy=0.25)
        cv2.imshow('Blood Spatter', small)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def remove_circle_markers(gray, img):
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=100,
                                param2=58, minRadius=24, maxRadius=82)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(img, (i[0],i[1]),i[2] + 10, (0,0,0), -2)


def binarize_image(img_original, gray) :
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 99, 10)
    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations = 2)
    dilation = cv2.dilate(erosion, kernel, iterations = 2)

    return cv2.bitwise_not(dilation)

def label_stains(pattern):
    ''' Not used for research purposes to export json in readable format 
    for instance segmenation labelling tool 'label me' '''

    labels = {"shapes" : [], "lineColor": [0, 255, 0, 128],
    "imagePath": sys.argv[1],
    "flags": {},
    "imageData" : None,
    "fillColor": [255, 0, 0,128]}
    i = 0
    for stain in pattern.stains:
        labels["shapes"].append(stain.label(" " + str(i)))
        i = i + 1

    mask_filename = path + os.path.splitext(sys.argv[1])[0] + '.json'
    with open(mask_filename, 'w') as outfile:
        json.dump(labels)

def show_intentsity_histogram(img):
    ''' Not used for research purposes'''

    plt.hist(img.ravel(), 256, [0, 255])
    plt.xlim([0, 360])
    plt.show()

if __name__ == '__main__':
    CLI()