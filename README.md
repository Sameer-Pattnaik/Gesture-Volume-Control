# Gesture Volume Control Using OpenCV

## Overview
This project demonstrates a real-time system that allows users to control their computer's volume using hand gestures. The system leverages **OpenCV** for video processing, **Mediapipe** for hand tracking, and **PyCaw** for volume control on Windows.

---

## Features
1. **Real-Time Hand Tracking**:
   - Detects and tracks hand landmarks using Mediapipe.
2. **Gesture-Based Volume Control**:
   - Measures the distance between the thumb and index finger to adjust the volume.
3. **Visual Feedback**:
   - Displays a volume percentage on the screen.
   - Shows visual markers (circles and lines) for fingertips and distance.

---

## Prerequisites

### Install Dependencies
1. **Python 3.x**: Ensure Python is installed on your system.
2. Install required libraries:
   ```bash
   pip install opencv-python mediapipe pycaw
   ```

3. **PyCaw** is Windows-specific. Ensure you are using a Windows OS for this implementation.

### Hardware
- A computer with a webcam for capturing video input.

---

## Code Explanation

### 1. **Import Libraries**
The necessary libraries for the program include:
- `cv2` for video processing.
- `mediapipe` for hand tracking.
- `pycaw` for controlling the system's volume.

### 2. **Setup for Mediapipe and PyCaw**
- **Mediapipe**:
  - Detects hand landmarks, such as the index finger and thumb.
- **PyCaw**:
  - Provides access to the system's audio controls, including volume adjustment.
  - Retrieves the system's current volume range and adjusts it dynamically.

### 3. **Gesture Detection**
- The program calculates the distance between the index finger tip and the thumb tip using the Euclidean formula:
  ```python
  distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
  ```

### 4. **Volume Mapping**
- The distance is mapped to the system's volume range using `np.interp`:
  ```python
  normalized_volume = np.interp(distance, [30, 150], [min_volume, max_volume])
  ```

### 5. **Visual Feedback**
- Circles and lines are drawn to visualize the thumb and index finger.
- Volume percentage is displayed as text on the screen.

---

## Running the Program

1. **Start the Program**:
   - Save the code to a file, e.g., `gesture_volume_control.py`.
   - Run the program:
     ```bash
     python gesture_volume_control.py
     ```

2. **Control Volume**:
   - Place your hand in front of the webcam.
   - Bring your thumb and index finger closer to decrease volume or farther apart to increase it.
   - The system updates the volume in real-time.

3. **Exit**:
   - Press `q` to quit the application.

---

## Code Details

### Main Sections
#### 1. **Hand Tracking Setup**
```python
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
```
Initializes the Mediapipe hand tracking module.

#### 2. **Volume Control Setup**
```python
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_volume, max_volume, _ = volume.GetVolumeRange()
```
Configures PyCaw to control the system volume.

#### 3. **Real-Time Gesture Processing**
```python
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    # Process each frame from the webcam
```
Tracks hand landmarks in real time with Mediapipe's `Hands` class.

#### 4. **Visual Feedback**
```python
cv2.circle(frame, index_finger_tip, 10, (255, 0, 0), -1)
cv2.circle(frame, thumb_tip, 10, (0, 255, 0), -1)
cv2.line(frame, index_finger_tip, thumb_tip, (255, 255, 0), 2)
```
Draws visual markers for better user feedback.

#### 5. **Volume Adjustment**
```python
normalized_volume = np.interp(distance, [30, 150], [min_volume, max_volume])
volume.SetMasterVolumeLevel(normalized_volume, None)
```
Maps the finger distance to the system volume range and adjusts the volume.

---

## Customization

### Sensitivity
Adjust the `np.interp` range for `distance` to control sensitivity:
```python
normalized_volume = np.interp(distance, [30, 150], [min_volume, max_volume])
```
- Increase `30` (minimum) to require fingers closer for minimum volume.
- Decrease `150` (maximum) to require less distance for maximum volume.

### Visual Feedback
Modify the colors, sizes, and positions of the markers:
```python
cv2.circle(frame, index_finger_tip, 10, (255, 0, 0), -1)  # Color and size
```

---

## Troubleshooting

1. **Volume Not Changing**:
   - Ensure PyCaw is installed and your system supports its functionality.
   - Test with other audio devices if the default one doesn’t work.

2. **No Hand Detected**:
   - Ensure proper lighting for the webcam.
   - Adjust `min_detection_confidence` and `min_tracking_confidence` values.

3. **Slow Performance**:
   - Ensure your system meets hardware requirements.
   - Use a lower resolution for the webcam input.

---

## Example Output
- **Visualization**:
  - Circles drawn on the thumb and index finger tips.
  - A line connecting the tips showing the distance.
- **Volume Display**:
  - Volume percentage displayed on the video feed.

---

## Conclusion
This project provides a fun and interactive way to control system volume using hand gestures. It combines advanced computer vision (Mediapipe) with practical audio control (PyCaw), demonstrating the power of Python in creating real-time interactive applications.
