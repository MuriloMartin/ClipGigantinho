import cv2
import time
from collections import deque

CLIP_SIZE = 30
# Set up the video capture
cap = cv2.VideoCapture('http://192.168.0.51:8080/video')

# Buffer to store frames (max length to hold 60 seconds worth of video)
frames_buffer_pos = []
frames_buffer_neg = []

current_buffer = 1

# Function to save video clip
def save_clip(buffer, output_path='clip.avi', fps=30, frame_size=(640, 480)):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI format
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
    for frame in buffer:
        out.write(frame)
    out.release()
    print(f"Saved clip to {output_path}")



def combine_buffers(current_buffer, buffer_pos, buffer_neg):
    crop_frame = 30 * CLIP_SIZE
    if current_buffer == 1:
        buffer = buffer_neg + buffer_pos
    else:
        buffer = buffer_pos + buffer_neg
    return buffer[-crop_frame:]
   


# Initialize a variable to track the last update time
last_update_time = time.time()
last_log_time = time.time()
first_track = True
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break
    
    if current_buffer == 1:
        frames_buffer_pos.append(frame)
    else:
        frames_buffer_neg.append(frame)
    

    current_time = time.time()
    if current_time - last_update_time >= 30:
        current_buffer = current_buffer * -1

        if current_buffer == 1:
            frames_buffer_pos = []
        else:
            frames_buffer_neg = []

        last_update_time = current_time  # Update the last update time
        new_track_time = time.time()
        first_track = False
    
    if not first_track and current_time - new_track_time >= 30:
        if current_buffer == 1:
            frames_buffer_neg = []
        else:
            frames_buffer_pos = []

    if current_time - last_log_time >= 2.5:
        print('Current buffer = {} | Len buffer pos = {} | Len buffer neg = {}'.format(current_buffer,len(frames_buffer_pos), len(frames_buffer_neg)))
        last_log_time = time.time()

    cv2.imshow('Video', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Escape key
        print("Exiting...")
        break
    elif key == 32:  # Space key
        print("Saving last 30 seconds as a clip...")
        buffer = combine_buffers(current_buffer,frames_buffer_pos, frames_buffer_neg)
        save_clip(buffer, frame_size=(frame.shape[1], frame.shape[0]))

# Clean up
cap.release()
cv2.destroyAllWindows() 
