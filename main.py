import cv2
import time
import threading

CLIP_SIZE = 15
FPS = 25
# Set up the video capture
cap = cv2.VideoCapture('rtsp://admin:elefante123123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0')

# Buffer to store frames (max length to hold 60 seconds worth of video)
frames_buffer = []



# Function to save video clip
def save_clip(buffer, output_path='clip.avi', fps=FPS, frame_size=(640, 480)):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI format
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
    for frame in buffer:
        out.write(frame)
    out.release()
    print(f"Saved clip to {output_path}")



def snip_buffer_start(buffer):
    snip_frame =(int) (FPS * CLIP_SIZE)
    return buffer[snip_frame:]
   
def crop_frames_buffer(buffer):
    crop_frame = (int) (FPS * CLIP_SIZE)
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
    
    
    frames_buffer.append(frame)


    current_time = time.time()

    if current_time - last_update_time >= 15:
        if first_track:
            first_track = False
        else:
            last_update_time = current_time
            frames_buffer = snip_buffer_start(frames_buffer)

    if current_time - last_log_time >= 1:
        FPS = cap.get(cv2.CAP_PROP_FPS) 
        print('Len buffer = {} | FPS = {}'.format(len(frames_buffer), FPS), end='\r',flush=True)
        last_log_time = time.time()

    cv2.imshow('Video', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Escape key
        print("Exiting...")
        break
    elif key == 32:  # Space key
        print("Saving last 30 seconds as a clip...")
        buffer = crop_frames_buffer(frames_buffer)
        # Run save_clip in a separate thread
        save_thread = threading.Thread(target=save_clip, args=(buffer, 'clip.avi', 30, (frame.shape[1], frame.shape[0])))
        save_thread.start()

# Clean up
cap.release()
cv2.destroyAllWindows() 
