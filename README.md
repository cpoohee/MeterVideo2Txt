# MeterVideo2Txt

## Work in Progress!!

## Introduction
Logs digital meter readings from standalone devices from video. 

All you need is to record a video of your reading.

This project will convert video of oximetry readings into logs as a use case.
Internally, it relies on pretrained AI for OCR based on the library [MMOCR](https://github.com/open-mmlab/mmocr).

## Usage
TODO

## Installation
TODO

### Requirements
TODO


## TODO list
- Add mode to choose between tracking mode or fixed area mode.
- Allow editing/repositioning of tracked Labels.
- Add threshold for tracking nearest polygon in tracking mode. 
- Add kalman filter for tracking between points
- Separate settings to download detectors and recognisers

### Potential issues
- 2 or more values might be detected within the same bounding polygon. 
