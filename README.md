# MeterVideo2Txt

## Introduction
Logs digital meter readings from standalone devices from video. 

All you need is to record a video of your reading.

This project will convert video of oximetry readings into logs as a use case.
Internally, it relies on pretrained AI for OCR based on the library [MMOCR](https://github.com/open-mmlab/mmocr).


## Tech stack: 
- OpenCV
- Qt
- MMOCR
- Pandas


## Requirements
- Ubuntu 22.04.3 LTS (Windows is possible but not tested)
- Nvidia's GPU capable of installing CUDA 11.8 and it's drivers.
- Python's [Anaconda](https://www.anaconda.com/download) for virtual environment 
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Installation
Go to your terminal, create a folder that you would like to clone the repo. 

Run the following command in your terminal to clone this repo. 
```bash 
git clone https://github.com/cpoohee/MeterVideo2Txt
```

Assuming, anaconda is properly installed, run the following to create the environment
```bash 
conda env create -f requirements.yml
```

Activate the environment
```bash 
conda activate MV2T
```

Then, run the app.
```bash 
python src/main.py
``` 

For the first time running the app, it will appear unresponsive. 
It will take some time to download and cache the AI models. 

## Usage
- load the video under ``File->Load video``
- Select the appropriate rotation of the video under ``Orientation->``
- Select the choice of text detection model under ``Detector Model->``
  - if ``Fixed Area`` is selected, click and drag a bounding box on the video for tracking. A label will be created for the area.
  - otherwise, double-click on the detected bounding box for tracking . A label will be attached to the box.
- Select the choice of text recognition model under ``Recognizer Model->``
- No duplicated labels are allowed. 
- Navigate the video using the Slider, or the spinbox to go to an exact frame. 
  - You can choose the starting frame where the detection starts.
- Click on ``Track Next Frame`` to track values that are labelled.
- Click on ``Track Subsequent Frames`` to track values from the current frame onwards.
- Click on ``Export`` to save the tracked values to CSV/Excel's xlsx/Panda's Pickle files.

## FAQ 
- If the ``mmcv`` library encounters errors, it might need to be recompiled.
  - see [build mmcv from source](https://mmcv.readthedocs.io/en/latest/get_started/build.html)

- Why does the tracking drifted too far?
  - Currently, the tracking works by finding the nearest bounding boxes from the previous location.
  Unfortunately, some frame could be missing the detected text which in turn will create erroneous tracking. 
  In the future, I might add a threshold to prevent drifting.

## TODO list
- Test a very long video experience

## Possible Future Improvements
- Allow editing/repositioning of tracked Labels.
- Add threshold for tracking nearest polygon in tracking mode. 
- Add kalman filter for tracking between points
- Separate settings to download detectors and recognisers
- Utilise LLM to match words/header

