# Camera Calibration

📷 This repository provides a script to generate the distortion matrix used in VSS-Vision.

## How to Use:
### Step 1:
- Save a minimum of 10 frames taken from the camera to be used, using an image of a chessboard. ([Example](https://github.com/ersaraujo/camera-calibration/tree/3f2d89ca96ddf2b960ccab20e2d2bad48952bb0b/img/exemplos))
- The "img" folder contains a script for capturing frames.

**To Run:**
```python capture_frames.py```  or  ```python3 capture_frames.py```
- To capture a frame, press 's'.
- After capturing a minimum of 10 frames, press 'q'.

### Step 2: Run the calibration script ```camera_calibration.py```
**To Run:**
```python camera_calibration.py```  or  ```python3 camera_calibration.py```
- After the script execution, the matrix will be saved in the root of the repository in an XML file.
- A visualization of the distortion removal will be displayed; to exit, press 'q'.

## Reference:
- [OpenCV Tutorial](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
