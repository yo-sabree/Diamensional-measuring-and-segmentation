This project uses YOLOv8 for object detection and segmentation, along with MiDaS for depth estimation, to measure object sizes in real-time using a webcam.
## Features

Real-time object detection and segmentation using [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics).
Depth estimation using [Intel ISL MiDaS](https://github.com/isl-org/MiDaS).
Object size classification based on estimated area in meters.
Interactive visualization with bounding boxes and labels indicating object size.

## Requirements
Ensure you have the following dependencies installed:
pip install ultralytics opencv-python numpy torch torchvision torchaudio

## Installation &amp; Setup

Clone the repository:
git clone https://github.com/yo-sabeer/object-size-measurement.git
cd Dimensional-measuring-and-segmentation

Install dependencies:
pip install -r requirements.txt
Run the script:
python main.py

## How It Works

The script captures frames from a webcam.
YOLOv8 detects objects and generates segmentation masks.
MiDaS estimates the depth map of the scene.
The script calculates object size using depth information and a predefined focal length.
Objects are classified as Small, Medium, or Large based on area in square meters.

## Key Parameters

Focal Length (focal = 600): Determines scale for size calculations.
Base Depth (base_z = 1.0): Adjusts scaling of depth measurements.
Area Thresholds:

&lt; 0.1m² → Small (Green)
0.1m² - 0.3m² → Medium (Orange)
&gt; 0.3m² → Large (Red)



## Example Output
The program displays an annotated video feed with:

Segmented objects (polygons around detected objects)
Bounding boxes with size labels
Real-time classification based on estimated object area

## Controls

Press 'q' to exit the application.

## Notes

Ensure the camera is stable for accurate depth estimation.
Depth estimation may have noise; consider smoothing techniques if necessary.

## 
## Acknowledgments

[Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
[Intel ISL MiDaS](https://github.com/isl-org/MiDaS)
OpenCV and PyTorch
