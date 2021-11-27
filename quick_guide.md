# Bloodstain Analysis Tool Quick Duide for Developers

Last edited 27/11/2021 by Phillip Kim

This file is a short guide to help new developers give the basic idea of the code base of the analsysis tool and get to working on development as soon as possible. For more detailed documentation, check out the source code documentation.

Feel free to run and mess around with the program as you read the code structure part of this guide, seeing the code being run will help with understanding.

## Setting up your development environment
You will need a python IDE for this, the recommended IDE is the Microsoft Visual Studio Code as it is free and light-weight. This IDE has worked well for previous years. Other Python IDEs such as Pycharm, Wing, and IntelliJ(with extensions), have not been tested for this project. If you wish to experiment with other IDEs for reasons, please document them for future students.

Refer to README for OS specific installation process for the project itself. You will need to download all dependecies listed in the requirements.txt file.

# Code Structure
The stain_segmentation directory contains few more folders. This guide will go through the general idea what each file does in the folders.

# analysis
This folder contains the definitions and the methods for the main classes the tool will use. bloodstain.py and pattern.py will contain definitions of the bloodstain and the pattern. You can consider pattern as a collection of bloodstains in the image. Either refer to the initialisation methods or the source code documentation for what  kind of data they carry. 

### bloodstain.py
When the segment image process is run, each row in the spreadsheet represents a bloodstain object. All stains on the image are analysed and put into the stains list in the pattern object.

Going through fit_ellipse() method in bloodstain.py line-by-line is recommended as it is one of the most important methods in the tool as stain ellipses are used in a lot of analysis processes and also one of the most complex methods in the project. 

### pattern.py
The pattern object contains the bloodstain objects calculated earlier and is used for pattern analysis such as calculating convergence, intersection, centroid, and linearity. Methods for each metric is documented in the source code documentation.

### stain_segmentation.py
This file is the heart of the segmentation process. This file uses the previously defined objects to run the actual analysis process when main.py tells it to do so. It also contains helper functions that are used by the tool, functions for modifying the image and exporting data.

# app
This directory is the core of this program. The base of operations. The files in this directory are used to set up the application and tell them what to do.

## main.py
As the name suggests, this is the main file of this program. The main purpose of this file is to set up GUI when the program is first run and tell the functions in other files to run when a certain conditions are met, such as pressing a button or importing an image into the program.

## photo_viewer.py
This file is responsible for setting up an image viewer, showing an image when it's imported, and displaying annotations on the image when looking at individual stains.

Each annotation item is put into a container called self._scene. The annotations in the frame is controlled by adding and removing these annotation items from the container.

# generated
This folder contains scripts for setting up the GUI. All files are structured the same way so it is relatively straight forward. If you need to set up new buttons and labels, look at the other objects in the file and follow their examples.

# Some notes
If some files are not covered in this guide, it means I never had to edit them. If you happen to need to use them, good luck and please document them for future students. I decided not to include them here as I felt not acknowledgeable enough to document them.

Please edit this guide if you change the structure or add something that is significant enough of being documented here to the project.

I hope this guide is useful to you.