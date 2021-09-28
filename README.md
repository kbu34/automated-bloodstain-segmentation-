# Automated Bloodstain Segmentation

This is a tool kit for Automatic Bloodstain Spatter Pattern analysis.

It provides automatic dectection and segmentation of stains then various stain and pattern metrics are computed.

Includes a table view and annotated image view.


# Windows/Linux/MacOS install

Requirements:
 - miniconda3 [https://docs.conda.io/en/latest/miniconda.html] (64 bit, Python 3.9). 
 - git (if in Windows)[https://git-scm.com/downloads]

#### Windows:
Open up an Anaconda shell (link in start menu). Navigate to the desired install location.
```
git clone https://eng-git.canterbury.ac.nz/kbu34/automated-bloodstain-segmentation-improved.git

cd Automated_Bloodstain_segmentation-improved
pip install -r requirements.txt

cd stain_segmentation
```

#### Linux/MacOS:
Open terminal (ctrl + alt + T on Linux).

Navigate to the desired installation location.

Enter the following commands to the terminal line by line.

```
git clone https://eng-git.canterbury.ac.nz/kbu34/automated-bloodstain-segmentation-improved.git

cd Automated_Bloodstain_segmentation-improved
pip install -r requirements.txt

cd stain_segmentation
```

### UI Tool

```
python -m app.main
```


### Command line interface
Analyse single image 
```
python -m scripts.analysis my_image.jpg -s 7.0
```


### Batch Processing
Analyse a folder of images, example:
```
python -m scripts.analysis my_folder/ -s 7.0 --overwrite
```


### Options
```
optional arguments:
  -h, --help            show this help message and exit
  -s SCALE, --scale SCALE
                        scale in pixels per mm
  -o OUTPUT, --output OUTPUT
                        folder for output (default is <file path>/output)
  --show                show stain detection
  --no-linearity        disable linearity computation
  --no-distribution     disable distribution computation
  --no-convergence      disable convergence computation
  --overwrite           overwrite output folder
```

# CNN Pattern Classifcation
Included in this repo there is an implementation for a converlotional neural network that classifies between Cast off, expirated and impact patterns.

It uses transfer learning with ResNet using Pytorch. The code is basically the transfer learning tutorial from pytorch see here( https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html) for more details.

It depends on pytorch and has been set up with GPU enabled.

To run it first change the path of the dataset then to train use

<code> python transfer_resnet.py </code>

to evaluate use 

<code> python transfer_resnet.py --model [path to your model here] </code>

This requires the image to be cropped to 1000-1000 around the highest density of stains. Code to automate this is in the branch "cropping-at-highest-density" inside this repo.

  
#### Contact

For more information see the report attached to this repo or email me at clairelouisebarnaby@gmail.com

For further work on this repo see https://docs.google.com/document/d/1_ieyeSxFw5pi7pMLjonNRQM7eUtoN1-qwqkRn5WOLdY/edit?usp=sharing

For information on the improved version contact me Phillip Kim at phillipkim156@gmail.com