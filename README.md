# Real-time Facial Recognition
This project demonstrates real-time facial recognition, using pre-trained Haar cascade classifier in OpenCV and the online facial recognition service provides by [Kairos](https://www.kairos.com/).

## Pre-requisites
We use [Conda](https://www.continuum.io/content/conda-data-science) to manage the Python environment. The configuration file is provided in the project root.
```
conda env create -f conda_env.txt
```

## Quick Start
Use
```
source activate cnl
```
to initiate the Python environment, and
```
python demo.py -d
```
to start the real-time identification. This is a sub-project of our Computer Network Lab 2017 course, hence the identification result will get piped to a server backend of ours. 
